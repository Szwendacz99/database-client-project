import logging

from src.database.table import Table
from src.exceptions import TableExistsException, ClientException

log = logging.getLogger(__name__)


class Database:

    def __init__(self):
        self.tables = {}

    def list_tables_names(self) -> list:
        return [name for name in self.tables]

    def add_table(self, table: Table):
        if self.tables.get(table.name) is not None:
            raise TableExistsException(table.name)
        self.tables[table.name] = table
        log.info(f"added new table \"{table.name}\"")

    def drop_table(self, name: str) -> None:
        if self.tables.get(name) is None:
            raise ClientException(f"Cannot delete table with name {name} that do not exists lol")
        self.tables.pop(name)
        log.info(f"deleted table \"{name}\"")

    def get_table(self, name: str) -> Table:
        if self.tables.get(name) is None:
            raise ClientException(f"Cannot get table with name {name} that do not exists lol")
        return self.tables.get(name)
