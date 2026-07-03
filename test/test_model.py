from src.dbt_ls.model import discover_models, Model
from pathlib import Path


def test_discover_models():
    models = discover_models("testdata/project", ["models"])
    assert set(models) == {
        Model(
            name="my_first_dbt_model",
            path=Path("testdata/project/models/example/my_first_dbt_model.sql"),
        ),
        Model(
            name="my_second_dbt_model",
            path=Path("testdata/project/models/example/my_second_dbt_model.sql"),
        ),
    }
