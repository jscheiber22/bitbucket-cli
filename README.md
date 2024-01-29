### Bitbucket CLI Tool

The `bitbucket.py` script is a Bitbucket command-line interface (CLI) tool, designed to automate and simplify various tasks associated with managing Bitbucket repositories. Below is a detailed overview of the functionality this script offers and instructions on how to use it.

#### Features

1. **User Authentication:**
    
    - Logs in to the Bitbucket account using Selenium WebDriver with Chrome.
    - The script operates in headless mode by default, meaning the browser's GUI is not displayed, making the program more user-friendly.
2. **Repository Management:**
    
    - **Add Repository (`addRepository`):** Creates a new repository under a specified project. Users can set the repository name, project name, path for cloning the repository, and visibility (public or private).
        - The repository is initialized with a clone URL.
        - Optionally, it sets up default files and directories, including `LICENSE`, `__init__.py`, and `__main__.py`, and performs an initial commit with the message "Initial commit :)".
3. **Project and Repository Listing:**
    
    - **List Projects (`listProjects`):** Fetches and displays a list of all the projects under the user's Bitbucket account.
    - **List Repositories (`listRepos`):** Fetches and displays a list of all the repositories under the user's Bitbucket account. If there are more than 20 repositories, it prompts the user to confirm whether they want to list them all.
4. **Command-Line Interface:**
    
    - The script supports various command-line arguments for performing the above operations.

#### Command-Line Arguments

- `-r` / `--add-repo <repoName>`: Add a new repository.
- `-P` / `--project-name <projectName>`: Specify the project name under which to create the repository. Defaults to 'Untitled project'.
- `-p` / `--path <path>`: Specify the path where the new repository should be cloned. Defaults to the current directory.
- `-l` / `--list-projects`: List all projects under the user's account.
- `-L` / `--list-repos`: List all repositories under the user's account.
- `-d` / `--pkg-defaults`: Create default files and directories for the new repository and commit them.
- `--public`: Make the new repository public. The default is private.

#### How to Use

1. **Installation and Setup:**
    
    - Ensure you have Python installed on your system.
    - Install the required packages: `selenium`, `webdriver_manager`.
2. **Running the Script:**
    
    - Open your terminal or command prompt.
    - Navigate to the directory where the `bitbucket.py` script is located.
    - Run the script using Python and pass the desired arguments. For example:
    ```
    python3 bitbucket.py <your-bitbucket-username> --add-repo MyNewRepo --project-name MyProject --public
  	```
    - Follow the prompts for password input and any other required information.

#### Notes

- The tool is interactive and will require user input for passwords and, optionally, for listing repositories if the number is large.
- It's essential to ensure that the Bitbucket account credentials are correct to avoid login failures.
- The script is designed to be user-friendly and provide feedback about the operations being performed, including login status, repository creation status, and listings of projects and repositories.
