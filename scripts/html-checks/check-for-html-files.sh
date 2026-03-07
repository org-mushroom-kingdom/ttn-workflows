arg1="$1"
arg2="$2"
arg3="$3"

html_files_found="false"
html_filenames_str=""

if [ "${{ github.event_name }}" == "something" ]
then 
    echo "HEY"
    # PR #9 in ttn-workflows has 2 .html files in it
    echo "PR_NUMBER=9" >> $GITHUB_ENV
fi
# Use process substitution to have jq output be treated as stdin for mapfile. (use Github CLI command below to get file info (obj array)), then jq to get just the "path" from each obj. Use -r to remove double quotes from values otherwise they will be present in the string  )
mapfile -t changed_filenames < <(gh pr view $PR_NUMBER --json files | jq -r '.files[].path')
[ "${{ inputs.verbose }}" == "true" ] && echo "About to start HTML file search..." || :
for changed_filename in "${changed_filenames[@]}"
do
    [ "${{ inputs.verbose }}" == "true" ] && echo "changed_filename=${changed_filename}" || :
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