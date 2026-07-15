# DBT-Language-Server

<img alt="DBT Language Server" src="https://vhs.charm.sh/vhs-1IEY4fW47S53ZaFfI9ri8B.gif" />

## Features

| Feature | LSP method / command | Description |
| --- | --- | --- |
| Model completion | `textDocument/completion` | Suggests dbt models inside `ref('...')` |
| Source completion | `textDocument/completion` | Suggests sources inside `source('...')`, auto-inserting the `source_name`, `table` pair   |
| Column completion | `textDocument/completion` | Suggests columns for an aliased model/source (`alias.<column>`), with the column's data type shown as a detail. |
| Go to definition | `textDocument/definition` | Jumps from `ref('model')` to that model's `.sql` file. |
| Database enrichment | on `initialize` | Reads column names and data types for models directly from the connected warehouse. |
| Catalog enrichment | on `initialize` | Reads source column info from `target/catalog.json` when available. |
| Profile resolution | on `initialize` | Locates the dbt profile, resolves the active target    |
| Auto project discovery | on `initialize` | Finds the dbt project root by locating `dbt_project.yml` (ignoring `target/`). |
| Project reload | `dbt-ls.reload` command | Re-discovers models, sources, and re-runs enrichment without restarting the server. |
| Current model info | `dbt-ls.current_model` command | Returns the dbt project root and the model's execution path for the current file. (Can be used to run models)   |


## Installation
~~~sh
uv tool install dbt-ls
~~~

## Configuration
~~~lua
vim.lsp.config("dbt_ls", {
    cmd = { "dbt-ls" },
    filetypes = { "sql" },
    root_markers = { "dbt_project.yml" },
})
vim.lsp.enable("dbt_ls")

~~~

## Supported backends
- DuckDB
- SQL Server / MSSQL
- PostgreSQL
- MySQL
- Spark (Spark Connect, no auth)
- Databricks
- Athena
- Glue

> [!IMPORTANT]
> Databricks supports two auth methods, resolved from your dbt profile:
>
> - **Personal access token** — set `token` in the target.
> - **Service principal OAuth (M2M)** — set `client_id` and `client_secret` in the target. Used automatically when no `token` is present.

Install each version with 
~~~sh
uv tool install dbt-ls[duckdb]
~~~
or all supported backends with
~~~sh
uv tool install dbt-ls[all]
~~~

