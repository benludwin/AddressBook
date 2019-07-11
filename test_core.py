
import core_logic as cl
import sqlparser as sqlp

import pytest
import os
import tempfile
import flask


@pytest.fixture
def client():
    db_fd, cl.app.config['DATABASE'] = tempfile.mkstemp()
    cl.app.config['TESTING'] = True
    client = cl.app.test_client()

    yield client

    os.close(db_fd)
    os.unlink(cl.app.config['DATABASE'])


def test_index(client):

    rv = client.get('/')
    assert isinstance(
        rv, flask.wrappers.Response) and b'Application landing page' in rv.data


def test_close(client):

    rv = client.get('/close')
    assert isinstance(
        rv, flask.wrappers.Response) and b'Close the application' in rv.data
    

def test_create(client):

    rv = client.get('/create')
    cl.createWithName("test")
    assert isinstance(
        rv, flask.wrappers.Response) and b'Create an address book' in rv.data


def test_error(client):

    rv = client.get('/error')
    assert isinstance(
        rv, flask.wrappers.Response) and b'Error page' in rv.data


def test_new_entry(client):

    rv = client.get('/entry/test')
    assert isinstance(
        rv, flask.wrappers.Response) and b'Add a new entry to the application' in rv.data


def test_update_entry(client):

    rv = client.get('/update/test')
    assert isinstance(
        rv, flask.wrappers.Response) and b'Update an existing entry in an address book' in rv.data


def test_view(client):

    rv = client.get('/view/test')
    assert isinstance(
        rv, flask.wrappers.Response) and b'Main table view' in rv.data


def test_view_books(client):

    rv = client.get('/open')
    assert isinstance(
        rv, flask.wrappers.Response) and b'View Address Book' in rv.data