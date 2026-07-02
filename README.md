# DBT-Language-Server

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

