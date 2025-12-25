# Take in an argument of changed_files_str (a comma-delimited string)
# Turn that str into an arr called changed_files
# Set a status var called changelog_exists to false
# Set a status var called changelog_naming_passes to false
# For each filename in changed_files
#   If filename starts with "CHANGELOG"
#       Set changelog_exists = true
#       files_with_changelog.push(filename) OR files_with_changelog += "$filename,"
#       IF: Assess the filename is equal to the expected CHANGELOG filename
#           If filename == expected --> set expected_naming_passes = true, exit loop early
# End of for loop
# If changelog_exists == true && expected_changelog_name == true
#   sys.exit(0)   ?? --> Pass up to workflow and have workflow output a success message
# Elseif changelog_exists == true && expected_changelog_name == false
#   sys.exit(1) ?? --> Pass up to workflow, have workflow output failure message, also comment on PR
#   The failure message and comment should basically be the same
#   To compose the failure message: "file(s) beginning with CHANGELOG found, but none with expected name ($expected_name) \n: ${files_with_changelog}"
# Else 
    # Must not have been able to find any files that had CHANGELOG in them
    # sys.exit(1) ?? --> Pass up to workflow and have workflow output message and PR comment
    # The failure message = "No CHANGELOG files found in PR."

changed_files = sys.argv[1]
expected_changelog_name = sys.argv[2]

file_beg_w_changelog_exists = False
changed_files_arr = changed_files.split(',')
files_beg_w_changelog = []

for changed_filename in changed_files_arr:
    if changed_filename.startswith("CHANGELOG"):
        file_beg_w_changelog_exists = True
        print("changed filename starts with CHANGELOG")
        files_beg_w_changelog.append(changed_filename)
        if changed_filename == expected_changelog_name:
            changelog_naming_passes = True
            break
if changelog_exists == true and changelog_naming_correct == true:
    output = "A CHANGELOG file was found and matches the expected naming convention for this repo and release branch."
elif  file_beg_w_changelog_exists == true and changelog_naming_correct == false:
