import time
import unittest

from utils_future import file_cache


class TestFileCache(unittest.TestCase):
    def test_file_cache(self):
        big_num = 1_000_000_000
        def slow_function(n):
            s = 0
            for i in range(n):
                s += i
            return s

        @file_cache
        def file_cached_slow_function(big_num):
            return slow_function(big_num)

        t = time.time()
        r1 = slow_function(big_num)
        dt1 = time.time() - t

        file_cached_slow_function()
        
        t = time.time()
        r2 = file_cached_slow_function(big_num)
        dt2 = time.time() - t

        self.assertEqual(r1, r2)
        self.assertGreaterEqual(dt1, dt2)
