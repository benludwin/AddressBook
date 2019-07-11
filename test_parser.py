import core_logic as cl
import sqlparser as sqlp

import pytest
import os
import tempfile
import flask


@pytest.fixture
def parser():
    sql_parser = sqlp.SqlParser("test.db")
    sql_parser.initialize()
    yield sql_parser
    os.remove("test.db")

def test_init(parser):
    assert parser._cursor

def test_createTable(parser):
    rv = parser.createTable("test_create")
    assert(rv)

def test_searchForTable_good(parser):
    parser.createTable("test_search")
    rv = parser.searchForTable("test_search")
    assert(rv)

def test_searchForTable_bad(parser):
    rv = parser.searchForTable("NOT_A_TABLE")
    assert not (rv)

def test_removeTable(parser):
    parser.createTable("test_remove")
    rv = parser.removeTable("test_remove")
    assert(rv)

def test_searchTable(parser):
    parser.createTable("test_search2")
    rv = parser.searchTable("test_search2", "SELECT * FROM test_search2")
    assert(rv)

def test_displayBooks(parser):
    parser.createTable("test_display")
    rv = parser.displayBooks()
    assert("test_display" in str(rv))

def test_saveBook_good(parser):
    parser.createTable("test_save")
    rv = parser.saveBook("test_save")
    assert(rv)

def test_saveBook_bad(parser):
    rv = parser.saveBook("NOT_A_TABLE2")
    assert not (rv)

def test_saveBookAs_good(parser):
    parser.createTable("test_saveas")
    rv = parser.saveBookAs("test_saveas", "test_saveas2")
    assert(rv)

def test_saveBookAs_bad(parser):
    rv = parser.saveBookAs("test_saveas2", "test_saveas3")
    assert not (rv)

def test_deleteBook(parser):
    parser.createTable("test_delete")
    rv1 = parser.searchForTable("test_delete")
    parser.deleteBook("test_delete")
    rv2 = parser.searchForTable("test_delete")
    assert (rv1 and not rv2)
