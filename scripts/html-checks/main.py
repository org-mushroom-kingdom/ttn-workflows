import sys
import os

# Need BeautifulSoup to make the bs4 obj, Comment to TODO WHAT DOES IT DO
from bs4 import BeautifulSoup, Comment

def main():
    print("main() running!")
    findTODOs()

def findTODOs():
    # comma-separated string of filenames "path/.../ex-file1.html,path/.../ex-file2.html"
    html_files_str = sys.argv[1]
    path = sys.argv[2]
    html_files_arr = html_files_str.split(',')
    # html_files_arr = ["./docs/testing/html-checks/html/article-template.html"]
    cwd = os.getcwd()
    print(f"Current working directory: {cwd}")
    for html_filename in html_files_arr:
        print(f"HTML filename = {html_filename}")
        # Open file --> Make bs4 obj? from each file's contents --> scan contents for TODOs, throw in arr?
        path_html_filename = path+html_filename
        # The with keyword ensures the file is closed once done with open() activity
        # open() opens a file: "r" specifies read mode, encoding is the charset
        with open(html_filename, "r", encoding="utf-8") as html_file:
            html_contents = html_file.read()

        # This creates a bs4 object, which can be accessed as a data structure
        soup = BeautifulSoup(html_contents, 'html.parser')
        # find_all finds all elements in an HTML doc, returning a ResultSet (ex. to find all links --> all_links = soup.find_all('a'))
        # You can use the "string" argument to look for strings instead of tags. This argument takes a string, but can also take regex and functions. Only get the text INSIDE elements is obtained, not along with the tag (ex. if html contains <p>HELLO</p> only gets "HELLO" as output, not "<p>HELLO</p>")
        # Comments aren't elements in a traditional sense and we don't want to pick up other elements, so need to use a lambda function
        # A lambda function is a small, anonymous (nameless), inline function usually made once and immediately used. (format --> argument: expression)
        # find_all feeds each line of text to the lambda. The lambda takes in "line_text" as an input, whose value is a line of text and class is NavigableString.
        # isinstance(item, class) sees if "item" is an instance of "class" and returns true or false
        # So basically this is saying "Read through all lines (NavigableStrings). Filter out lines that are identified as comments (instance of the Comment class)"
        # find_all returns a ResultSet, which is a bs4 version of a Python list. 
        # Each item in that ResultSet is a NavigableString, which is like a string++: in addition to the text contents, it also has navagational functionality.
        # A Comment is a specialized subclass of NavigableString (All Comments are NavigableStrings, but not all NavigableStrings are comments)
        comments = soup.find_all(string=lambda line_text: isinstance(line_text, Comment))

        # At this point we have all the comments in the HTML
        # print(f"Comments in {html_filename}:")
        for comment in comments:
            has_todo=""
            print(f"{comment}")
            # Filter out comments that contain the text "TODO"
            # if "TODO" in comment:
            #     print(f"TODO!!!! {comment}")
            # else:
            #     print(f"{comment}")


if __name__ == "__main__":
    main()
