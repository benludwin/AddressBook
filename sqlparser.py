'''
SQL parser that interacts with our database

AUTHOR: Christopher Jens Johnson
UPDATE (10/10): Basic framework and functionality implemented, more to come...
'''

import sqlite3, datetime, pandas as pd  # SQL for interfacing with the database, datetime for logging, and pandas for dataframes
from enum import Enum                   # For enumerating our SQL commands
from shutil import copy2                # For data replication on startup

class Commmands(Enum):
    '''
    SQL Commands to interface with sqlite3.
    These are parameterized for the parser to take user commands.
    '''
    SEARCH = "SELECT name FROM sqlite_master WHERE type='table' AND name='{}';"
    DROP = "DROP TABLE IF EXISTS {};"
    CREATE = "CREATE TABLE {} (firstName tinytext, lastName tinytext, phone char(10), email tinytext, address tinytext, state varchar(13), zip char(5));"
    TABLES = "SELECT name FROM sqlite_master WHERE type='table';"
    INSERT = "INSERT INTO {} (firstName, lastName, phone, email, address, state, zip) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}');"
    UPDATE = "UPDATE {} SET firstName='{}', lastName='{}', phone='{}', email='{}', address='{}', state='{}', zip='{}' WHERE firstName='{}' AND lastName='{}' AND phone='{}' AND email='{}' AND address='{}' AND state='{}' AND zip='{}';"
    DELETE = "DELETE FROM {} WHERE firstName='{}' AND lastName='{}' AND phone='{}' AND email='{}' AND address='{}' AND state='{}' AND zip='{}';"

class SqlParser:
    def __init__(self, db):
        '''
        Initialize the book. We set up logging capabilities, and set up connections to a primary store, and our temporary store,
        which allows the user to save data when needed.
        '''
        self._db = db
        self._connection = None
        self._primaryStore = sqlite3.connect('addressbook.db', check_same_thread=False)
        self._primaryStoreCursor = self._primaryStore.cursor()
        self._cursor = None
        self._errLog = open('logs/error.log', 'w')
        self._appLog = open('logs/application.log', 'w')

    def initialize(self):
        '''
        Replicates the current address data to our temporary connection, and establishes a cursor to the temporary database.
        '''
        copy2("addressbook.db", "temp.db")
        self._connection = sqlite3.connect(self._db, check_same_thread=False)
        self._cursor = self._connection.cursor()
        self._appLog.write(str(datetime.datetime.now())+" [Application]: Established database connection to '{}'\n".format(self._db))
    
    def searchForTable(self, table):
        '''
        Auxilary function to search the database for a given table

        Returns:
            True if the table exists in the database
            False otherwise
        '''
        self._cursor.execute(Commmands.SEARCH.value.format(table))
        if self._cursor.fetchone() == None:
            self._appLog.write(str(datetime.datetime.now())+" [Application]: Table '{}' not found in '{}'.\n".format(table, self._db))
            return False
        else:
            self._appLog.write(str(datetime.datetime.now())+" [Application]: Table '{}' found in '{}'.\n".format(table, self._db))
            return True

    def createTable(self, table):
        '''
        Creates a table (i.e. address book) in the database

        Returns:
            True if the name is available and it was able to successfully create the table
            False otherwise
        '''
        if self.searchForTable(table):
            self._errLog.write(str(datetime.datetime.now())+" [Application]: Error - Cannot create table '{}'. Already exists in '{}'.\n".format(table, self._db))
            return False
        else:
            self._cursor.execute(Commmands.CREATE.value.format(table))
            self._appLog.write(str(datetime.datetime.now())+" [Application]: Table '{}' successfully created in '{}'.\n".format(table, self._db))
            return True

    def removeTable(self, table):
        '''
        Remove a table (i.e. address book) from the database

        Returns:
            True if the table existed in the database and was successfully removed
            False otherwise
        '''
        if self.searchForTable(table):
            self._cursor.execute(Commmands.DROP.value.format(table))
            self._appLog.write(str(datetime.datetime.now())+" [Application]: Table '{}' successfully dropped from '{}'.\n".format(table, self._db))
            return True
        else:
            self._errLog.write(str(datetime.datetime.now())+" [Application]: No such table '{}' exists in '{}'. Failed to remove table.\n".format(table, self._db))
            return False

    def searchTable(self, table, query):
        '''
        Searches a table with the given query (not parameterized)

        Returns
            True with a payload (panda dataframe) of the results if the table exists and the query was successful
            False otherwise
        '''
        if self.searchForTable(table):
            self._appLog.write(str(datetime.datetime.now())+" [Application]: Querying table '{}' in '{}'.\n".format(table, self._db))
            df = pd.read_sql_query(query, self._connection)
            return True, df
        else:
            self._errLog.write(str(datetime.datetime.now())+" [Application]: No such table '{}' exists in '{}'. Failed to execute query.\n".format(table, self._db))
            return False, None

    def displayBooks(self):
        '''
        Displays all books in the database.

        Returns:
            The dataframe containing the names of all of the books (which may be empty)
        '''
        self._appLog.write(str(datetime.datetime.now())+" [Application]: Retrieving all address books in the database '{}'\n".format(self._db))
        df = pd.read_sql_query(Commmands.TABLES.value, self._connection)
        return df
    
    def insertEntry(self, table, values):
        '''
        Insert an entry into the a book in the database

        Values is an array of the values: [firstName, lastName, phone, email, address, state, zip]
        '''
        self._appLog.write(str(datetime.datetime.now())+" [Application]: Inserting entry into the address book '{}'\n".format(table))
        self._cursor.execute(Commmands.INSERT.value.format(table, *values))
        self._connection.commit()
    
    def updateEntry(self, table, values):
        '''
        Updates an entry in a book in the database using its given parameters.

        Values is an array of the values: [firstName, lastName, phone, email, address, state, zip]

        Note: This operation will not be reflected in the primary store unless the book is saved.
        '''
        self._appLog.write(str(datetime.datetime.now())+" [Application]: Updating entry with in the address book '{}'\n".format(table))
        self._cursor.execute(Commmands.UPDATE.value.format(table, *values))
        self._connection.commit()
    
    def deleteEntry(self, table, values):
        '''
        Deletes an entry in the address book given its values.

        Note: This operation will not be reflected in the primary store unless the book is saved.
        '''
        self._appLog.write(str(datetime.datetime.now())+" [Application]: Deleting entry in the address book '{}'\n".format(table))
        self._cursor.execute(Commmands.DELETE.value.format(table, *values))
        self._connection.commit()
    
    def saveBook(self, table):
        '''
        Saves a book to the primary store with its given name.
        Replicates temporary data to a dataframe, and loads this into the primary store (replacing the table's current values if it exists)

        Returns:
            True if the book was found and the application was able to successfully save it to the primary store
            False if else
        '''
        self._appLog.write(str(datetime.datetime.now())+" [Application]: Saving address book with name '{}' to primary store\n".format(table))
        found, contacts_df = self.searchTable(table, "SELECT * FROM {};".format(table))
        if not found:
            return False
        else:
            contacts_df.to_sql(table, con=self._primaryStore, if_exists='replace')
            return True
    
    def saveBookAs(self, oldTable, newTable):
        '''
        Saves a book to the primary store with its given new name

        Note: This operation works as many other file i/o applications in the sense that it replicates the books contents (i.e. it does not rename the original book)

        Returns:
            True if the book was found and the application was able to successfully save it to the primary store
            False if else
        '''
        self._appLog.write(str(datetime.datetime.now())+" [Application]: Saving address book with name '{}' as '{}' to primary store\n".format(oldTable, newTable))
        found, contacts_df = self.searchTable(oldTable, "SELECT * FROM {};".format(oldTable))
        if not found:
            return False
        else:
            contacts_df.to_sql(newTable, con=self._connection, if_exists='replace')
            contacts_df.to_sql(newTable, con=self._primaryStore, if_exists='replace')
            return True
    
    def deleteBook(self, table):
        '''
        Deletes a book from the database.

        Note: This application also deletes the book from the primary store if it exists.
        '''
        self._appLog.write(str(datetime.datetime.now())+" [Application]: Removing book with name '{}' from temporary connection and primary store.\n".format(table))
        self._cursor.execute(Commmands.DROP.value.format(table))
        self._primaryStoreCursor.execute(Commmands.DROP.value.format(table))
