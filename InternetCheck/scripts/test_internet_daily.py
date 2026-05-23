
#!/usr/bin/env python3
import csv
import os
import statistics
import subprocess
import time
from datetime import datetime, timezone
from pathlib import Path
import argparse

def ping_host(host: str, count: int, timeout_s: float):
    latencies = []
    for _ in range(count):
        try:
            result = subprocess.run(
                ["ping", "-c", "1", "-W", str(int(timeout_s)), host],
                capture_output=True, text=True, check=False
            )
            if result.returncode == 0:
                # find "time=XX.x ms"
                line = next((l for l in result.stdout.splitlines() if "time=" in l), None)
                if line:
                    try:
                        part = line.split("time=")[-1].split()[0]
                        latencies.append(float(part))
                    except Exception:
                        latencies.append(None)
                else:
                    latencies.append(None)
            else:
                latencies.append(None)
        except Exception:
            latencies.append(None)
        time.sleep(0.5)
    clean = [x for x in latencies if x is not None]
    if not clean:
        return None, None
    avg = sum(clean) / len(clean)
    jitter = statistics.stdev(clean) if len(clean) > 1 else 0.0
    return avg, jitter

def get_daily_file(out_dir: Path, prefix: str):
    today = datetime.now(timezone.utc).astimezone().date()  # local date
    subdir = out_dir / f"{today:%Y-%m}"
    subdir.mkdir(parents=True, exist_ok=True)
    return subdir / f"{prefix}_{today:%Y-%m-%d}.csv"

def log_row(path: Path, avg_latency, jitter):
    path.parent.mkdir(parents=True, exist_ok=True)
    is_new = not path.exists() or path.stat().st_size == 0
    with path.open("a", newline="") as f:
        w = csv.writer(f)
        if is_new:
            w.writerow(["timestamp", "latency_ms", "jitter_ms"])
        w.writerow([datetime.now().isoformat(), avg_latency, jitter])

def main():
    ap = argparse.ArgumentParser(description="Log internet latency/jitter into a per-day CSV file.")
    ap.add_argument("--host", default="8.8.8.8", help="Host to ping")
    ap.add_argument("--samples", type=int, default=5, help="Echo requests per run")
    ap.add_argument("--timeout", type=float, default=1.0, help="Timeout per ping (seconds)")
    ap.add_argument("--out", default="./logs", help="Directory to store daily CSVs")
    ap.add_argument("--prefix", default="latency", help="Filename prefix for CSVs")
    args = ap.parse_args()

    out_dir = Path(args.out).expanduser().resolve()
    csv_path = get_daily_file(out_dir, args.prefix)

    avg, jit = ping_host(args.host, args.samples, args.timeout)
    if avg is not None:
        log_row(csv_path, avg, jit)

if __name__ == "__main__":
    main()
