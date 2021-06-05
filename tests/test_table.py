from src.database.datatypes import Datatype
from src.database.table import Table
import unittest


class TableTest(unittest.TestCase):
    def test_cols_num(self):
        tab = Table("name")

        self.assertTrue(tab.cols_num() == 0)

        tab.add_column(("col1", Datatype.ITEGER))

        self.assertTrue(tab.cols_num() == 1)

        tab.add_column(("col2", Datatype.ITEGER))

        self.assertTrue(tab.cols_num() == 2)

    def test_rows_num(self):
        tab = Table("name")
        tab.add_column(("col1", Datatype.ITEGER))

        self.assertEqual(tab.rows_num(), 0, "Rows amount should be 0 but is not")

        tab.add_row(["1"])

        self.assertEqual(tab.rows_num(), 1, "Rows amount should be 1 but is not")

        tab.add_row(["1"])

        self.assertEqual(tab.rows_num(), 2, "Rows amount should be 2 but is not")


if __name__ == "__main__":
    unittest.main()

