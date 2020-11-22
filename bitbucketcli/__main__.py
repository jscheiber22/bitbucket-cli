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
        print("-l/--list-projects")
        print("    List all of the projects under the account\n")
        print("-L/--list-repos")
        print("    List all of the repositories under the account\n")
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

if __name__ == "__main__":
    main()
