import unittest

import numpy as np
from numpy.testing import assert_array_almost_equal

import feyn


class TestNormalizer(unittest.TestCase):
    
    # TODO: Explain why we default to this
    def test_default_normalization(self):
        normalizer = feyn.adapters.Normalizer()
        
        self.assertEqual(normalizer.feature_min, -1)
        self.assertEqual(normalizer.feature_max, 1)

    def test_can_normalize(self):
        normalizer = feyn.adapters.Normalizer(0, 4)
        normalized = normalizer._process_input(np.array([0, 1, 2, 3, 4]))
        
        assert_array_almost_equal(normalized, [-1,-.5,0,.5,1])

        denormalized = normalizer._process_output(normalized)
        assert_array_almost_equal(denormalized, [0, 1, 2, 3, 4])
