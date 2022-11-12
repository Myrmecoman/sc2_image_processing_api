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

- If you want to use pytesseract, set the USE_TESSETOCR variable to False in the UI_processor.py script.
- If you want to use tesserocr : https://github.com/sirfz/tesserocr

# Files description
- hotkey_helper : provides functions to easily do actions. This will only work if you have my keybinds (available in the keybinds folder), otherwise you can also change the keys in it to match your hotkeys.
- clicker_helper : provides location to click on the middle or right window of the game.
- units_dictionaries : dictionaries providing useful info corresponding to different units and buildings.
- UI_processor : makes a screenshot of the game and extracts usefull info from UI such as supply, mineral, gas etc.. Also extracts cropped parts of the game (minimap, central window, right window etc...).
- camera_view_processor : uses the game windows captured by the UI_processor, or screenshots it by itself, in order to find element in the camera view window. It can find mineral patches for example, in order to order workers to go back to mining. /!\ Work In Progress
- main : can be used to write testing code to familiarize with the API.
- 4raks_example_bot : a simple bot making a 4 barracks all in using this API. The code is 250 lines long and it is not smart at all but this demonstrates that boting using graphics only is possible ! Be careful this code will not work if you have different keybinds from mine, and I have a French keyboard. You can find my hotkeys in the hotkeys folder, otherwise you can convert every key in the hotkey_helper.py file to match yours.

# Usage prerequisites
This code expects to screenshot a usual 1v1 game against a human or an AI. The minimap colors must be set on Default for you and Default for the enemy (see image below).
This is currently being made for sc2 on a 1920x1080 screen. This is required since the program uses screenshots. I noticed that playing against no one in a custom match changes the minerals / gas / supply info position on the top right hand corner, which breaks the program. This could be supported later.
This code was only tested with terrans so far and will require modifications if you want to use other races since for example the gas icon is different for zergs and will not be detected by this code.

![Recommendations](./readme_images/recommended_colors_and_graphics.png?raw=true "Recommendations")
