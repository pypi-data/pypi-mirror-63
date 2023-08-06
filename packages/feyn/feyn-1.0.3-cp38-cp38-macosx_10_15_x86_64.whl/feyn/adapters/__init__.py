class Normalizer:
    """
    Transforms features by scaling each feature from a given range into -1 and 1.

    The implementation follows:
    https://en.wikipedia.org/wiki/Feature_scaling#Rescaling_(min-max_normalization)
    """
    def __init__(self, feature_min =-1, feature_max=1):
        self.feature_min = feature_min
        self.feature_max = feature_max

    def _process_input(self, inputs):
        return -1 + ((inputs - self.feature_min) * 2) / (self.feature_max-self.feature_min)

    def _process_output(self, outputs):
        return self.feature_min + (( outputs +1) * (self.feature_max-self.feature_min)) / 2

__all__ = [
    'Normalizer',
]
