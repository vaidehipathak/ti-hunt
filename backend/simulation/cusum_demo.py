"""CUSUM watchdog demo on synthetic feed volume (dummy data, for the review).
Run from the backend folder:  python simulation/cusum_demo.py
"""
import sys
import pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from app.watchdog.cusum import CUSUMWatchdog

T, T0, WARM = 200, 100, 50          # rounds, attack start, warm-up for baseline
K_SLACK, H_THRESH = 0.5, 5.0        # CUSUM parameters (in standard deviations)
rng = np.random.default_rng(42)


def make_series(kind):
    v = rng.poisson(30, T).astype(float)      # normal feed: ~30 events/round
    if kind == "sudden_burst":
        v[T0:] += 60                          # feed suddenly floods junk IOCs
    elif kind == "slow_ramp":
        v[T0:] += np.linspace(0, 25, T - T0)  # volume creeps up gradually
    return v


def run(series):
    mu, sd = series[:WARM].mean(), (series[:WARM].std() or 1.0)
    wd = CUSUMWatchdog(k=K_SLACK, h=H_THRESH)
    wd.set_baseline("feed", 0.0)              # we feed standardised values
    stat = []
    for t, x in enumerate(series):
        z = (x - mu) / sd
        if t < WARM:
            stat.append(0.0)
            continue
        fired = wd.update("feed", z)
        if fired:
            return stat, t                    # first alarm: stop here
        stat.append(max(wd.pos_cusum["feed"], wd.neg_cusum["feed"]))
    return stat, None


kinds = ["normal", "sudden_burst", "slow_ramp"]
fig, axes = plt.subplots(2, 3, figsize=(14, 6), sharex=True)
print(f"{'scenario':<14}{'alarm round':<14}{'delay after attack start'}")
for col, kind in enumerate(kinds):
    series = make_series(kind)
    stat, alarm = run(series)
    delay = "-" if alarm is None else alarm - T0
    print(f"{kind:<14}{str(alarm):<14}{delay}")
    top, bot = axes[0, col], axes[1, col]
    top.plot(series, color="#5b8def"); top.set_title(kind)
    bot.plot(range(len(stat)), stat, color="#f59e0b")
    bot.axhline(H_THRESH, color="red", ls="--", label="threshold h")
    for ax in (top, bot):
        if kind != "normal":
            ax.axvline(T0, color="grey", ls=":")
        if alarm is not None:
            ax.axvline(alarm, color="red")
    if col == 0:
        top.set_ylabel("events / round"); bot.set_ylabel("CUSUM statistic")
    bot.set_xlabel("round")
axes[1, 0].legend()
fig.suptitle("CUSUM watchdog on synthetic feed volume (grey = attack start, red = alarm)")
fig.tight_layout()
out = pathlib.Path(__file__).with_name("cusum_demo.png")
fig.savefig(out, dpi=130)
print("saved", out)