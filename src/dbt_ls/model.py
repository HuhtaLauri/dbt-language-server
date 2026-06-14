from dataclasses import dataclass
from pathlib import Path
from dbt_ls.column import Column
import json
from dbt_ls.profiles import ProfileTarget
import ibis
from ibis.expr.schema import Schema
from ibis.expr.types.relations import (
    Table,
)
from dbt_ls.profiles import DuckDBTarget, DatabaseTarget


@dataclass(frozen=True)
class Model:
    name: str
    path: str
    columns: tuple[Column, ...] = ()


def discover_models(root: str, model_paths: list[str]) -> list[Model]:
    return [
        Model(name=p.stem, path=str(p))
        for model_path in model_paths
        for p in (Path(root) / model_path).rglob("*.sql")
    ]


def enrich_models_from_catalog(models: list[Model], catalog_path: Path) -> list[Model]:
    path = Path(catalog_path)
    if not path.is_file():
        return models

    catalog = json.loads(path.read_text())
    nodes = catalog.get("nodes", {})

    # Build a lookup: model name -> columns
    columns_by_name: dict[str, tuple[Column, ...]] = {}
    for node in nodes.values():
        if not node.get("unique_id", "").startswith("model."):
            continue
        name = node["metadata"]["name"]
        columns_by_name[name] = tuple(
            Column(name=c["name"], data_type=c.get("type"))
            for c in node.get("columns", {}).values()
        )

    return [
        Model(name=m.name, path=m.path, columns=columns_by_name.get(m.name, m.columns))
        for m in models
    ]


def get_duckdb_models(
    models: list[Model], profile_target: DuckDBTarget, project_root: str | Path
) -> list[Model] | None:
    ibis.set_backend("duckdb")

    connection_path = (
        profile_target.path
        if Path(profile_target.path).is_absolute()
        else Path(project_root).joinpath(profile_target.path)
    )
    con = ibis.duckdb.connect(connection_path)

    con = ibis.duckdb.connect("myproject/" + profile_target.path)
    columns_by_name: dict[str, tuple[Column, ...]] = {}

    tables = con.list_tables()
    for t in tables:
        table: Table = con.table(t)
        schema: Schema = table.schema()

        columns_by_name[t] = tuple(
            Column(name=name, data_type=str(dtype)) for name, dtype in schema.items()
        )

    return [
        Model(name=m.name, path=m.path, columns=columns_by_name.get(m.name, ()))
        for m in models
    ]


def enrich_models_from_database(
    models: list[Model],
    profile_target: DuckDBTarget | DatabaseTarget,
    project_root: str | Path,
) -> list[Model] | None:
    match profile_target:
        case DuckDBTarget():
            return get_duckdb_models(models, profile_target, project_root)
        case _:
            return None
