import sys
# import os

# Need BeautifulSoup to make the bs4 obj, Comment to TODO WHAT DOES IT DO
from bs4 import BeautifulSoup, Comment

def main():
    print("main() running!")
    findTODOs()

def findTODOs():
    # comma-separated string of filenames "path/.../ex-file1.html,path/.../ex-file2.html"
    html_files_str = sys.argv[1]
    html_files_arr = html_files_str.split(',')
    for html_filename in html_files_arr:
        print(f"HTML filename = {html_filename}")
        # Open file --> Make bs4 obj? from each file's contents --> scan contents for TODOs, throw in arr?
        
        # The with keyword ensures the file is closed once done with open() activity
        # open() opens a file: "r" specifies read mode, encoding is the charset
        with open(html_filename, "r", encoding="utf-8") as html_file:
            html_contents = html_file.read()

        # This creates a bs4 object, which can be accessed as a data structure
        soup = BeautifulSoup(html_contents, 'html.parser')


if __name__ == "__main__":
    main()
