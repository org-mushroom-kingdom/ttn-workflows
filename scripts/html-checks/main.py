import sys
# import os

from bs4 import BeautifulSoup

def main():
    print("main() running!")
    getHTMLFiles()

def getHTMLFiles():
    print("Searching for HTML files within the changed files")
    # Array of filenames "ex-file1.html,ex-file2.html"
    html_files_str = sys.argv[1]
    html_files_arr = html_files_str.split(',')
    for html_filename in html_files_arr:
        print(f"HTML filename = {html_filename}")
if __name__ == "__main__":
    main()
