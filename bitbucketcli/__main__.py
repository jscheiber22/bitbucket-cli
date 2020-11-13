from bitbucketcli import Bitbucket
from getpass import getpass
import sys
import subprocess

def main():
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
            print("\nCreating new repo " + repoName + " under project " + projectName + ". The repo will be cloned under '" + path + repoName + " when complete.")
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

if __name__ == "__main__":
    main()
