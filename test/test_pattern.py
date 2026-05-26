import pytest
from src.dbt_ls.pattern import *


@pytest.mark.parametrize(
    "text, should_match",
    [
        ("ref('my_model", True),
        ('ref("my_model', True),
        ("ref('", True),
        ('ref("', True),
        ("ref(my_model", False),
        ("source('", False),
        ("hello world", False),
        ("", False),
    ],
)
def test_match_ref(text, should_match):
    result = ref_pattern(text)
    assert bool(result) == should_match

@pytest.mark.parametrize(
    "text, should_match",
    [
        ('source("', True),
        # ("source('src','my_table", True),
        # ('source("src","my_table', True),
        # ("source('src', 'my_table", True),
        # ("source('src',  '", True),
        # ("source('src','", True),
        # ("source('src')", False),       # no second arg started
        # ("source('", False),            # still in first arg
        ("source(src, tbl", False),     # no quotes
        ("ref('model", False),
        ("", False),
    ],
)
def test_match_source(text, should_match):
    result = source_pattern(text)
    assert bool(result) == should_match
