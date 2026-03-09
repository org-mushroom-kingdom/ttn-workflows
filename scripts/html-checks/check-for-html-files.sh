pr_number="$1"
verbose="$2"
event_name="$3"

html_files_found="false"
html_filenames_str=""
echo "in .sh!"
echo ".sh: pr_number = ${pr_number}"
echo ".sh: verbose = ${verbose}"
echo ".sh: event_name = ${event_name}"


if [[ "${event_name}" == "workflow_dispatch" ]]
then 
    echo "HEY"
    # PR #9 in ttn-workflows has 2 .html files in it
    echo "pr_number=9" >> $GITHUB_ENV
fi
# Use process substitution to have jq output be treated as stdin for mapfile. (use Github CLI command below to get file info (obj array)), then jq to get just the "path" from each obj. Use -r to remove double quotes from values otherwise they will be present in the string  )
mapfile -t changed_filenames < <(gh pr view $pr_number --json files | jq -r '.files[].path')
[ "${verbose}" == "true" ] && echo "About to start HTML file search..." || :
for changed_filename in "${changed_filenames[@]}"
do
    [ "${verbose}" == "true" ] && echo "changed_filename=${changed_filename}" || :
    if [[ "$changed_filename" == *".html" ]] 
    then
        echo "HIT!"
        html_files_found='true'
        html_filenames_str+="${changed_filename},"
    fi
done

# Removes last char (,) from string
html_filenames_str="${html_filenames_str%?}"
echo "html_filenames_str = ${html_filenames_str}"
echo "html-filenames=${html_filenames_str}" >> "$GITHUB_OUTPUT"

echo "html_files_found = ${html_files_found}"
echo "html-files-present=${html_files_found}" >> "$GITHUB_OUTPUT"