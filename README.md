# ttn-workflows

A repository that stores workflows and things surrounding them (scripts, etc) for the fake app "Toad Town News." Most of the workflows here should be reusable.

1-3-26: At the time of writing, this only has one reusable workflow changelog-quality-check.py used as a supplement to the Medium article 'TODO ARTICLE NAME'. However, it may store more reusable workflows for testing purposes or as additional supplmental material for future articles.

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
- Has the repository name in it (known in the script as release_verison) in the fashion of `org-mushroom-kingdom/ttn-*` where * is the desired text. This text (known in the script as `ttn_type`) should be after the CHANGELOG prefix and a dash separator (ex. if the repository is `org-mushroom-kingdom/ttn-frontend`, then the text 'frontend' should be present)
- Has the release version in it, after the above mentioned substring and a dash separator. The release version should match the name of the source branch that is being merged into the main/master branch (ex. if the source branch name is 'release/v1.1', the substring 'v1.1' should be present).
- Ends with the extension ".txt"

For example, given the following scenario: 

- <u>Repository</u>: `org-mushroom-kingdom/ttn-frontend` 
- <u>Source Branch (release branch)</u>: `release/v1.1`

The expected CHANGELOG filename would be `CHANGELOG-frontend-v1.1.txt`.

Examples CHANGELOG filenames that would NOT be valid are:
- `CHANGELOGfrontend-v1.1.txt` (lacks a dash between CHANGELOG and the ttn_type (frontend))
- `CHANGELOG-ttn-frontend-v1.1.txt` (has 'ttn' in it, when the expected ttn_type should be 'frontend')
- `CHANGELOGfrontend-1.1.txt` (has '1.1' in it, when the release_version should be 'v1.1')

#### **CHANGELOG File Quantity Check**

When assessing the changed files in a pull request, the workflow will assess how many potential CHANGELOG files there are. A potential CHANGELOG file is any file that begins with the substring "CHANGELOG" in this case. In the event the amount of potential CHANGELOG files is NOT 1, the workflow will evaluate this as a failure (even in a scenario where a properly-named CHANGELOG file may be present amongst other potential CHANGELOG files)

#### **Workflow and Script Logic**

TODO: Text Formatting (MAG?)

This workflow consists of 1 job 'changelog-check' (full name 'Changelog Check (Exists and Naming)'). This workflow relies on a Python script for much of its work. 

When called upon, this workflow will perform the following logic <br>(Note: steps that are triggered by manual testing are not listed. Additionally, the Python script is explained all in one step.)

1. Set various environmental variables that relate to the pull request.
2. Checkout the repository using `actions/checkout` (this will checkout the caller repository)
3. Print (echo) various environmental variables and select other variables
4. Set the expected CHANGELOG filename based on the (caller) repository name and source branch name. (see above subsection **__Expected CHANGELOG Filename__**)
5. Get the changed files of the pull request that triggered the workflow (i.e. the changed files of the pull request in the caller workflow's repo.). This is done via a Github API call. These files will be written to a comma-delimited string (the environmental variable `CHANGED_FILES_STR`).
6. Uses `actions/setup-python` to setup Python in the Github-hosted runner, since a Python script will be called to do some of the work.
7. Checks out the `org-mushroom-kingdom/ttn-workflows` repo. This is needed because the aforemetioned Python script is in the `ttn-workflows` repo. When this workflow is called, it is done within the context of the caller workflow's repository. Thus, we checkout the `ttn-workflows` repository to the `ttn-workflows-repo/` directory in our runner. We can then utilize the Python script via accessing this directory
8. Grant execute permissions to the Python script (via the `ttn-workflows-repo/` directory)
9. Run the Python script: <br>
      &emsp; We provide the expected CHANGELOG filename and changed file list as arguments. <br>
      &emsp;a. For each changed file (LOOP): <br>
            &emsp;&emsp;- IF it begins with 'CHANGELOG': <br>
                &emsp;&emsp;&emsp;- If true, add it to an array `potential_changelog_files` <br>
                &emsp;&emsp;&emsp;- If false, do nothing <br>
      &emsp;b. After the changed file LOOP has finished, assess the length of potential_changelog_files: <br>
            &emsp;&emsp;- IF the length is > 1: <br>
                &emsp;&emsp;&emsp;- Set an output message as the environmental variable CHANGELOG_MSG stating only one CHANGELOG file is allowed<br>
                &emsp;&emsp;&emsp;- Print this message<br>
                &emsp;&emsp;&emsp;- Exit with a bad status code<br>
            &emsp;&emsp;- ELSE IF the length is 0: <br>
                &emsp;&emsp;&emsp;- Set an output message as the environmental variable CHANGELOG_MSG stating a CHANGELOG file is required. <br>
                &emsp;&emsp;&emsp;- Print this message<br>
                &emsp;&emsp;&emsp;- Exit with a bad status code<br>
            &emsp;&emsp;- ELSE (potential_changelog_files is exactly 1 length):<br>
                &emsp;&emsp;&emsp;- IF the file has the expected CHANGELOG name (see above subsection **__Expected CHANGELOG Filename__**): <br>
                    &emsp;&emsp;&emsp;&emsp;- If true:<br>
                        &emsp;&emsp;&emsp;&emsp;&emsp;- Set an output message as the environmental variable CHANGELOG_MSG stating the name of the CHANGELOG file is correct. <br>
                        &emsp;&emsp;&emsp;&emsp;&emsp;- Print this message. <br>
                        &emsp;&emsp;&emsp;&emsp;&emsp;- Exit with a passing status code. <br>
                    &emsp;&emsp;&emsp;&emsp;- If false: <br>
                        &emsp;&emsp;&emsp;&emsp;&emsp;- Set an output message as the environmental variable CHANGELOG_MSG stating the name of the CHANGELOG file is incorrect, as well as what it should be. <br> 
                        &emsp;&emsp;&emsp;&emsp;&emsp;- Print this message. <br>
                        &emsp;&emsp;&emsp;&emsp;&emsp;- Exit with a bad status code.<br>
10. Use the CHANGELOG_MSG environmental variable that was set in step 9 in conjunction with the Github API to put a comment on the PR stating the status of the CHANGELOG file quality checks.
11. Based upon the status code of the Python script, the workflow returns a passing or failing status. This status can be leveraged with a branch protection rule to allow or disallow merging the PR into the target branch. 

### Manual Testing

This workflow has the workflow_dispatch trigger, meaning it can be triggered manually. This workflow was manually tested using the Github Actions UI page.
TODO AND ALSO FROM THE CALLER??? HOW TO MENTION

#### **Inputs**

The following inputs are used for manual testing:

| Name | Description | Type | Notes |
|---|---|---|---|
| exp_changelog_filename_man | Expected CHANGELOG filename | choice | Options: <br> - 'CHANGELOG_frontend_v1.1.txt' <br> - 'CHANGELOG_backend_v1.2.txt' |
| pr_num_man | Manual PR number (changed files) | choice | Options: <br> - '2 - CHANGELOG_frontend_v1.1.txt' <br>- '3 - CHANGELOG_backend_v1.2.txt' <br> - '4 - CHANGELOG_backend_v1.1.txt,CHANGELOG_backend_v1.2.txt' |

The first input is the name of the expected CHANGELOG filename. 

The other input is what the changed files might be in hypothetical pull request (which we can refer to as "pull request"). There is a number before the lis of changed files. This is because that number points to a real pull request in the ttn-workflows repo; that number is used in the Github API call mentioned in the __**Workflow and Script Logic**__ section. Having it be set up this way allows us to test the workflow more organically (versus doing something like setting the CHANGED_FILES_STR to the value of some input). You may ask why didn't I be fancy and try to take pull requests from other repos and the reason I didn't is because this way is simpler and I also didn't even think about that until I wrote this sentence.

The mixing and matching of these inputs allow you to produce the following scenarios:

1. (Happy Path) The CHANGELOG file has the expected name because its name properly corresponds with the source (release) branch name and it is the only CHANGELOG file present in the "pull request"
2. The CHANGELOG file is NOT properly named, because its name does NOT properly correspond with the source (release) branch name. However, it is the only CHANGELOG file present in the "pull request".
3. There are too many potential CHANGELOG files.
4. There are no CHANGELOG files. 

Scenario 1 is the most easily tested since the first option in each input match up with each other. To test Scenario 1, simply just hit the Run test button without changing any input. You could also test Scenario 1 by using the second option of each input.

Scenario 2 is tested by having the inputs be misaligned with each other. One CHANGELOG file exists in the changed file list, but does not match the expected CHANGELOG name.

Scenario 3 is tested by using the pr_num_man option '4 - CHANGELOG_backend_v1.1.txt,CHANGELOG_backend_v1.2.txt' which corresponds to a pull request with more than one CHANGELOG file in it. 

Scenario 4 is tested by using the pr_num_man option TODO MAKE THE PR