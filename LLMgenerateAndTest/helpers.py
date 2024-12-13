import ast
import re


def get_section(file_content, start_pattern, end_pattern, include_start_pattern=True):
    """

    :rtype: object
    """
    # This function takes a string "file_content" and returns the substring starting with the start_pattern and
    # ending with the end_pattern.   If the start_pattern and the end pattern  are not found, it returns
    # the empty string.  If the start_pattern is not found but the end_pattern is found, then it returns the substring
    # from the beginning until the end_pattern.  If the start_pattern is found but not the end_pattern, it returns the
    # substring from the start_pattern until the end of the string.
    # print(f"file_content = \n{file_content}, \nstart_pattern = '{start_pattern}', end_pattern = '{end_pattern}'")
    # print(f"get_section: start_pattern = {start_pattern}")
    start_pattern_index = file_content.find(start_pattern)
    if start_pattern_index == -1:
        start_index = 0
        print("start pattern not found")
    else:
        if include_start_pattern:
            start_index = start_pattern_index
            print("Found start pattern")
        else:
            # include_start_pattern = False so jump over the start pattern
            start_index = start_pattern_index + len(start_pattern)
            print("Found start pattern")
    print("start_pattern, start_pattern_index, start_index = ", start_pattern, start_pattern_index, start_index)
    # print("start_index =", start_index)
    end_index = file_content.find(end_pattern, start_index + len(start_pattern))
    # print("end_index = ", end_index)
    # If end index not found and start index not found, then return empty string ''
    # If end index not found but start index is found, then return the content from the start index until the end
    # if end index is found and start index is found, then return the content from the start index until the end index
    # if end index is found but the start index is not found, then return the contents from the beginning until the end index
    if end_index == -1:
        if start_pattern_index == -1:
            section = ''
        else:
            section = file_content[start_index:]
    else:
        section = file_content[start_index:end_index]
    return section


def has_multiple_lines(file_path):
  """Checks if a file has more than one line.

  Args:
    file_path: The path to the file.

  Returns:
    True if the file has more than one line, False otherwise.
  """

  with open(file_path, 'r') as f:
    for _ in range(2):
      line = f.readline()
      if not line:
        return False
    return True


def extract_errors(errors:str, service_name:str):
    lines = errors.splitlines()
    # print(lines)
    extractions = []
    i = 0
    while i < len(lines):
        # print(f"lines[{i}] = {lines[i]}")
        # if lines[i].startswith(f'File "/{service_name}.py"'):
        if f'File "/{service_name}.py"' in lines[i]:
            extractions.extend([lines[i],lines[i+1], lines[i+2],lines[i+3],"\n"])
            i += 4
        else:
            i +=1
    # print("extractions = ", extractions)
    compressed_errors = '\n'.join(extractions)
    compressed_errors.replace(r'\n','\n')
    # print("compressed_errors = ", compressed_errors)
    return compressed_errors



def extract_requirements(program_string):
    """Extracts a list of required packages from a Python program string.

    Args:
        program_string (str): The Python program string.

    Returns:
        list[str]: A list of required package names.
    """

    try:
        # Parse the program string into an abstract syntax tree (AST)
        tree = ast.parse(program_string)

        # Iterate over the top-level statements in the AST
        imports = []
        for stmt in tree.body:
            if isinstance(stmt, ast.Import):
                # Handle `import` statements
                for alias in stmt.names:
                    imports.append(alias.name)
            elif isinstance(stmt, ast.ImportFrom):
                # Handle `from ... import ...` statements
                imports.append(stmt.module)

        return imports
    except SyntaxError as e:
        print(f"SyntaxError: {e}")
        return []


def generate_requirements_file(program_string, dir):
    """Generates a GT-requirements.txt file based on the extracted packages and store it in directory dir

    Args:
        program_string (str): The Python program string.
        dir (str): The directory in which to store the GT-requirements.txt file.
    """

    required_packages = extract_requirements(program_string)

    if required_packages:
        with open(dir + "/" + "requirements.txt", "w") as f:
            for package in required_packages:
                # if the import statement is of the form "from x.y import z" then just import x
                # am doing this because gpt sometimes generates "from bson.objectid import ObjectId", instead of
                # "from bson import ObjectID".
                match = re.match(r"(\w+)\.\w+", package)
                if match:
                    imp = match.group(1)
                else:
                    imp = package
                # still having problems with importing bson because of conflicts with Flask.  Don't import it
                # similar for os
                if imp == "bson" or imp == 'os':
                    continue
                f.write(f"{imp}\n")
        print(f"Successfully generated a requirements.txt file into directory {dir}.")
    else:
        print("No required packages found in the program.")


#
# f = open("/Users/danielyellin/PycharmProjects/RestGen/automation/generate/24-09-2024?-1650-gpt-35-16k-temp0.3-tok10000/books-s1-v0-runtime-errors.txt", "r")
# input = f.read()
# f.close
# extract_errors(input, "books")
