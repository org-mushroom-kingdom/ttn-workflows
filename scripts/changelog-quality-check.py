# Take in an argument of changed_files_str (a comma-delimited string). Turn that str into an arr called changed_files_arr
# Iterate thru arr to see if properly named CHANGELOG file exists. Output result msg and status code
# Note: If more than one CHANGELOG file found, immediately fail regardless of passing CHANGELOG name.

import sys
import os

def main():
    print("main() running!")
    # Remember sys.argv[0] is the name of the script itself
    changed_files_str = sys.argv[1]
    expected_changelog_name = sys.argv[2]

    file_beg_w_changelog_exists = False
    changelog_naming_passes = False

    changed_files_arr = changed_files_str.split(',')
    files_beg_w_changelog = []
    github_env_file = os.getenv('GITHUB_ENV')

    output = ""
    changelog_found_msg = "A CHANGELOG file was found"
    only_1_changelog_msg = f"All release branches going into main must have exactly 1 CHANGELOG file in the pull request."
    exp_name_msg = f"The name of the CHANGELOG file should be {expected_changelog_name}"

    for changed_filename in changed_files_arr:
        if changed_filename.startswith("CHANGELOG"):
            file_beg_w_changelog_exists = True
            if changed_filename == expected_changelog_name:
                changelog_naming_passes = True
                break
            print("changed filename starts with CHANGELOG")
            files_beg_w_changelog.append(changed_filename)

    # If more than one CHANGELOG file exists, don't bother checking for a passing name.
    if len(files_beg_w_changelog) >1:
        output = f"There are multiple files in the pull request that begin with CHANGELOG. {only_1_changelog_msg} {exp_name_msg}"
        # sys.exit(1)
    else:
        # TODO: Write output as Github Actions env var which is possible but I forget how 
        if file_beg_w_changelog_exists and changelog_naming_passes:
            output = f"{changelog_found_msg} and matches the expected naming convention for this repo and release branch."
            print(f"{output}")
            # sys.exit(0)
        elif file_beg_w_changelog_exists and not changelog_naming_passes:
            output = f"{changelog_found_msg} (specifically, a file beginning with 'CHANGELOG' was found), but is not the correct name for this release branch. {exp_name_msg}"
            print(f"{output}")
            # sys.exit(1)
        else:
            # Note: Make sure synchronize is specified in pull_request event in caller workflows.
            # TODO: Make sure \n and += work in Python as expected.
            output = "No CHANGELOG file found. {only_1_changelog_msg}\n"
            output+= "{exp_name_msg}\n"
            output+= "Please either amend this PR to include the CHANGELOG file, or close this PR and create a new one with the CHANGELOG file."
            print(f"{output}")
            # sys.exit(1)

    # TODO: Test this and see if it works in the reusable workflow. Rework this into a function
    # The "a" flair means open the file in append mode
    # Each variable has to be set on a new line, so use \n as a best practice (even if no other vars get set in this script, it's a good habit to get into) 
    print("About to write to GITHUB_ENV")
    with open(github_env_file, "a") as github_env:
        github_env.write(f"CHANGELOG_MSG={output}\n")
    # github_env_file.write(f"{CHANGELOG_MSG}={output}\n")

# __name__ is a Python built-in. It is the name of the Python module assessed by the interpreter (usually CPython)
# __main__ is the name of the environment where top-level code is run: top-level imports all other module the program needs
# When you pass a Python module to the interpreter as a file argument (ex. in the workflow 'python changelog-quality-check.yml'), __name__ is set to '__main__'
# Using this convention helps the module identify if it is top-level or not--if the module is top-level, it will execute 
# The workflow for CHANGELOG stuff only runs this script, but for more complex scenarios some modules will have code meant only for script use. 
# If a module with script-use code was TODO Finish this thought
if __name__ == "__main__":
    main()
