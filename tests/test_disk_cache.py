import os
import time
import pytest
from datetime import datetime, timedelta
from disk_cache import disk_cache, clear_cache

# Set up a temporary cache folder for testing
TEST_CACHE_FOLDER = "test_cache"
os.makedirs(TEST_CACHE_FOLDER, exist_ok=True)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Code to run before each test
    clear_cache()
    yield
    # Code to run after each test
    clear_cache()

def test_disk_cache_decorator():
    @disk_cache(seconds=2, cache_folder=TEST_CACHE_FOLDER)
    def add(a, b):
        return a + b

    result1 = add(1, 2)
    result2 = add(1, 2)
    assert result1 == result2

    # Check if the result is cached by comparing modification times
    cache_file = os.path.join(TEST_CACHE_FOLDER, os.listdir(TEST_CACHE_FOLDER)[0])
    mod_time1 = os.path.getmtime(cache_file)

    time.sleep(1)
    result3 = add(1, 2)
    mod_time2 = os.path.getmtime(cache_file)
    assert result1 == result3
    assert mod_time1 == mod_time2  # Ensure the cache file was not modified

    # Modify the cache file to simulate expiration
    time.sleep(2)
    result4 = add(1, 2)
    mod_time3 = os.path.getmtime(cache_file)
    assert result1 == result4
    assert mod_time1 != mod_time3  # Ensure the cache file was modified

def test_clear_cache():
    @disk_cache(seconds=3600, cache_folder=TEST_CACHE_FOLDER)
    def add(a, b):
        return a + b

    add(1, 2)
    assert len(os.listdir(TEST_CACHE_FOLDER)) > 0

    clear_cache(cache_folder=TEST_CACHE_FOLDER)
    assert len(os.listdir(TEST_CACHE_FOLDER)) == 0

def test_cache_with_different_arg_types():
    @disk_cache(seconds=3600, cache_folder=TEST_CACHE_FOLDER)
    def concat_strings(a, b):
        return a + b

    result1 = concat_strings("hello", "world")
    result2 = concat_strings("hello", "world")
    assert result1 == result2

    @disk_cache(seconds=3600, cache_folder=TEST_CACHE_FOLDER)
    def multiply_list(lst, times):
        return lst * times

    result3 = multiply_list([1, 2, 3], 2)
    result4 = multiply_list([1, 2, 3], 2)
    assert result3 == result4

    @disk_cache(seconds=3600, cache_folder=TEST_CACHE_FOLDER)
    def combine_dicts(dict1, dict2):
        return {**dict1, **dict2}

    result5 = combine_dicts({"a": 1}, {"b": 2})
    result6 = combine_dicts({"a": 1}, {"b": 2})
    assert result5 == result6

    @disk_cache(seconds=3600, cache_folder=TEST_CACHE_FOLDER)
    def sum_set(s):
        return sum(s)

    result7 = sum_set({1, 2, 3})
    result8 = sum_set({1, 2, 3})
    assert result7 == result8

    @disk_cache(seconds=3600, cache_folder=TEST_CACHE_FOLDER)
    def join_tuple(t):
        return ''.join(t)

    result9 = join_tuple(('a', 'b', 'c'))
    result10 = join_tuple(('a', 'b', 'c'))
    assert result9 == result10

    @disk_cache(seconds=3600, cache_folder=TEST_CACHE_FOLDER)
    def identity(x):
        return x

    result11 = identity(42)
    result12 = identity(42)
    assert result11 == result12

    result13 = identity(3.14)
    result14 = identity(3.14)
    assert result13 == result14

    @disk_cache(seconds=3600, cache_folder=TEST_CACHE_FOLDER)
    def add_days_to_date(date, days):
        return date + timedelta(days=days)

    date = datetime(2023, 1, 1)
    result15 = add_days_to_date(date, 10)
    result16 = add_days_to_date(date, 10)
    assert result15 == result16
