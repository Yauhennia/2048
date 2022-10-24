# 2048
2048 is console game which is written in Python and uses some Python modules:
- module click is used to parametrize the game:
    to set the number of rows and columns of the playing field,
    to set height and width of the cells, 
    to load the previous game.
    
    Use --help to see details

- module keyboard is used to enable the use of such buttons as up, down, left, right, escape.
- module json is used to save score information and the ability to load the previous game
- module copy to ‘deepcopy’ the data
- try – except is used to exclude an error, when json file is missed
