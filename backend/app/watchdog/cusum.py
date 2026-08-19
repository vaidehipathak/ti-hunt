"""
CUSUM (Cumulative Sum) change-point detection.
Layer 2 — detects sudden, sustained shifts in a source's behavior
(e.g. alert volume spike, or a sharp drop in trust score), independent
of the slower-learning EXP3 bandit.
"""

class CUSUMWatchdog:
    def __init__(self, k: float = 0.5, h: float = 5.0):
        """
        k: reference/slack value (how much deviation to tolerate before it counts)
        h: decision threshold (how much cumulative deviation triggers an alarm)
        """
        self.k = k
        self.h = h
        # per-source running cumulative sums
        self.pos_cusum: dict[str, float] = {}
        self.neg_cusum: dict[str, float] = {}
        self.baseline: dict[str, float] = {}

    def set_baseline(self, source_name: str, value: float):
        self.baseline[source_name] = value
        self.pos_cusum[source_name] = 0.0
        self.neg_cusum[source_name] = 0.0

    def update(self, source_name: str, value: float) -> bool:
        """
        Feed a new observation (e.g. current trust score, or volume).
        Returns True if an anomalous shift is detected (should throttle).
        """
        if source_name not in self.baseline:
            self.set_baseline(source_name, value)
            return False

        mean = self.baseline[source_name]
        deviation = value - mean

        # positive CUSUM catches sudden increases (e.g. volume spike)
        self.pos_cusum[source_name] = max(
            0.0, self.pos_cusum[source_name] + deviation - self.k
        )
        # negative CUSUM catches sudden decreases (e.g. trust collapse)
        self.neg_cusum[source_name] = max(
            0.0, self.neg_cusum[source_name] - deviation - self.k
        )

        anomalous = (
            self.pos_cusum[source_name] > self.h
            or self.neg_cusum[source_name] > self.h
        )

        if anomalous:
            # reset after triggering so it can detect the next shift
            self.pos_cusum[source_name] = 0.0
            self.neg_cusum[source_name] = 0.0
            self.baseline[source_name] = value

        return anomalous