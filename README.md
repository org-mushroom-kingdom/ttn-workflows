# ttn-workflows

A repository that stores workflows and things surrounding them (scripts, etc) for the fake app "Toad Town News." Most of the workflows here should be reusable.

1-3-26: At the time of writing, this only has one reusable workflow (TODO cqc) used as a supplement to the Medium article 'TODO ARTICLE NAME'. However, it may store more reusable workflows for testing purposes or as additional supplmental material for future articles.

# Workflows

## changelog-quality-check.py

### Trigger

A reusable workflow that should be called upon by caller workflows when the caller workflow's repository has a pull request (opened, synchronize, or reopened)that is a release branch being merged into the main/master branch. A release branch will have the word 'release' as a prefix. See more details in caller workflow repos like ttn-frontend.

### Business Logic

#### **Expected CHANGELOG Filename**

This workflow will assess a pull request's files and ensure there is a properly named CHANGELOG file. A properly named CHANGELOG file meets the following criteria:
- Begins with the text "CHANGELOG"
- Ends with the extension ".txt"
- Has the post-"org-mushroom-kingdom/ttn-" repository name in it, after the CHANGELOG prefix and a dash separator (ex. if the repository is org-mushroom-kingdom/ttn-frontend, then the text 'frontend' should be present)
- Has the release version in it, after the above mentioned substring and a dash separator. The release version should match the name of the source branch that is being merged into the main/master branch (ex. if the source branch name is 'release/v1.1', the substring 'v1.1' should be present).


This workflow consists of 1 job 'changelog-check' (full name TODO FULL NAME). 

When called upon, this workflow will perform the following logic (Note: steps that are triggered by manual testing are not listed)

1. Set various environmental variables that relate to the pull request.
2. Checkout the repository using actions/checkout (this will checkout the caller repository)
3. Print (echo) various environmental variables and select other variables
4. Set the expected CHANGELOG filename.
5. Get the changed files of the pull request that triggered the workflow (i.e. the changed files of the pull request in the caller workflow's repo.)
6. 
7. 
will look at a pull request's files. 