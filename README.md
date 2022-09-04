# Trivia Helper

## Video Overview: https://youtu.be/SuShHr8dCx8

#### How to Use:
In order to run this script, you'll need Python installed on your system, and you'll need to be able to utilize a command line. I'll leave it to you to figure that out, but a nice simple GUI version is planned for the relatively-near future.

The utility works simply by searching its local directory for a 'csv' folder.
Files in the 'csv' folder require the following in order for the utility to make use of them:
- Contain a filename of the format 'game_level.csv'
- The first row contains the entry 'question,answer' as these are the default keys used by the utility
- NOTE: If the utility does not open the file despite meeting the above requirements, then try to copy and paste the entire contents of the file into a plain text editor and re-save the file. Saving the CSV file using a word-processing program may cause formatting issues.

Once the utility can read at least one file, it will allow you to select the game and level if multiple options are available.
You will then be met with a 'Keywords' prompt. Enter any useful keywords, separated by spaces. All lines from the 'question' column in the spreadsheet that contain all of the entered keywords will be considered a match, and the associated 'answer' column for all matching lines will be immediately displayed for you.
Whether or not any results are returned, you will be prompted again to enter keywords and repeat the process. Pressing Ctrl-d will exit the script.

Hold Ctrl-d to back up and select another game/level. Press Ctrl-c to quit the script.

#### Features and Design Choices:
For a question that has multiple answers, it is recommended to format the CSV file so that all answers are separated by a pipe '|' delimiter, e.g., question,answer3|answer1|answer2. If this formatting is used, the script will automatically sort the matching answers alphabetically and print each answer on a new line to assist with readability, e.g., entering 'question' in the example above outputs the following:
- answer1
- answer2
- answer3

The code automatically searches the local 'csv' directory and uses the filenames to sort by game and level. This was done as most of the trivia games I am familiar with, e.g., Trivia Murder Party, contain separate and distinct levels. Having all of the data in a single file could cause overlap and confusion, especially since some levels expect a single correct answer, but others are multiple-choice.
- If you prefer to have all of the game data in a single file and ignore level differences, then feel free to name files along the lines of 'game_all.csv' or similar.

It is extremely easy to add support for other games and applications. Just put a properly-formatted CSV file into the correct directory, and the script will take care of the rest.
The yield generator is used to return matches to allow for extremely large spreadsheets and amount of data to be searched.

#### Future Plans:
Next items on the list are getting a GUI and binary files compiled for ease of access. The more people "doing well" at trivia, the better. >=)

#### Background:
I hate trivia, so I decided to beat it.
