# SC2 image processing API
In progress starcraft 2 image processing api to extract data from live sc2 1v1 games.

![Presentation](./templates/presentation.png?raw=true "Presentation")

# The idea behind the project
This api should be able to provide meaningful information in the objective to build a bot afterwards.
It should for example be able to find mineral patches on the minimap and infer on the position of futur expansion bases, or be able to locate and count the number of barracks, factories and spatioports in order to put them in control groups.

# Why python
Python is used for now even though we might need speed to do operations frequently because we might want to use tensorflow to build a learning model afterwards.
Building bindings from C++ to python for the most intensive functions will need to be evaluated.
The objective is 0.5 sec for the whole image segmentation process, in order to leave 1 or 2 sec for the futur bot to perform actions.

# Usage prerequisites
This code expects to screenshot a usual 1v1 game against a human or an AI. The minimap colors must be set on green for you and red for the enemy.
This is currently being made for sc2 on a 1920x1080 screen. This is required since the program uses screenshots. I noticed that playing against no one in a custom match changes the minerals / gas / supply info position on the top right hand corner, which breaks the program. This could be supported later.
This code was only tested with terrans so far but should work with the other races.

# About the OCR (optical character recognition)
Tesserocr is reputed faster and usually more precise than pytesseract, however it is more complicated to install.

- If you want to use pytesseract, set the USE_TESSETOCR variable to False in the screenshot_maker.py script.
- If you want to use tesserocr : https://github.com/sirfz/tesserocr

# Files description
- clicker_helper : provides location to click on the middle or right window of the game.
- units_dictionaries : dictionaries providing useful info corresponding to different units and buildings.
- screenshot_maker : makes a screenshot of the game and extracts usefull info such as supply, mineral, gas etc.. Also extracts cropped parts of the game (minimap, central window, right window etc...).
- main : can be used to write testing code to familiarize with the API.