
#!/usr/bin/env python3
import argparse
from pathlib import Path
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def plot_csv(csv_file: Path, out_png: Path):
    df = pd.read_csv(csv_file, parse_dates=["timestamp"])
    plt.figure(figsize=(10, 5))
    plt.plot(df["timestamp"], df["latency_ms"], marker="o", label="Latency (ms)")
    plt.plot(df["timestamp"], df["jitter_ms"], marker="x", label="Jitter (ms)")
    plt.xlabel("Time")
    plt.ylabel("Milliseconds (ms)")
    plt.title("Internet Latency & Jitter Over Time — " + csv_file.name.replace(".csv",""))
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.xticks(rotation=45)
    out_png.parent.mkdir(parents=True, exist_ok=True)
    plt.savefig(out_png)

def main():
    ap = argparse.ArgumentParser(description="Plot a single day's latency CSV to PNG.")
    ap.add_argument("csv", help="Path to daily CSV file")
    ap.add_argument("--out", help="Output PNG path; defaults next to CSV", default=None)
    args = ap.parse_args()

    csv_file = Path(args.csv).expanduser().resolve()
    out_png = Path(args.out).expanduser().resolve() if args.out else csv_file.with_suffix(".png")
    plot_csv(csv_file, out_png)
    print(f"Saved plot to {out_png}")

if __name__ == "__main__":
    main()
