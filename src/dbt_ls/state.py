from dataclasses import dataclass, field

from dbt_ls.model import Model
from dbt_ls.project import Project
from dbt_ls.source import SourceTable


@dataclass
class ProjectState:
    """Discovered dbt project data shared across LSP handlers.

    Held on the language server instance instead of module-level globals so it
    can be rebuilt on reload and constructed in isolation for tests.
    """

    models: list[Model] = field(default_factory=list)
    sources: list[SourceTable] = field(default_factory=list)
    dbt_root: str = "."
    project: Project | None = None
