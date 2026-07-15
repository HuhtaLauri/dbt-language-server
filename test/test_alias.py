import pytest

from dbt_ls.alias import parse_aliases


@pytest.mark.parametrize(
    "text, expected",
    [
        ("{{ ref('accounts') }} a", {"a": "accounts"}),
        ('{{ ref("orders") }} o', {"o": "orders"}),
        ("{{ source('src', 'my_table') }} t", {"t": "my_table"}),
        (
            "{{ ref('accounts') }} a join {{ ref('orders') }} o",
            {"a": "accounts", "o": "orders"},
        ),
        ("select 1", {}),
        ("{{ ref('accounts') }} as a", {"a": "accounts"}),
        (
            "{{ ref('accounts') }} AS a join {{ ref('orders') }} o",
            {"a": "accounts", "o": "orders"},
        ),
        ("{{ source('src', 'my_table') }} as t", {"t": "my_table"}),
        (
            "{{ source('src', 'accounts') }} AS a join {{ ref('orders') }} o",
            {"a": "accounts", "o": "orders"},
        ),
        (
            """
        SELECT
            *
        FROM {{ ref('orders') }} o
         """,
            {"o": "orders"},
        ),
    ],
)
def test_parse_aliases(text, expected):
    assert parse_aliases(text) == expected
