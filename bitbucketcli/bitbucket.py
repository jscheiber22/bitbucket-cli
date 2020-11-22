from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import sys
import subprocess
from getpass import getpass

'''
CLI INPUT FORMATTING
    python3 bitbucket.py username([1] in args list) -r/--add-repo repoName -P/--project-name projectName -p/--path path
'''

'''
    TODO: make a list projects dude for listing projects because yuh 8)
          add a parameter to automatically create a License, blank __init__ file, blank __setup__ file, and anything else for basic package stuff, then auto try to commit them :)
             and folder for package contents, oh and readme :) but custom and cool 8)

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

    def addRepository(self, repoName = "New Repository"):
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
            print("\nCreating new repo " + repoName + " under project " + projectName + ". The repo will be cloned under '" + path + repoName + " when complete.")
        else:
            print("\nCreating new repo " + repoName + " under project " + projectName + ". The repo will be cloned under the current directory when complete.")
            print("btw the current directory is:")
            subprocess.call("pwd")

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
            subprocess.call(["git", "clone", cloneLink, path + repoName])
        else:
            subprocess.call(["git", "clone", cloneLink])

        print("\nDub :)")

    def listProjects(self):
        projectNames = []

        self.driver.get('https://bitbucket.org/dashboard/projects')
        sleep(5)
        projectSpans = self.driver.find_elements_by_xpath("//span[@class='project-list--name']")
        print("\n")
        print("Projects:")
        for span in projectSpans:
            name = span.find_element_by_xpath(".//a").text
            print("     " + name)
        print("\n")



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
        pswd = getpass()
    except IndexError:
        print("No username input.")
        exit()
    except:
        raise

    # Initial Login
    bit = Bitbucket(username=sys.argv[1], password=pswd)

    # For loop specifically for finding tasks
    count = 0
    for arg in sys.argv:
        if "-r" in arg or "--add-repo" in arg:
            bit.addRepository(sys.argv[count + 1])
        elif "-l" in arg or "--list-projects" in arg:
            bit.listProjects()

        count += 1
