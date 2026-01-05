# ttn-workflows

A repository that stores workflows and things surrounding them (scripts, etc) for the fake app "Toad Town News." Most of the workflows here should be reusable.

1-3-26: At the time of writing, this only has one reusable workflow (TODO cqc) used as a supplement to the Medium article 'TODO ARTICLE NAME'. However, it may store more reusable workflows for testing purposes or as additional supplmental material for future articles.

# Workflows

## changelog-quality-check.py

### Trigger

A reusable workflow that should be called upon by caller workflows when the caller workflow's repository has a pull request (opened, synchronize, or reopened)that is a release branch being merged into the main/master branch. A release branch will have the word 'release' as a prefix. See more details in caller workflow repos like ttn-frontend.

### Business Logic

The following section and subsections explain how the TODO NAME reusable workflow performs its work. 

#### **Expected CHANGELOG Filename**

TODO: LOTS of formatting (MAG?)

This workflow will assess a pull request's files and ensure there is a singular, properly named CHANGELOG file. 

A properly named CHANGELOG file meets the following criteria:
- Begins with the text "CHANGELOG"
- Has the repository name in it (known in the script as release_verison) in the fashion of "org-mushroom-kingdom/ttn-*" where * is the desired text. This text (known in the script as ttn_type) should be after the CHANGELOG prefix and a dash separator (ex. if the repository is org-mushroom-kingdom/ttn-frontend, then the text 'frontend' should be present)
- Has the release version in it, after the above mentioned substring and a dash separator. The release version should match the name of the source branch that is being merged into the main/master branch (ex. if the source branch name is 'release/v1.1', the substring 'v1.1' should be present).
- Ends with the extension ".txt"

For example, given the following scenario: 

- <u>Repository</u>: org-mushroom-kingdom/ttn-frontend 
- <u>Source Branch (release branch)</u>: release/v1.1

The expected CHANGELOG filename would be CHANGELOG-frontend-v1.1.txt.

Examples CHANGELOG filenames that would NOT be valid are:
- CHANGELOGfrontend-v1.1.txt (lacks a dash between CHANGELOG and the ttn_type (frontend))
- CHANGELOG-ttn-frontend-v1.1.txt (has 'ttn' in it, when the expected ttn_type should be 'frontend')
- CHANGELOGfrontend-1.1.txt (has '1.1' in it, when the release_version should be 'v1.1')

#### **CHANGELOG File Quantity Check**

When assessing the changed files in a pull request, the workflow will assess how many potential CHANGELOG files there are. A potential CHANGELOG file is any file that begins with the substring "CHANGELOG" in this case. In the event the amount of potential CHANGELOG files is NOT 1, the workflow will evaluate this as a failure (even in a scenario where a properly-named CHANGELOG file may be present amongst other potential CHANGELOG files)

#### **TODO SOME HEADER HERE**

TODO: Text Formatting (MAG?)

This workflow consists of 1 job 'changelog-check' (full name TODO FULL NAME). 

When called upon, this workflow will perform the following logic (Note: steps that are triggered by manual testing are not listed)

1. Set various environmental variables that relate to the pull request.
2. Checkout the repository using actions/checkout (this will checkout the caller repository)
3. Print (echo) various environmental variables and select other variables
4. Set the expected CHANGELOG filename based on the (caller) repository name and source branch name. (see above subsection **__Expected CHANGELOG Filename__**)
5. Get the changed files of the pull request that triggered the workflow (i.e. the changed files of the pull request in the caller workflow's repo.). These files will be written to a comma-delimited string.
6. Uses actions/setup-python to setup Python in the Github-hosted runner, since a Python script will be called to do some of the work.
7. Checks out the org-mushroom-kingdom/ttn-workflows repo. This is needed because the aforemetioned Python script is in the ttn-workflows repo. When this workflow is called, it is done within the context of the caller workflow's repository. Thus, we checkout the ttn-workflows repository to the 'ttn-workflows-repo' directory in our runner. We can then utilize the Python script via accessing this directory
8. Grant execute permissions to the Python script (via the ttn-workflows-repo directory)
9. Run the Python script:
      a. For each changed file (LOOP): <br>
            - IF it begins with 'CHANGELOG': <br>
                - If true, add it to an array potential_changelog_files <br>
                - If false, do nothing
      b. After the changed file LOOP has finished, assess the length of potential_changelog_files:
            - IF the length is > 1: <br>
                - Set an output message as the environmental variable CHANGELOG_MSG stating only one CHANGELOG file is allowed
                - Print this message
                - Exit with a bad status code
            - ELSE IF the length is 0: <br>
                - Set an output message as the environmental variable CHANGELOG_MSG stating a CHANGELOG file is required, 
                - Print this message
                - Exit with a bad status code
            - ELSE (potential_changelog_files is exactly 1 length):
                - IF the file has the expected CHANGELOG name (see above subsection **__Expected CHANGELOG Filename__**): <br>
                    - If true:
                        - Set an output message as the environmental variable CHANGELOG_MSG stating the name of the CHANGELOG file is correct. 
                        - Print this message. 
                        - Exit with a passing status code. 
                    - If false: 
                        - Set an output message as the environmental variable CHANGELOG_MSG stating the name of the CHANGELOG file is incorrect, as well as what it should be. 
                        - Print this message. 
                        - Exit with a bad status code.
10. Use the CHANGELOG_MSG environmental variable that was set in step 9 in conjunction with the Github API to put a comment on the PR stating the status of the CHANGELOG file quality checks.
11. Based upon the status code of the Python script, the workflow returns a passing or failing status. This status can be leveraged with a branch protection rule to allow or disallow merging the PR into the target branch. 
