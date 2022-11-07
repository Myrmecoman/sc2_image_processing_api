# SC2 image processing API
In progress starcraft 2 image processing api to extract data from live sc2 1v1 games as terran.

![Presentation](./readme_images/presentation.png?raw=true "Presentation")

# The idea behind the project
This api should be able to provide meaningful information in the objective to build a bot afterwards.
It should for example be able to find mineral patches on the minimap and infer on the position of futur expansion bases, or be able to locate and count the number of barracks, factories and spatioports in order to put them in control groups.

# Why python
Python is used for now even though we might need speed to do operations frequently because we might want to use tensorflow to build a learning model afterwards.
Building bindings from C++ to python for the most intensive functions will need to be evaluated.
The objective is 0.5 sec for the whole image segmentation process, in order to leave 1 or 2 sec for the futur bot to perform actions.

# About the OCR (optical character recognition)
Tesserocr is reputed faster and usually more precise than pytesseract, however it is more complicated to install.

- If you want to use pytesseract, set the USE_TESSETOCR variable to False in the screenshot_maker.py script.
- If you want to use tesserocr : https://github.com/sirfz/tesserocr

# Files description
- clicker_helper : provides location to click on the middle or right window of the game.
- units_dictionaries : dictionaries providing useful info corresponding to different units and buildings.
- screenshot_maker : makes a screenshot of the game and extracts usefull info such as supply, mineral, gas etc.. Also extracts cropped parts of the game (minimap, central window, right window etc...).
- main : can be used to write testing code to familiarize with the API.

# Usage prerequisites
This code expects to screenshot a usual 1v1 game against a human or an AI. The minimap colors must be set on Default for you and Default for the enemy (see image below).
This is currently being made for sc2 on a 1920x1080 screen. This is required since the program uses screenshots. I noticed that playing against no one in a custom match changes the minerals / gas / supply info position on the top right hand corner, which breaks the program. This could be supported later.
This code was only tested with terrans so far and will require modifications if you want to use other races since for example the gas icon is different for zergs and will not be detected by this code.

![Recommendations](./readme_images/recommended_colors_and_graphics.png?raw=true "Recommendations")

# In depth explanation of the screenshot_maker class

The screenshot_maker class is the main class in charge of screenshoting and processing the image. It has many variables and is fully multithreaded. It takes about 0.3 sec to run completely, but sometimes you only need 1 information. Therefore you can disable any processing you want and only keep the one you are interested in (for example, how many minerals do i have ?).
This class only have a constructor. You can specify debug=True to generate the segmented images and print the results of the process.

## minimap

Just the cropped minimap.

## game

Cropped image of the camera view in the game.

## building

Cropped image of the bottom right screen, corresponding to the building screen for workers, unit production and ability usage.

## selected group

Cropped image of the select units icons.

## supply left

Left part of the supply info, which is your current supply.

## supply right

Right part of the supply info, your max supply.

## minerals

Your bank of minerals.

## gas

Your bank of gas.

## idle workers

Your number of idle workers.

## army units

Your number of army units.

## selected single

The name of the selected unit if you only clicked on one.

## building authorisation

Wether or not you where allowed to build when trying to.

## mineral extraction info

Provides your number of workers on the mineral patches visible on screen. Example : when the game starts you have 12/16 workers. Also provides the location to select the corresponding command center using the mouse.

## gas extraction info

Provides your number of workers on the gas refineries visible on screen. Also provides the location to select the corresponding refinery using the mouse.

## base locations

Provides rough base locations on the map.

## resource mask

An image of the minimap with resources only.

## allies mask

An image of the minimap with ally positions only.

## enemies mask

An image of the minimap with enemy positions only. If the enemy was not scouted it will obviously empty.