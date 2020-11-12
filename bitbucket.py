from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from autoread import read
import sys
import subprocess

'''
CLI INPUT FORMATTING
    python3 bitbucket.py username([1] in args list) -r/--add-repo repoName -P/--project-name projectName -p/--path path
'''

class Bitbucket():
    def __init__(self, username, password):
        # Adding the headless option allows the browser to open without a GUI. This makes the program far more user friendly.
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        # COMMENT OUT THE ABOVE THREE LINES AND UNCOMMENT THIS ONE IF YOU WANT TO SEE THE BROWSER WINDOW
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())

        try:
            # Login stuff
            self.driver.get("https://bitbucket.org/account/signin/")
            usernameBox = self.driver.find_element_by_id("username")
            usernameBox.send_keys(username)
            loginSubmit = self.driver.find_element_by_id("login-submit")
            loginSubmit.click()
            sleep(1)

            passBox = self.driver.find_element_by_id("password")
            passBox.send_keys(password)
            loginSubmit.click()
            sleep(5)

            print("\nSuccessful login.")
        except:
            print("\nLogin failed.")
            raise

    def addRepository(self, repoName, public, path, projectName='Untitled project'):
        self.driver.get("https://bitbucket.org/repo/create")
        sleep(5)
        projectDropdown = self.driver.find_element_by_xpath("//div[@id='s2id_id_project']")
        projectDropdown.click()

        sleep(2)
        projectSelect = self.driver.find_element_by_xpath("//span[text()='" + projectName + "']")
        projectSelect.click()

        sleep(2)
        repoText = self.driver.find_element_by_xpath("//input[@name='name']")
        repoText.send_keys(repoName)

        if publicAccess:
            sleep(2)
            publicCheckBox = self.driver.find_element_by_id("id_is_private")
            publicCheckBox.click()

        print("\nSubmitting the repository now.")
        sleep(2)
        finalSubmit = self.driver.find_element_by_xpath("//button[text()='Create repository']")
        finalSubmit.click()


        # Get code for first pull
        sleep(4)
        cloneLink = self.driver.find_element_by_xpath("//code").get_attribute("innerHTML").splitlines()[0]
        cloneLink = cloneLink.replace("git clone ", "")
        print("\nFound clone link at " + cloneLink + ", pulling now.")
        sleep(1)
        if path is not None:
            subprocess.call(["git", "clone", cloneLink, path + repoName + "/"])
        else:
            subprocess.call(["git", "clone", cloneLink])

        print("\nDub :)")


if __name__ == "__main__":
    if "-h" in sys.argv or "--help" in sys.argv:
        print("\nUse bitbucket-cli to do a variety of fun bitbucket tasks, like create a new repository and pull it automatically.")
        print("\nArgs:")
        print("-r/--add-repo")
        print("    Add a new repo\n")
        print("-P/--project-name")
        print("    Specify a project name to create a repo under. Defaults to 'Untitled project'\n")
        print("-p/--path")
        print("    Specify a path to clone the new repository to. Defaults to the current directory\n")
        print("--public")
        print("    Make the new repo public, rather than the default private\n")
        exit()

    try:
        print("\nLogging in as " + sys.argv[1])
    except IndexError:
        print("No username input.")
        exit()
    except:
        raise

    # Initial Login
    bit = Bitbucket(username=sys.argv[1], password=read("pass"))

    # Tasks (ex. add repository)
    addRepo = False
    repoName = None

    # For loop specifically for finding tasks
    count = 0
    for arg in sys.argv:
        if "-r" in arg or "--add-repo" in arg:
            repoName = sys.argv[count + 1]
            addRepo = True
        count += 1

    # Add a Repository Selected
    if addRepo:
        # Repo specific variables
        projectName = 'Untitled project'
        path = None
        publicAccess = False

        # Get all other necessary info from cli input
        count = 0
        for arg in sys.argv:
            if "--project-name" in arg or "-P" in arg:
                projectName = sys.argv[count + 1]
            if "--path" in arg or "-p" in arg:
                path = sys.argv[count + 1]
            if "--public" in arg:
                publicAccess = True
            count += 1

        if repoName is None:
            print("\nNo repository name detected. Please use the '-r' tag to include one.")
            exit()

        if path is not None:
            print("\nCreating new repo " + repoName + " under project " + projectName + ". The repo will be cloned under '" + path + repoName + "/' when complete.")
        else:
            print("\nCreating new repo " + repoName + " under project " + projectName + ". The repo will be cloned under the current directory when complete.")
            print("btw the current directory is:")
            subprocess.call("pwd")

        # Do it 8)
        bit.addRepository(repoName=repoName, projectName=projectName, public=publicAccess, path=path)

    else:
        print("\nNo task specified. A wasted login :(")
        bit.driver.close()
        exit()
