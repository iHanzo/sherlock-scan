# Spray and Pray (SAP) Application

## Introduction
Spray and Pray (SAP) is a tool tailored for security professionals and enthusiasts to simulate controlled login attempts. It's designed to closely mimic real-world login attempts by combining customizable headers with various iteration modes, enhancing testing precision and efficiency.

## Features

### Header Customization Modes
SAP offers multiple modes for header customization, ensuring flexibility for various testing scenarios:
- **Uniform Headers for All Requests:** Applies the same set of headers to every login attempt.
- **Random Headers for Each Request:** Randomly selects a set of headers from the `headers.csv` for each login attempt.
- **Randomize Each Header Value Individually:** For each header, a random value is chosen for every login attempt, allowing for a mix-and-match approach.
- **Unique Headers per Username:** Assigns a unique set of headers to each username, cycling through the `headers.csv` list.

### Iteration Modes
SAP allows users to choose how login attempts are sequenced through different iteration modes, providing flexibility for various testing strategies:
- **Systematic Order:** This default mode attempts every possible combination of usernames and passwords, systematically covering the entire set to ensure thorough testing.
- **Random Order:** To simulate more realistic login attempts and potentially evade detection mechanisms that flag systematic access patterns, this mode randomizes the order of login attempts.
- **Stuffing Mode:** Designed to mimic credential stuffing attacks, this mode pairs each username with a corresponding password based on their order in the list. It's particularly useful for testing against known username-password pairs.

Each mode is designed to cater to different testing requirements, from comprehensive coverage to mimicking real-world attack patterns.

### Attempt Delay
To simulate real-world usage and avoid triggering rate-limiting mechanisms on the target site, SAP allows setting a random delay between login attempts. Users can specify a minimum and maximum delay range, with the actual delay randomly chosen within this range for each attempt.

### CSRF Token Bypass
SAP is designed to handle CSRF tokens efficiently, automatically fetching and including them in login attempts to bypass CSRF protection mechanisms. This feature is crucial for testing web applications that employ CSRF tokens as a security measure.

### Editable Resource Lists
Directly from the SAP interface, users can edit the lists of usernames, passwords, and headers, facilitating quick adjustments to the testing parameters without needing to navigate away from the application.

### Results Logging
SAP logs the outcomes of login attempts in the `results` folder, providing a detailed record of successful and unsuccessful logins, including timestamps and the credentials used.

For detailed guidance on each feature and setting up your first login sequence, refer to the Help section within the SAP application.


## Getting Started
This section will guide you through setting up and starting your first login sequence with SAP.

### Prerequisites
- Python 3.6 or newer
- Requests library (`pip install requests`)
- BeautifulSoup library (`pip install beautifulsoup4`)
- Tkinter (usually comes with Python)

### Installation
1. Clone the repository or download the ZIP file.
2. Extract the files to your preferred directory.
3. Ensure you have the required Python libraries installed.

### Running the Application
1. Open a terminal or command prompt.
2. Navigate to the directory containing `sap.py`.
3. Run the command `python sap.py` to start the application.

## Resources Folder
The `resources` folder contains essential files for the application's operation:
- `usernames.txt`: List of usernames to try during login attempts.
- `passwords.txt`: List of passwords to pair with the usernames.
- `headers.csv`: CSV file where you can define custom headers for each request.
- `users.ods`: A table storing all real and unreal credential pairs for reference.

## Results Folder
After executing login sequences, the `results` folder will store session logs, including successful login attempts with timestamps and used credentials.

## Help and Documentation
Detailed documentation on how to use each feature of the SAP application can be found within the application's Help menu, offering step-by-step instructions and tips for effective testing.

## Contributing
We welcome contributions to the Spray and Pray application. Please feel free to submit pull requests or open issues on GitHub to suggest enhancements or report bugs.

## License
The Spray and Pray application is provided under All Rights Reserved. Please see the LICENSE file for more details.

## Acknowledgments
- Special thanks to [CONTRIBUTOR NAMES] for their invaluable contributions to the project.
- Gratitude to the open-source community for the tools and libraries that made this project possible.


