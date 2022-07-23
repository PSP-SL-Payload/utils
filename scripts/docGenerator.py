import os
import subprocess
import shutil

# Read the PSP_PATH environment variable
try:
    PSP_PATH = os.environ['PSP_PATH']
    print(f"Using '{PSP_PATH}' as the PSP_PATH")
except:
    print("Please set the PSP_PATH environment variable.\nExiting.")
    exit()

# Commands to use
GIT_ADD_CMD = 'git add .'
GIT_COMMIT_CMD = 'git commit -m "Updating documentation automatically from docGenerator.py"'
GIT_PUSH_CMD = 'git push -f origin main'
DOXYGEN_CMD = 'doxygen Doxyfile'

CMD_SUCCESS = 0

# GCS
GCS_REPO_PATH = os.path.join(PSP_PATH, 'GCS')

# GCS-Core
DOCS_GCS_CORE_REPO_PATH        = os.path.join(PSP_PATH, 'Docs_GCS-Core')
GCS_CORE_REPO_PATH             = os.path.join(GCS_REPO_PATH, 'Core')

# GCS-SensorHub
DOCS_SENSORHUB_REPO_PATH        = os.path.join(PSP_PATH, 'Docs_GCS-SensorHub')
SENSORHUB_REPO_PATH             = os.path.join(GCS_REPO_PATH, 'SensorHub')

# GCS-ButtonHandler
DOCS_BUTTONHANDLER_REPO_PATH    = os.path.join(PSP_PATH, 'Docs_GCS-ButtonHandler')
BUTTONHANDLER_REPO_PATH         = os.path.join(GCS_REPO_PATH, 'ButtonHandler')

# libraries
DOCS_LIBRARIES_REPO_PATH        = os.path.join(PSP_PATH, 'Docs_libraries')
LIBRARIES_REPO_PATH             = os.path.join(PSP_PATH, 'libraries')


def GenerateDocumentation(sourceRepoPath):
    """
    Generates the documentation from the Doxyfile found within the docs/ folder of the sourceRepoPath.

    @param sourceRepoPath (string)     - The absolute path to the source repository to generate documentation for.

    @return (bool)    - Whether or not the documentation was successfully generated.
    """
    sourceRepoPath = os.path.join(sourceRepoPath, 'docs')
    if (os.path.isdir(sourceRepoPath)):
        os.chdir(sourceRepoPath)
        if (os.getcwd() == sourceRepoPath):
            result = subprocess.run(DOXYGEN_CMD, shell=True, capture_output=True, text=True)
            if (result.returncode == CMD_SUCCESS):
                return True
            print(f"    Failed generating documentation using '{DOXYGEN_CMD}'")
            print(result.stderr)
        else:
            print(f"    Error trying to change directory into '{sourceRepoPath}'")
    else:
        print(f"    Error '{sourceRepoPath}' does not exist.")

    print(f"    Will not generate documentation for {sourceRepoPath.split(os.path.sep)[-2]}.")
    return False


def RenameHtmlToDocsDir(docsRepoPath):
    """
    Renames the html/ folder generated by Doxygen within docsRepoPath to docs/ which is required by GitHub pages.

    @param docsRepoPath (string)     - The absolute path to the documentation repository where the documentation was placed by Doxygen.

    @return (bool)    - Whether or not the directory was successfully renamed.
    """
    htmlDir = os.path.join(docsRepoPath, 'html')
    docsDir = os.path.join(docsRepoPath, 'docs')

    if (os.path.isdir(docsDir)):
        try:
            shutil.rmtree(docsDir)
        except:
            print(f"Could not delete '{docsDir}'")

    try:
        os.rename(htmlDir, docsDir)
        return True
    except OSError:
        print(f"Could not rename '{htmlDir}' to '{docsDir}'")
        return False


def PushDocumentation(docsRepoPath):
    """
    Pushes the documentation found in docsRepoPath to GitHub automatically.

    @param docsRepoPath (string)     - The absolute path to the documentation repository where the documentation was placed by Doxygen.

    @return (bool)    - Whether or not the repository was successfully pushed to the remote.
    """
    if (os.path.isdir(docsRepoPath)):
        os.chdir(docsRepoPath)
        if (os.getcwd() == docsRepoPath):
            # Run all the commands ANDed together, so if one fails, the next ones won't run
            cmd = f"{GIT_ADD_CMD} && {GIT_COMMIT_CMD} && {GIT_PUSH_CMD}"
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

            if (result.returncode == CMD_SUCCESS):
                print(f"    Successfully updated {docsRepoPath.split(os.path.sep)[-1]}.")
                return True
            elif ('nothing to commit, working tree clean' in result.stdout):
                print(f"    No updates.")
                return True

            print(f"    Failed pushing documentation using '{cmd}'")
            print(result.stderr)
        else:
            print(f"    Error trying to change directory into '{docsRepoPath}'")
    else:
        print(f"    Error '{docsRepoPath}' does not exist.")

    print(f"    Will not push documentation for {docsRepoPath.split(os.path.sep)[-1]}.")
    return False


def GenerateAndPushDocumentation(sourceRepoPath, docsRepoPath, projectName):
    """
    Generates documentation from sourceRepoPath and places it in docsRepoPath where it is automatically pushed to GitHub pages.

    @param sourceRepoPath (string)   - The absolute path to the source repository to generate documentation for.
    @param docsRepoPath (string)     - The absolute path to the documentation repository where the documentation was placed by Doxygen.
    @param projectName (string)      - The project's name
    """
    print(f"\n\n{projectName}:")
    if (os.path.exists(sourceRepoPath) and os.path.exists(docsRepoPath)):
        if (GenerateDocumentation(sourceRepoPath)):
            if (RenameHtmlToDocsDir(docsRepoPath)):
                PushDocumentation(docsRepoPath)
    else:
        print(f"    Not generating documentation for {projectName} since one of these paths does not exist:\n    {sourceRepoPath}\n    {docsRepoPath}")


if __name__ == '__main__':
    # GCS Core
    GenerateAndPushDocumentation(GCS_CORE_REPO_PATH, DOCS_GCS_CORE_REPO_PATH, 'Core')

    # GCS SensorHub
    GenerateAndPushDocumentation(SENSORHUB_REPO_PATH, DOCS_SENSORHUB_REPO_PATH, 'SensorHub')

    # GCS ButtonHandler
    GenerateAndPushDocumentation(BUTTONHANDLER_REPO_PATH, DOCS_BUTTONHANDLER_REPO_PATH, 'ButtonHandler')

    # Libraries
    GenerateAndPushDocumentation(LIBRARIES_REPO_PATH, DOCS_LIBRARIES_REPO_PATH, 'Libraries')
