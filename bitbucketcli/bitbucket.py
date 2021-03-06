from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import sys
import subprocess
from getpass import getpass
import os

'''
CLI INPUT FORMATTING
    python3 -m bitbucketcli username([1] in args list) -r/--add-repo repoName -P/--project-name projectName -p/--path path
'''

'''
    TODO:
'''

class Bitbucket():
    def __init__(self, username, password):
        print("\n\nChrome installation stuff:")

        # Adding the headless option allows the browser to open without a GUI. This makes the program far more user friendly.
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

        # COMMENT OUT THE ABOVE THREE LINES AND UNCOMMENT THIS ONE IF YOU WANT TO SEE THE BROWSER WINDOW
        # self.driver = webdriver.Chrome(ChromeDriverManager().install())

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

        # Unfortunately backwards logic to confirm a successful login. It checks to see if the username prompt is still on the screen, and if it is not, it fails, which means the
        # login was successful, if that makes sense :/
        fail = False
        try:
            successCheck = self.driver.find_element_by_id("password")
            print("\nLogin Failed. Incorrect password?")
            fail = True
        except:
            print("\nLogin Successful.")

        # Also putting exit() in the try section makes it fail so it does the except stuff >:(
        if fail:
            exit()


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

        if "-d" in sys.argv or "--pkg-defaults" in sys.argv:
            print("\nNow creating the defualt files and directories.")
            name = input("Your name(for the License): ")

            subprocess.call(["touch", path + repoName + "/" + "LICENSE"])
            f = open(path + repoName + "/" + "LICENSE", "w+")

            f.write("MIT License\n\nCopyright (c) 2020 " + name + '\n\nPermission is hereby granted, free of charge, to any person obtaining a copy\nof this software and associated documentation files (the "Software"), to deal\nin the Software without restriction, including without limitation the rights\nto use, copy, modify, merge, publish, distribute, sublicense, and/or sell\ncopies of the Software, and to permit persons to whom the Software is\nfurnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all\ncopies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR\nIMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,\nFITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE\nAUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER\nLIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,\nOUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE\nSOFTWARE.')
            f.close()

            os.mkdir(path + repoName + "/" + repoName + "/")
            subprocess.call(["touch", path + repoName + "/" + repoName + "/" + "__init__.py"])
            subprocess.call(["touch", path + repoName + "/" + repoName + "/" + "__main__.py"])

            print("\nSuccessfully created all files and directories, now attempting to commit.")

            os.chdir(path + repoName)
            subprocess.call(["git", "pull"])

            subprocess.call(["git", "add", "."])
            subprocess.call(["git", "commit", "-am", "Initial commit :)"])
            subprocess.call(["git", "push"])

            print("Extra dub :D")

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

    def listRepos(self):
        repoNames = []

        self.driver.get('https://bitbucket.org/dashboard/repositories')
        sleep(5)
        repoSpans = self.driver.find_elements_by_xpath("//a[@class='']")
        if len(repoSpans) / 2 > 20:
            yn = input("List all " + str(len(repoSpans) / 2) + " repositories? (y/n): ")
            if yn == "n" or yn == "N":
                exit()
        print("\n")
        print("Repositories:")
        for span in repoSpans:
            print("     " + span.text)
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
        print("-l/--list-projects")
        print("    List all of the projects under the account\n")
        print("-L/--list-repos")
        print("    List all of the repositories under the account\n")
        print("-d/--pkg-defaults")
        print("    Create default files for a package such as a License and setup.py as well as directories, then attempt to commit the new goodies to the new repository.\n")
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
        elif "-L" in arg or "--list-repos" in arg:
            bit.listRepos()

        count += 1
