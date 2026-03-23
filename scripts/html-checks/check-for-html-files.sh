#!/usr/bin/env bash

pr_number="$1"
verbose="$2"
event_name="$3"

org_name="org-mushroom-kingdom"
repo_name="ttn-workflows"

html_files_found="false"
html_filenames_str=""

# Use process substitution to have jq output be treated as stdin for mapfile. (use Github CLI command below to get file info (obj array)), then jq to get just the "path" from each obj. Use -r to remove double quotes from values otherwise they will be present in the string  )
# mapfile -t changed_filenames < <(gh pr view $pr_number --json files | jq -r '.files[].path')

# gh pr view doesn't tell you if the changed files are deleted. 
# In reality you wouldn't probably have to use two separate CLI calls but this is a learning exercise so here we are
# The gh api repos/.../<pr_number> files will give us the status of the changed files. The q flag is a "query", a jq-like expression to filter the response
# .[] says iterate over the response's JSON array. The next piped segment says get the 'status' and 'filename' keys only. 
# The '@csv' says make the element tab-separated string (ex. if file "example.html" is deleted, element looks like "example.html\tdeleted")
# tsv is easier to parse than using @csv 
mapfile -t changed_files_details < <(gh api repos/$org_name/$repo_name/pulls/$pr_number/files -q '.[] | [.filename,.status] | @tsv')


[ "${verbose}" = "true" ] && echo "About to start HTML file search..." || :
for changed_file in "${changed_files_details[@]}"
do
    [ "${verbose}" = "true" ] && echo "changed_file=${changed_file}" || :
    # Feed in the element as a here-string (using <<<). A here-string is a string substitution of stdin, where read normally gets input from  
    # Using tab as a delimiter, split the string into multiple items. Assign the variables listed (status,file) values based on the delimited items and order of the variables
    # ex. if line is "example.html\tdeleted" --> file = "example.html", status = "deleted"
    IFS=$'\t' read -r filename status <<< "${changed_file}"
    if [[ "$status" == "removed" ]]
    then
        # If file is deleted, no need to continue assessment since we don't care about the contents of a deleted file (even if it's an HTML)
        continue
    fi 
    if [[ "$filename" == *".html" ]] 
    then
        [ "${verbose}" = "true" ] && echo "HTML file found!" || :
        html_files_found='true'
        html_filenames_str+="${filename},"
    fi
done


# [ "${verbose}" = "true" ] && echo "About to start HTML file search..." || :
# for changed_filename in "${changed_filenames[@]}"
# do
#     [ "${verbose}" = "true" ] && echo "changed_filename=${changed_filename}" || :
#     if [[ "$changed_filename" == *".html" ]] 
#     then
#         [ "${verbose}" = "true" ] && echo "HTML file found!" || :
#         html_files_found='true'
#         html_filenames_str+="${changed_filename},"
#     fi
# done

echo "html_files_found = ${html_files_found}"
echo "html-files-present=${html_files_found}" >> "$GITHUB_OUTPUT"

# Removes last char (,) from string
html_filenames_str="${html_filenames_str%?}"
echo -e "\nhtml_filenames_str = ${html_filenames_str}"
echo "html-filenames=${html_filenames_str}" >> "$GITHUB_OUTPUT"