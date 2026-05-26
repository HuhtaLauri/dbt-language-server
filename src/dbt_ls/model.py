from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Model:
    name: str
    path: str | None = None


def discover_models(root: str) -> list[Model]:
    return [
        Model(name=p.stem, path=str(p))
        for p in Path(root).rglob("*.sql")
        if "target" not in p.parts
    ]
