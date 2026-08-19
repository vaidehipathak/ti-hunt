"""
Real EXP3 (Exponential-weight algorithm for Exploration and Exploitation).

Each CTI source is treated as an "arm". Weight updates use the
importance-weighted reward estimator, which is what makes EXP3 robust
to adversarial (non-stationary) reward sequences.
"""

import math


class EXP3:
    def __init__(self, gamma: float = 0.1):
        """
        gamma: exploration rate (0 < gamma <= 1).
        Higher gamma = more exploration of low-trust sources.
        """
        self.gamma = gamma

    def get_probability(self, weight: float, total_weight: float, n_sources: int) -> float:
        """
        Convert a source's raw weight into a trust probability.
        p_i = (1 - gamma) * (w_i / sum(w)) + gamma / n_sources
        """
        if total_weight <= 0 or n_sources == 0:
            return 1.0 / max(n_sources, 1)
        exploit_term = (1 - self.gamma) * (weight / total_weight)
        explore_term = self.gamma / n_sources
        return exploit_term + explore_term

    def update_weight(self, weight: float, probability: float,
                       reward: float, n_sources: int) -> float:
        """
        Importance-weighted update.
        reward: 1.0 for true positive, 0.0 for false positive.
        estimated_reward = reward / probability   (importance weighting)
        w_i_new = w_i * exp(gamma * estimated_reward / n_sources)
        """
        if probability <= 0:
            probability = 1e-6
        estimated_reward = reward / probability
        new_weight = weight * math.exp(
            (self.gamma * estimated_reward) / n_sources
        )
        # clip to avoid numerical blowup
        return min(new_weight, 1e6)