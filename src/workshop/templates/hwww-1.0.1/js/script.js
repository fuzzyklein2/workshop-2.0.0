$(document).ready(function() {
    // Create a button with text 'OK'
    const okButton = $('<button>OK</button>');

    // Add click event to the button
    okButton.click(function() {
        // Send AJAX GET request to cgi-bin/hello.py
        $.ajax({
            url: 'cgi-bin/cgignition.py',   // URL of your CGI script
            method: 'GET',             // or 'POST' if needed
            success: function(response) {
                // Put the response inside the output div
                $('#output').html(response);
            },
            error: function(xhr, status, error) {
                $('#output').html('Error: ' + error);
            }
        });
    });

    // Add the button to the container
    $('#button-container').append(okButton);
});