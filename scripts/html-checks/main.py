# Built-in modules
import sys
import os
import re

# Need BeautifulSoup to make the bs4 obj, Comment to TODO WHAT DOES IT DO
from bs4 import BeautifulSoup, Comment, NavigableString

def main():
    print("main() running!")
    # The <var>: <datatype> = <value> seen below here is know as type annotation. This is an optional Python way of defining/declaring variables. 
    html_files_str: str = sys.argv[1] # comma-separated string of filenames "path/.../ex-file1.html,path/.../ex-file2.html"
    path: str = sys.argv[2]
    html_files_arr: list[str] = html_files_str.split(',')
    for html_filename in html_files_arr:
        todos = findTODOs()
        print(f"todos[0] = {todos[0]}")
        # assessTODOs()

def findTODOs() -> list[NavigableString]:
    

    # html_files_arr = ["./docs/testing/html-checks/html/article-template.html"]
    cwd: str = os.getcwd()
    print(f"Current working directory: {cwd}")
    
    files_with_bad_todos: list[str] = []

    # for html_filename in html_files_arr:
        print("--------------")
        print(f"HTML filename = {html_filename}")
        # Open file --> Make bs4 obj? from each file's contents --> scan contents for TODOs, throw in arr?
        html_filepath: str = path+"/"+html_filename
        # The with keyword ensures the file is closed once done with open() activity
        # open() opens a file: "r" specifies read mode, encoding is the charset
        with open(html_filepath, "r", encoding="utf-8") as html_file:
            html_contents: str = html_file.read()

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
        comments: list[NavigableString] = soup.find_all(string=lambda line_text: isinstance(line_text, Comment))


        # This is a list comprehension. It's a shorthand way to create a new list based on the values of an existing list
        # The structure of a list comprehenison is [<expression><iterable><filter condition (optional)>]
        # This is saying "For each comment (in the comments array), if the comment has "TODO" in it, keep it AS IS (thus the very first "comment") in this new list. 
        # You can map and filter in the same step. For example if the first "comment" after [ was replace with "comment.upper" you'd filter for all comments containing "TODO", then upper() to those
        todo_comments: list[str] = [comment for comment in comments if "TODO" in comment]
        
        return todo_comments

        todos_missing_jiras: list[str] = []
        for todo_comment in todo_comments:
            # print(f"Item in todo_comments: {todo_comment}")
            # re.Pattern is the result of re.compile(). It's an object you can call regex-based methods on, like search() (see below)
            # This pattern is  "A #, followed by 4-6 letters, followed by a -, followed by (1-5 numbers)"
            jira_story_pattern: re.Pattern = re.compile(r"#[a-z]{4,6}-\d{1,5}", re.IGNORECASE)
            
            # search() returns a Match object if a match was found. It returns None if it wasn't (None evaluates to falsy)
            match: bool = jira_story_pattern.search(todo_comment)
            if match: 
                print(f"This TODO comment has a story number! {todo_comment}")
            else:
                print(f"This TODO comment DOES NOT have a story number! {todo_comment}")
                todos_missing_jiras.append(todo_comment)

        if (len(todos_missing_jiras)):
            print("The following comments have 'TODO' in them, but are missing corresponding Jira story numbers:")
            for bad_todo in todos_missing_jiras:
                print(f"{bad_todo}")
                files_with_bad_todos.append(html_filename)


if __name__ == "__main__":
    main()
