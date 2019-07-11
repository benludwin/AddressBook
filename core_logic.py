'''
Core logic for server

AUTHOR: Christopher Jens Johnson
UPDATE (10/10): This is being modularized, mode of the logic is in sql-parser.py for now
'''

import sqlite3, datetime                                      # SQLite3 for sql interfacing, datetime for logging
import sqlparser                                              # Parser class instance
from flask import Flask, render_template, redirect, request   # Flask tools

# Our startup routine (this initializes the server and sql parser)
app = Flask(__name__)                   # Our flask app
parser = sqlparser.SqlParser("temp.db") # Establish a temporary data connection
parser.initialize()                     # Initialize the parser

# Index page (aka landing/home page)
@app.route('/')
def index():
    return render_template("index.html")

# Create a new address book
@app.route('/create')
@app.route('/create/retry/<name>')
def create(name=None):
    parser._appLog.write(str(datetime.datetime.now())+" [Application]: Fulfilling user request to create new book.\n")
    return render_template("create.html", name=name)

# Creates a new address book with name <name>, redirects to the view page for that book
@app.route('/create/<name>')
def createWithName(name=None):
    if parser.createTable(name):
        parser._appLog.write(str(datetime.datetime.now())+" [Application]: Request recieved from page to create new address book- '{}'.\n".format(name))
        return redirect("view/"+name)
    else:
        return redirect("create/retry/"+name)

# Lists all address books (if any) in the database, with the option to open, delete, or create one
@app.route('/open')
def displayBooks(books=None):
    parser._appLog.write(str(datetime.datetime.now())+" [Application]: Request recieved from page to display all address books.\n")
    books_df = parser.displayBooks()
    return render_template("viewBooks.html", books=books_df)


# View the contents of an address book (if the book doesn't exist, return error)
@app.route('/view/<name>')
def viewBook(name=None, sortedQuery=None):
    parser._appLog.write(str(datetime.datetime.now())+" [Application]: Request recieved from page to display contents of address book '{}'.\n".format(name))
    searchValue = request.args.get('searchValue')

    # If we have a search parameter, say 'dog', query the address book, searching each field that was selected, to search for that value
    if searchValue:
        query = "SELECT * FROM {} WHERE ".format(name)
        for param in request.args.get('params').split(','):
            query += param + " LIKE '%{}%' OR ".format(searchValue)
        query = query[:-4] + ";"
        parser._appLog.write(str(datetime.datetime.now())+" [Application]: Request recieved to query book '{}' with value '{}'.\n".format(name, searchValue))
        found, contacts_df = parser.searchTable(name, query)
    
    # If the user selects a field to sort, view the book as sorted by the specified field, either ascending or descending
    elif (request.args.get('sorted') == 'true'):
        parser._appLog.write(str(datetime.datetime.now())+" [Application]: Request recieved to query sorted order of book '{}'.\n".format(name))
        found, contacts_df = parser.searchTable(name, "SELECT * FROM {} ORDER BY {} {};".format(name, request.args.get('field'), request.args.get('order')))
    
    # If the user doesn't specify a sort or search param, simply select all from the book.
    else:
        found, contacts_df = parser.searchTable(name, "SELECT * FROM {};".format(name))
    
    # If we can't find the book, return error (this SHOULD NOT happen, but its always better to be safe than sorry :))
    if not found:
        parser._errLog.write(str(datetime.datetime.now())+" [Application]: Error - Could not display contents of book - '{}'. None such book exists.\n".format(name))
        return redirect("/error")
    return render_template("view.html", book=name, contacts=contacts_df)


# View the contents of an address book (sorted)
@app.route('/viewSorted/<name>/<column>/<order>')
def viewSorted(name=None, column=None, order=None):
    return redirect('/view/{}?sorted=true&field={}&order={}'.format(name, column, order))


# Error page (this should never be hit, but better safe than sorry)
@app.route('/error')
def error():
    return render_template("error.html")


# Adding a new entry
@app.route('/entry/<name>', methods=['POST', 'GET'])
def entry(name=None):

    # If the user fills out the form for a new entry for a given table (i.e. HTTP POST request), use the parser to create a new entry in the table
    if request.method == 'POST':
        parser._appLog.write(str(datetime.datetime.now())+" [Application]: Inserting entry into '{}' with first name '{}'.\n".format(name, str(request.form['firstNameEntry'])))
        parser.insertEntry(name, [str(request.form['firstNameEntry']), str(request.form['lastNameEntry']), str(request.form['phoneNumberEntry']), str(request.form['emailEntry']), str(request.form['addressEntry']), str(request.form['stateEntry']), str(request.form['zipEntry'])])
        return redirect('/view/'+name)
    
    # If the user is requesting to create a new entry (i.e. get request), then route them to the new entry form
    else:
        parser._appLog.write(str(datetime.datetime.now())+" [Application]: Writing to address book '{}'.\n".format(name))
        return render_template("newEntry.html", book=name)


# Update an existing entry. Uses parameterized query to pre-fill out form.
@app.route('/update/<name>')
def update(name=None):
    parser._appLog.write(str(datetime.datetime.now())+" [Application]: Updating entry in address book '{}'.\n".format(name))
    firstName = request.args.get('firstName')
    lastName = request.args.get('lastName')
    phone = request.args.get('phone')
    email = request.args.get('email')
    address = request.args.get('address')
    state = request.args.get('state')
    zipCode = request.args.get('zip')
    return render_template("update.html", book=name, firstName=firstName, lastName=lastName, phone=phone, email=email, address=address, state=state, zip=zipCode)

# POST request sent after existing entry is updated. Uses old values to replace an entry with new values.
@app.route('/update/<name>/<values>', methods=['POST'])
def submitUpdate(name=None, values=None):
    updateParams = [str(request.form['firstNameEntry']), str(request.form['lastNameEntry']), str(request.form['phoneNumberEntry']), str(request.form['emailEntry']), str(request.form['addressEntry']), str(request.form['stateEntry']), str(request.form['zipEntry'])]
    for param in values.split(','):
        updateParams.append(param)
    parser._appLog.write(str(datetime.datetime.now())+" [Application]: Request recieved to update entry in book '{}'.\n".format(name))
    parser.updateEntry(name, updateParams)
    return redirect('view/'+name)

# Delete an entry in a book with the given values.
@app.route('/delete/<name>/<values>')
def delete(name=None, values=None):
    parser._appLog.write(str(datetime.datetime.now())+" [Application]: Request recieved from page to delete an entry in the book- '{}'.\n".format(name))
    valuesList = values.split(',')
    parser.deleteEntry(name, valuesList)
    return redirect('view/'+name)

# Save a book with the given name (route to error if SQL failure)
@app.route('/save/<name>')
def save(name=None):
    if parser.saveBook(name):
        return redirect('view/'+name)
    else:
        return redirect('/error')

# Save a book with a new given name (route to error if SQL failure)
@app.route('/save/<old>/<new>')
def saveAs(old=None, new=None):
    if parser.saveBookAs(old, new):
        return redirect('view/'+new)
    else:
        return redirect('/error')

# Delete a book, routing back to main after completion
@app.route('/delete/<name>')
def deleteBook(name=None):
    parser._appLog.write(str(datetime.datetime.now())+" [Application]: Request recieved from page to delete address book '{}'.\n".format(name))
    parser.deleteBook(name)
    return redirect('/open')

# Search a book given a query, send from the view page's search box via POST request
@app.route('/search/<name>', methods=['POST'])
def searchBook(name=None):
    searchParams = set([
        ('firstName', request.form.get('searchFirstName')),
        ('lastName', request.form.get('searchLastName')),
        ('email', request.form.get('searchEmail')),
        ('phone', request.form.get('searchPhone')),
        ('address', request.form.get('searchAddress')),
        ('state', request.form.get('searchState')),
        ('zip', request.form.get('searchZip'))
    ])
    query = "?searchValue="+request.form.get('searchEntry')+"&params="
    subquery = ""
    for param in searchParams:
        if param[1] != None:
            if subquery == "": subquery += param[0]
            else: subquery += ',' + param[0]
    
    # Build a subquery given search params that were selected via the search checkboxes, add this to the query if any were
    if subquery != "":
        query += subquery
    
    # If no query params are entered to search through, we will simply use the default fields of first and last names for the search term
    else:
        query += "firstName,lastName"
    return redirect('view/'+name+query)

# Close the application, sends the user to a confirmation page.
@app.route('/close')
def closeConfirmation():
    return render_template("close.html")

# Shutdown protocol
@app.route('/shutdown')
def shutdown():
    protocol = request.environ.get('werkzeug.server.shutdown')
    if protocol is None:
        return redirect('/error')
    protocol()
    return render_template('goodbye.html')

'''
global parser
parser = sqlparser.SqlParser("example.db")
parser.initialize()
connect = sqlite3.connect("example.db")
cursor = connect.cursor()
parser.createTable("cat")

testRows = [('Jens', 'Johnson', '3039187742', '97401', 'Oregon', '123 Oregon Way'),
            ('Mike', 'Smith', '4551231121', '97403', 'Oregon', '55 Ducks Way'),
            ('Adam', 'White', '6512312243', '84212', 'Colorado', '99 Skiing Avenue')]

cursor.executemany('INSERT INTO cat VALUES (?,?,?,?,?,?)', testRows)
connect.commit()
'''