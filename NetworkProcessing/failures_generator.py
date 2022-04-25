import numpy as np

EXPONENTIAL_DISTRIBUTION = "exponential"
WEIBULL_DISTRIBUTION = "weibull"


class FailuresGenerator:

    all_distributions = {
        EXPONENTIAL_DISTRIBUTION: np.random.exponential,
        WEIBULL_DISTRIBUTION: np.random.weibull,
    }

    def __init__(
        self,
        trials: int = 1,
        failures_intensity: float = 10e-5,
        distribution: str = EXPONENTIAL_DISTRIBUTION,
    ):
        self.intensity = failures_intensity
        self.trials = trials
        self.distribution = self.all_distributions[distribution]

    def conduct_test(self) -> np.array:
        return np.random.rand(self.trials) < self.distribution(
            1.0 / self.intensity, size=self.trials
        )
