import pytest
from dbt_ls.profiles import (
    ProfileTarget,
    DuckDBTarget,
    MySQLTarget,
    Secret,
    DatabaseTarget,
    MSSQLTarget,
    SparkTarget,
    DatabricksTarget,
)


@pytest.mark.parametrize(
    "target_dict, expected",
    [
        pytest.param(
            {"type": "duckdb", "threads": 1, "path": "dev.duckdb"},
            DuckDBTarget(type="duckdb", threads=1, path="dev.duckdb"),
        ),
        pytest.param(
            {
                "type": "mysql",
                "threads": 4,
                "user": "root",
                "password": "passwd",
                "server": "127.0.0.1",
                "port": 1433,
                "schema": "dev",
            },
            MySQLTarget(
                type="mysql",
                threads=4,
                user="root",
                password=Secret("passwd"),
                server="127.0.0.1",
                port=1433,
                schema="dev",
            ),
        ),
        pytest.param(
            {
                "type": "postgres",
                "threads": 4,
                "user": "postgres",
                "password": "passwd",
                "host": "127.0.0.1",
                "port": 5432,
                "schema": "dev",
                "dbname": "mydb",
            },
            DatabaseTarget(
                type="postgres",
                threads=4,
                user="postgres",
                password=Secret("passwd"),
                host="127.0.0.1",
                port=5432,
                schema="dev",
                dbname="mydb",
            ),
        ),
        pytest.param(
            {
                "type": "sqlserver",
                "threads": 4,
                "user": "sa",
                "password": "root",
                "server": "127.0.0.1",
                "port": 1234,
                "schema": "dev",
                "database": "mydb",
                "driver": "{MSSQL DRIVER}",
                "encrypt": False,
            },
            MSSQLTarget(
                type="sqlserver",
                threads=4,
                user="sa",
                password=Secret("root"),
                server="127.0.0.1",
                port=1234,
                schema="dev",
                database="mydb",
                driver="{MSSQL DRIVER}",
                encrypt=False,
            ),
        ),
        pytest.param(
            {
                "type": "spark",
                "method": "session",
                "host": "localhost",
                "schema": "default",
            },
            SparkTarget(
                type="spark", method="session", host="localhost", schema="default"
            ),
        ),
        pytest.param(
            {
                "type": "databricks",
                "catalog": "mycatalog",
                "schema": "default",
                "host": "https://adb-23452935842.2.azuredatabricks.net",
                "http_path": "/sql/1.0/warehouses/29348rw7edf",
                "token": "mytoken",
                "threads": 1,
            },
            DatabricksTarget(
                type="databricks",
                catalog="mycatalog",
                schema="default",
                host="https://adb-23452935842.2.azuredatabricks.net",
                http_path="/sql/1.0/warehouses/29348rw7edf",
                token=Secret("mytoken"),
                threads=1,
            ),
        ),
        pytest.param(
            {
                "type": "databricks",
                "catalog": "mycatalog",
                "schema": "default",
                "host": "https://adb-23452935842.2.azuredatabricks.net",
                "http_path": "/sql/1.0/warehouses/29348rw7edf",
                "client_id": "clientid123",
                "client_secret": "clientsecret123",
                "threads": 1,
            },
            DatabricksTarget(
                type="databricks",
                catalog="mycatalog",
                schema="default",
                host="https://adb-23452935842.2.azuredatabricks.net",
                http_path="/sql/1.0/warehouses/29348rw7edf",
                client_id="clientid123",
                client_secret=Secret("clientsecret123"),
                threads=1,
            ),
        ),
    ],
    ids=[
        "duckdb",
        "mysql",
        "postgres",
        "sqlserver",
        "spark",
        "databrickstoken",
        "databricksoauth",
    ],
)
def test_target_from_dict(target_dict, expected):
    assert ProfileTarget.from_dict(target_dict) == expected
