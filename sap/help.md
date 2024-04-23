#Unified Login Script Help Guide

##Introduction
This guide provides detailed instructions on using the Unified Login Script application to automate login attempts with customizable headers and various iteration modes.
Configuring Your Session

Before starting a login sequence, configure the following settings:

    Target URL: Enter the login page URL where the script will attempt logins.
    Usernames File: Choose a text file containing usernames, one per line.
    Passwords File: Select a text file with corresponding passwords.
    Headers CSV File: Upload a CSV file defining custom headers for HTTP requests.

##Customization Options
The application allows customization through the following options:

    Header Customization Mode: Choose how headers are applied to requests:
        Uniform Headers for All Requests: Applies the same headers to all login attempts.
        Random Headers for Each Request: Randomly selects a header set for each login attempt.
        Randomize Each Header Value Individally: Randomizes individual header values for each request.
        Unique Headers per Username: Associates unique header sets with each username.

    Iteration Modes: Select the order in which usernames and passwords are paired for login attempts:
        Random Order: Randomly pairs usernames with passwords.
        Systematic Order: Pairs each username with each password systematically.
        Stuffing Mode: Pairs each username with the corresponding password by line number.

##Running a Login Sequence
To start a login sequence, ensure all configurations are set, and click the Start button. The application will begin attempting logins based on your settings. The progress bar and results table will update in real-time.


##Cancelling a Session
To cancel an ongoing login sequence, click the Cancel button. This will immediately stop the process and reset the application for a new session.


##Viewing Results
Successful login attempts are displayed in the results table, including the username and password combination that succeeded. You can save these results for further analysis.

##Troubleshooting and Support
If you encounter issues or need assistance, check the following:

    Ensure all files are correctly formatted and accessible.
    Verify the target URL is correct and the server is reachable.
    For network-related issues, check your internet connection and firewall settings.
