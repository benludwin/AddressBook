const isAlphaNumeric = ch => {
    /*
    Credit for this function is to Brett Lowrey's online guide (https://lowrey.me/test-if-a-string-is-alphanumeric-in-javascript/)
    Pattern used for validation in save as input box.
    */
	return ch.match(/^[a-z0-9]+$/i) !== null;
}

$(document).ready(function(){
    $('#newTableForm').submit(function(event) {
        // User request to create a new table
        $(location).attr('href', '/create/' + $('#newTableInput').val());
        event.preventDefault();
    });
    
    $('button.btn.btn-dark.viewBookBtn').click(function(){
        // User request to view book from the viewbooks.html page
        $(location).attr('href', '/view/' + $(this).parent().parent().find('.col-8.viewBookName').text());
    });

    $('button.btn.btn-danger.deleteBookBtn').click(function(){
        // Confirm that a user would like to delete a book, and then delete it
        var bookName = $(this).parent().parent().find('.col-8.viewBookName').text()
        if (window.confirm("Are you sure you would like to delete the book "+bookName+"?")){
            $(location).attr('href', '/delete/' + bookName);
        }
    });

    $('button#createNewBook').click(function(){
        // User request to create new book
        $(location).attr('href', '/create');
    });
    $('button#newEntry').click(function(){
        // Request to add new entry to a book
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/entry/' + path[path.length - 1]);
    });
    $('button.btn.btn-dark.newEntryWithData').click(function(){
        // Sends a parameterized redirect to update an entry in an address book
        let path = $(location).attr('pathname').split('/');
        var firstName = "?firstName=" + $(this).parent().siblings('.firstNameRow').text();
        var lastName = "&lastName=" + $(this).parent().siblings('.lastNameRow').text();
        var phone = "&phone=" + $(this).parent().siblings('.phoneRow').text();
        var email = "&email=" + $(this).parent().siblings('.emailRow').text();
        var address = "&address=" + $(this).parent().siblings('.addressRow').text();
        var state = "&state=" + $(this).parent().siblings('.stateRow').text();
        var zip = "&zip=" + $(this).parent().siblings('.zipRow').text();
        $(location).attr('href', '/update/' + path[path.length - 1] + firstName+lastName+phone+email+address+state+zip);
    });
    $('button.btn.btn-danger.deleteEntry').click(function(){
        // Confirm that a user would like to delete an entry in an address book, then delete it
        let path = $(location).attr('pathname').split('/');
        var firstName = $(this).parent().siblings('.firstNameRow').text();
        var lastName = $(this).parent().siblings('.lastNameRow').text();
        var phone = $(this).parent().siblings('.phoneRow').text();
        var email = $(this).parent().siblings('.emailRow').text();
        var address = $(this).parent().siblings('.addressRow').text();
        var state = $(this).parent().siblings('.stateRow').text();
        var zip = $(this).parent().siblings('.zipRow').text();
        if (window.confirm('Are you sure you want to delete this entry?')){
            $(location).attr('href', '/delete/' + path[path.length - 1] + '/'+firstName+','+lastName+','+phone+','+email+','+address+','+state+','+zip);
        }
    });
    $('button#newBookEntryBtn').click(function(){
        // Create a new entry in an address book
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/entry/'+path[path.length - 1]);
    });
    $('button#saveBtn').click(function(){
        // Save current changes in an address book with a given name (confirming first)
        let path = $(location).attr('pathname').split('/');
        if (window.confirm("Would you like to save the address book '"+path[path.length - 1]+"'?")){
            $(location).attr('href', '/save/'+path[path.length - 1]);
        }
    });
    $('button#saveAsBtn').click(function(){
        // Save a book with the provided name (verifying that it is alphanumeric first)
        let path = $(location).attr('pathname').split('/');
        var newName = prompt("What would you like to save your book as?", "");
        while (newName == "" || !isAlphaNumeric(newName)){
            newName = prompt("What would you like to save your book as?\n(Note: the book's name must be an alphanumeric string)", "");
        }
        if (newName != "" || newName != null){
            $(location).attr('href', '/save/'+path[path.length - 1]+'/'+newName);
        }
    });
    $('button.btn.sortBtn').mouseenter(function(){
        // Highlights sort button on mouseover
        $(this).children('i').css('color', '#005899');
    });
    $('button.btn.sortBtn').mouseleave(function(){
        // De-highlights sort button on mouseout
        $(this).children('i').css('color', 'white');
    });
    $('button#sortFirstNameAsc').click(function(){
        // Sort by first name ascending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/firstName/ASC');
    });
    $('button#sortFirstNameDesc').click(function(){
        // Sort by first name descending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/firstName/DESC');
    });
    $('button#sortLastNameAsc').click(function(){
        // Sort by last name ascending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/lastName/ASC');
    });
    $('button#sortLastNameDesc').click(function(){
        // Sort by last name descending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/lastName/DESC');
    });
    $('button#sortPhoneAsc').click(function(){
        // Sort by phone ascending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/phone/ASC');
    });
    $('button#sortPhoneDesc').click(function(){
        // Sort by phone descending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/phone/DESC');
    });
    $('button#sortEmailAsc').click(function(){
        // Sort by email ascending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/email/ASC');
    });
    $('button#sortEmailDesc').click(function(){
        // Sort by email descending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/email/DESC');
    });
    $('button#sortAddressAsc').click(function(){
        // Sort by address ascending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/address/ASC');
    });
    $('button#sortAddressDesc').click(function(){
        // Sort by address descending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/address/DESC');
    });
    $('button#sortStateAsc').click(function(){
        // Sort by state ascending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/state/ASC');
    });
    $('button#sortStateDesc').click(function(){
        // Sort by state descending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/state/DESC');
    });
    $('button#sortZipAsc').click(function(){
        // Sort by zip ascending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/zip/ASC');
    });
    $('button#sortZipDesc').click(function(){
        // Sort by zip descending
        let path = $(location).attr('pathname').split('/');
        $(location).attr('href', '/viewSorted/'+path[path.length - 1]+'/zip/DESC');
    });
    $('button#refreshBook').click(function(){
        // Refresh the book after a search or sort query
        $(location).attr('href', '/view/'+$(this).attr('name'));
    });
    $('button.btn.btn-dark.addBook').click(function(){
        // Add a new book (called from viewbooks.html)
        $(location).attr('href', '/create');
    });
    $('button#closeApplicationBtn').click(function(){
        // Close the application
        if (window.confirm("The application will now shut down.")){
            $(location).attr('href', '/shutdown');
        }
    });
});