from pygls.lsp.server import LanguageServer
from lsprotocol import types
from importlib.metadata import version
from dbt_ls.pattern import ref_pattern, source_pattern
from dbt_ls.model import discover_models
from dbt_ls.source import discover_sources

__version__ = version("dbt-ls")

server = LanguageServer("dbt-ls", __version__)


@server.feature(types.INITIALIZE)
def on_initialize(params: types.InitializeParams):
    global models
    global sources
    if params.root_path:
        models = discover_models(params.root_path)
        sources = discover_sources(params.root_path)


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
                label_details=types.CompletionItemLabelDetails(s.source_name), # s.database
                insert_text=f'{s.source_name}", "{s.name}', # Works only perfect with autocomplete, Fix later
                insert_text_format=types.InsertTextFormat.PlainText,
            )
            for s in sources
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
