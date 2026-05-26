from pygls.lsp.server import LanguageServer
from lsprotocol import types
from importlib.metadata import version
from dbt_ls.pattern import ref_pattern, source_pattern, column_pattern
from dbt_ls.model import discover_models, enrich_models_from_catalog
from dbt_ls.source import discover_sources
from pathlib import Path
from dbt_ls.alias import parse_aliases

__version__ = version("dbt-ls")

server = LanguageServer("dbt-ls", __version__)

def find_dbt_project_root(root: str) -> str | None:
    for p in Path(root).rglob("dbt_project.yml"):
        if "target" not in p.parts:
            return str(p.parent)
    return None


@server.feature(types.INITIALIZE)
def on_initialize(params: types.InitializeParams):
    global models
    global sources
    global dbt_root
    if params.root_path:
        dbt_root = find_dbt_project_root(params.root_path)
        catalog_path = Path(f"{dbt_root}/target/catalog.json")
        models = discover_models(params.root_path)
        sources = discover_sources(params.root_path)
        models = enrich_models_from_catalog(models, catalog_path)


@server.feature(
    types.TEXT_DOCUMENT_COMPLETION,
    types.CompletionOptions(trigger_characters=[".", '"']),
)
def completions(params: types.CompletionParams):
    document = server.workspace.get_text_document(params.text_document.uri)
    current_line = document.lines[params.position.line].strip()

    if current_line.endswith('ref("")') or ref_pattern(current_line):
        return [
            types.CompletionItem(
                m.name,
                kind=types.CompletionItemKind(18),
                label_details=types.CompletionItemLabelDetails(m.path),
            )
            for m in models
        ]
    elif current_line.endswith('source("")') or source_pattern(current_line):
        return [
            types.CompletionItem(
                s.name,
                kind=types.CompletionItemKind(10),
                label_details=types.CompletionItemLabelDetails(s.database),
                insert_text=f'{s.source_name}", "{s.name}', # Works only perfect with autocomplete, Fix later
                insert_text_format=types.InsertTextFormat.PlainText,
            )
            for s in sources
        ]
    elif column_pattern(str.strip(current_line)):
        # server.window_show_message(types.ShowMessageParams(type=types.MessageType(3), message=f"models with columns: {[(m.name, len(m.columns)) for m in models]}"))
        match = column_pattern(current_line)
        alias = match.group(0).split(".")[0]
        full_text = document.source
        alias_map = parse_aliases(full_text)
        model_name = alias_map.get(alias)
        return [
            types.CompletionItem(
                label=c.name,
                kind=types.CompletionItemKind(5),
                label_details=types.CompletionItemLabelDetails(c.data_type),
                )
            for m in models
            for c in m.columns
            if m.name == model_name
        ]
    else:
        return []


def main():
    banner = f"""
   ╔═══════════════════════════════════════╗
   ║                                       ║
   ║      _ _     _        _               ║
   ║   __| | |__ | |_     | |___           ║
   ║  / _` | '_ \\| __|____| / __|          ║
   ║ | (_| | |_) | ||_____| \\__ \\          ║
   ║  \\__,_|_.__/ \\__|    |_|___/          ║
   ║                                       ║
   ║   {__version__:^5} · Language Server · stdio     ║
   ║                                       ║
   ╚═══════════════════════════════════════╝
    """
    print(banner)
    server.start_io()


if __name__ == "__main__":
    main()
