import serial
import csv
import glob
import time
from datetime import datetime
from pathlib import Path


# =========================
# 設定（ここだけ調整）
# =========================
BAUDRATE = 115200

LOG_HZ = 100                  # 等間隔ログ周波数
LOG_PERIOD_S = 1.0 / LOG_HZ

THRESHOLD = 110               # 閾値
OVER_TIMEOUT_S = 0.15         # 閾値超え保持時間（秒）

PORT_GLOB = "/dev/cu.usbmodem*"


def find_arduino():
    ports = sorted(glob.glob(PORT_GLOB))
    return ports[0] if ports else None


def main():
    port = find_arduino()
    print("Using port:", port)
    if port is None:
        raise RuntimeError("Arduino が見つかりません。")

    ser = serial.Serial(port, BAUDRATE, timeout=0)

    # ===== ログ保存先（この.pyと同じ場所）=====
    base_dir = Path(__file__).resolve().parent
    log_dir = base_dir / "logs"
    log_dir.mkdir(exist_ok=True)

    now = datetime.now()
    filename = f"Log_{now.strftime('%Y%m%d_%H%M%S')}.csv"
    filepath = log_dir / filename
    print("Logging to:", filepath)

    latest_raw = 0
    last_over_t = None

    t0 = time.monotonic()
    next_tick = t0

    def parse_sensor(line: str):
        try:
            return int(line.strip())
        except ValueError:
            return None

    try:
        with open(filepath, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["time_ms", "raw", "over_value", "over_flag"])
            f.flush()

            while True:
                now_t = time.monotonic()

                # --- シリアル受信 ---
                while ser.in_waiting > 0:
                    raw_bytes = ser.readline()
                    if not raw_bytes:
                        break
                    line = raw_bytes.decode("utf-8", errors="ignore").strip()
                    if not line:
                        continue

                    sensor = parse_sensor(line)
                    if sensor is None:
                        continue

                    latest_raw = sensor
                    if latest_raw >= THRESHOLD:
                        last_over_t = time.monotonic()

                # --- 次のログ時刻まで待つ ---
                if now_t < next_tick:
                    time.sleep(min(0.001, next_tick - now_t))
                    continue

                t_ms = int((now_t - t0) * 1000)

                if last_over_t is None:
                    over_flag = 0
                else:
                    over_flag = 1 if (now_t - last_over_t) <= OVER_TIMEOUT_S else 0

                over_value = latest_raw if latest_raw >= THRESHOLD else 0

                writer.writerow([t_ms, latest_raw, over_value, over_flag])
                f.flush()

                next_tick += LOG_PERIOD_S

    except KeyboardInterrupt:
        print("\nCtrl+C を受け取ったのでログを終了します。")
    finally:
        if ser.is_open:
            ser.close()
        print("シリアルポートをクローズしました。")
        print("ログファイル:", filepath)


if __name__ == "__main__":
    main()