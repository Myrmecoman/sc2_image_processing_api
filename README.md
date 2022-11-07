# SC2 image processing API
In progress starcraft 2 image processing api to extract data from live sc2 1v1 games as terran.

![Presentation](./readme_images/presentation.png?raw=true "Presentation")

# The idea behind the project
This api should be able to provide meaningful information in the objective of building a bot afterwards.
It should for example be able to find mineral patches on the minimap and infer on the position of futur expansion bases, or be able to locate and count the number of barracks, factories and spatioports in order to put them in control groups.

WARNING : some infos can be wrong or absent during the segmentation ! You have to make your own checks when using the code since the class can fail to get some infos.

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
Don't hesitate to read the code, it has comments and the class is quite small.


## game

Cropped image of the camera view in the game.

![a](./readme_images/game.png?raw=true "a")

## minimap

Just the cropped minimap.

![a](./readme_images/minimap.png?raw=true "a")

## building

Cropped image of the bottom right screen, corresponding to the building screen for workers, unit production and ability usage.

![a](./readme_images/building.png?raw=true "a")

## selected group

Cropped image of the select units icons.

![a](./readme_images/selected_group.png?raw=true "a")

## supply left and supply right

Left part of the supply info, which is your current supply, right part of the supply info, your max supply.

![a](./readme_images/supply.png?raw=true "a")

## minerals

Your bank of minerals.

![a](./readme_images/mineral.png?raw=true "a")

## gas

Your bank of gas.

![a](./readme_images/gas.png?raw=true "a")

## idle workers

Your number of idle workers.

![a](./readme_images/idle_workers.png?raw=true "a")

## army units

Your number of army units.

![a](./readme_images/army_units.png?raw=true "a")

## selected single

The name of the selected unit if you only clicked on one.

![a](./readme_images/selected_single.png?raw=true "a")

## mineral extraction info

Provides your number of workers on the mineral patches visible on screen. Example : when the game starts you have 12/16 workers. Also provides the location to select the corresponding command center using the mouse.

![a](./readme_images/mineral_extraction0.png?raw=true "a")

## gas extraction info

Provides your number of workers on the gas refineries visible on screen. Also provides the location to select the corresponding refinery using the mouse.

![a](./readme_images/gas_extraction0.png?raw=true "a")

## base locations

Provides rough base locations on the map. It is a list of tuples (x, y).

## resource mask

An image of the minimap with resources only.

![a](./readme_images/ressources.png?raw=true "a")

## allies mask

An image of the minimap with ally positions only.

![a](./readme_images/allies.png?raw=true "a")

## enemies mask

An image of the minimap with enemy positions only. If the enemy was not scouted it will obviously be empty.

![a](./readme_images/enemies.png?raw=true "a")
