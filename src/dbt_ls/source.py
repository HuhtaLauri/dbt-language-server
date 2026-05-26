from dataclasses import dataclass
import yaml
from pathlib import Path

from dbt_ls.column import Column

@dataclass(frozen=True)
class SourceTable:
    name: str
    source_name: str
    database: str | None = None
    schema: str | None = None
    columns: tuple[Column, ...] = ()


def discover_sources(root: str) -> list:
    sources = []
    for p in Path(root).rglob("*.yml"):
        if "target" in p.parts or not p.is_file():
            continue
        doc = yaml.safe_load(p.read_text())
        if not doc or "sources" not in doc:
            continue
        for src in doc["sources"]:
            source_name = src.get("name", "")
            for table in src.get("tables", []):
                sources.append(SourceTable(
                    name=table["name"],
                    source_name=source_name,
                    database=src.get("database"),
                    schema=src.get("schema"),
                    columns=tuple([
                        Column(name=c["name"], data_type=c.get("data_type"))
                        for c in table.get("columns", [])
                    ]),
                ))
    return sources
