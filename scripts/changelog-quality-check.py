# Take in an argument of changed_files_str (a comma-delimited string). Turn that str into an arr called changed_files_arr
# Iterate thru arr: add to potential_changelog_files if filename begins with "CHANGELOG"
# Note: If length of potential_changelog_files != 1, fail regardless of passing CHANGELOG name.
# If length of potential_changelog_files == 1, pass
# In whatever scenario, write an output message that the workflow can use in a PR comment

import sys
import os

def main():
    print("main() running!")
    # Remember sys.argv[0] is the name of the script itself
    changed_files_str = sys.argv[1]
    expected_changelog_name = sys.argv[2]

    changed_files_arr = changed_files_str.split(',')
    potential_changelog_files = []
    github_env_file = os.getenv('GITHUB_ENV')

    output = ""
    changelog_found_msg = "A CHANGELOG file was found (specifically, a file beginning with 'CHANGELOG' was found)"
    only_1_changelog_msg = f"All release branches going into main must have exactly 1 CHANGELOG file in the pull request."
    exp_name_msg = f"The name of the CHANGELOG file should be {expected_changelog_name}"

    for changed_filename in changed_files_arr:
        if changed_filename.startswith("CHANGELOG"):
            print("changed filename starts with CHANGELOG")
            potential_changelog_files.append(changed_filename)

    # If more than one CHANGELOG file exists, don't bother checking for a passing name.
    if len(potential_changelog_files) >1:
        output = f"There are multiple files in the pull request that begin with CHANGELOG. {only_1_changelog_msg} {exp_name_msg}"
        # sys.exit(1)
    elif len(potential_changelog_files) == 0:
        # Note: Make sure synchronize is specified in pull_request event in caller workflows.
        # TODO: Make sure <br> and += work in Python as expected.
        output = f"No CHANGELOG file found. {only_1_changelog_msg}<br>"
        output+= f"{exp_name_msg}<br>"
        output+= f"Please either amend this PR to include the CHANGELOG file, or close this PR and create a new one with the CHANGELOG file."
        print(f"{output}")
        # sys.exit(1)
    else:
        # There must be only 1 potential CHANGELOG file to assess
        changelog_file_of_interest = potential_changelog_files[0]
        if potential_changelog_files[0] ==  expected_changelog_name:
            output = f"{changelog_found_msg} and matches the expected naming convention for this repo and release branch."
            print(f"{output}")
            # sys.exit(0)
        elif:
            output = f"{changelog_found_msg}, but is not the correct name for this release branch. {exp_name_msg}"
            print(f"{output}")
            # sys.exit(1)

    # TODO: Rework this into a function
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

# Snake, try to remember some of the basics of CQC