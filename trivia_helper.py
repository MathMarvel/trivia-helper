import csv
import os
from sys import exit

DIR = "csv"
EXT = ".csv"
SEP = "_"
GAME = "game"
LEVEL = "level"
QUESTION = "question"
ANSWER = "answer"
INSTRUCTIONS = "\nEnter keywords separated by spaces.\nCtrl-c to exit.\nCtrl-d to return to previous menu."
ERROR_SELECTION = "Invalid selection. Try again"
EXIT_MSG = "\nExiting..."
EXIT_FILE_FORMAT = "Problem with file formatting. Please make sure the first line contins the text '" + QUESTION + "," + ANSWER + "' (without the quotes), save the file in a plain text editor, and try again."
EXIT_DIR = "Cannot access local '" + DIR + "' directory"
EXIT_FILE = "Cannot access file for inputted values"
EXIT_OPTIONS = "No valid options to choose from."

def main():
    try:
        options = get_options(os.listdir(DIR), EXT, SEP)
    except FileNotFoundError:
        exit(EXIT_DIR)
    selections = choose(options)
    while True:
        if not selections:
            exit(EXIT_MSG)
        game, level = selections
        file = get_file(game, level, DIR, EXT, SEP)
        reader = get_reader(file)
        if QUESTION not in reader.fieldnames or ANSWER not in reader.fieldnames:
            exit(EXIT_FILE_FORMAT)
        print(INSTRUCTIONS)
        while True:
            try:
                keywords = input("Keywords: ").lower().split(" ")
                file.seek(0)
                for answer in match_keywords(reader, keywords, QUESTION, ANSWER):
                    if "|" in answer:
                        print(*sorted(answer.split("|")), sep = "\n")
                        continue
                    print(answer)
            except EOFError:
                file.close()
                print()
                if len([option for option in options if option[0] == game]) == 1:
                    if len(options) == 1:
                        selections = None
                        break
                    preselect = []
                else:
                    preselect = [game]
                selections = choose(options, preselect)
                break
            except KeyboardInterrupt:
                file.close()
                exit(EXIT_MSG)
            
def get_options(files, ext = ".csv", sep = "_"):
    """Retrieves files from a local directory and verifies each file has the inputted extension and naming format, e.g., game_level.csv.

    :param files: List of file names
    :type files: list
    :param ext: The extension of files the function will evaluate
    :type files: str
    :param sep: The separator used to distinguish between words in the filename
    :type sep: str
    :return: A list of lists formed based on the file names, e.g., game_level.csv converts to [game, level].
    :rtype: list
    """
    options = []
    for file in files:
        root = os.path.splitext(file)[0]
        if sep not in root or ext.lower() != os.path.splitext(file)[1].lower():
            continue
        fname_left, fname_right = root.split(sep, maxsplit = 1)
        options.append([fname_left, fname_right])
    return options

def get_file(fname_left, fname_right, dir, ext, sep):
    selected_file = fname_left + sep + fname_right + ext
    try:
        files = os.listdir(dir)
        match = [file for file in files if selected_file.lower() == file.lower()]
        return open(dir + "/" + match[0], "r")
    except FileNotFoundError:
        raise FileNotFoundError("Cannot access directory " + dir)
    except IndexError:
        raise FileNotFoundError("Cannot access file " + selected_file + " in " + dir + " directory")
        
def get_reader(file):
    return csv.DictReader(file)

def match_keywords(reader, keywords, key_search, key_result):
    """Checks which lines from a file contain all strings from an inputted list

    :param reader: Object from the csv.DictReader class.
    :type reader: object
    :param keywords: List of strings.
    :type keywords: list
    :param key_search: Name of dictionary key, entries here are matched against the keywords.
    :type key_search: str
    :param key_result: Name of dictionary key, entries are returned for successful matches between key_search and keywords.
    :type key_result: str
    :raises KeyError: If key_search or key_result keys are not found.
    :return: Strings for all matches from the requested key, done via yield generator.
    :rtype: str
    """
    for row in reader:
        if all(keyword in row[key_search].lower() for keyword in keywords):
            yield row[key_result].upper()

def choose(options, selections = []):
    """An recursive function that takes a nested list as input and assumes that each inner list contains the same number of elements. For each inner list, the 
    user is first given every option from list[0] and asked to make a selection. The inner lists that do not contain the selected value at list[0] are filtered 
    out, and the user is then asked to select an option from list[1] for the remaining lists. This process will repeat n times, where n is the same number of 
    elements in an inner list.

    :param options: A list of lists for the user to select from. See above for a more thorough explanation.
    :type options: list
    :param selections: Optional list of pre-chosen values, i.e., [list[0], list[1], ...] where list[n] represents an element from a nested list in options.
    :type selections: list
    :return: A list containing all of the users choices.
    :rtype: list
    """

    if not isinstance(options, list):
        raise TypeError("Expected type list for options argument, received type " + type(options))
    try:
        options[0]
        [option[0] for option in options]
    except IndexError:
        raise IndexError("options argument must be a nested list, each inner list containing at least one element, i.e., no empty lists")
    results, recur_options, recur_selections = [], [], []
    autoselect = False
    n = len(options[0])
    lst = [option[0] for option in options]
    lst_n = len(set(lst))
    if lst_n < 1:
        exit(EXIT_OPTIONS)
    sel_n = len(selections)
    if sel_n > 1:
        recur_selections = [selections[i] for i in range(1, sel_n)]        
    while True:
        if lst_n == 1:
            choice = lst[0]
            autoselect = True
            print("\nOnly available option", choice.upper(), "selected automatically.")
        elif selections and selections[0] in lst:
            choice = selections[0]
        else:
            try:
                print("\nOptions:", *map(str.upper, sorted(set(lst))))
                choice = input("Choose option: ").strip().lower()
                if choice not in lst:                
                    print(ERROR_SELECTION)
                    continue
            except EOFError:
                print()
                break
            # Ctrl-c used to exit script
            except KeyboardInterrupt:
                exit(EXIT_MSG)
        results.append(choice)
        if n > 1:
            for option in options:
                if option[0] == choice:
                    recur_options.append([option[i] for i in range(1, n)])
            results_recur = choose(recur_options, recur_selections)
            if not results_recur:
                results, selections, recur_selections, recur_options = [], [], [], []
                if autoselect:
                    break
                continue
            results.append(results_recur[0])
        return results

if __name__ == "__main__":
    main()