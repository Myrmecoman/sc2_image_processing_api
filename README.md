# SC2 image processing API
In progress starcraft 2 image processing api to extract data from live sc2 1v1 games.

WARNING : this is currently being made for sc2 on a 1920x1080 screen. This is required since the program uses screenshots.

# The idea behind the project
This api should be able to provide meaningful information in the objective to build a bot afterwards.
It should for example be able to find mineral patches on the minimap and infer on the position of futur expansion bases, or be able to locate and count the number of barracks, factories and spatioports in order to put them in control groups.

# Why python
Python is used for now even though we might need speed to do operations frenquently since we might want to use tensorflow to build a learning model afterwards.
Building bindings from C++ to python for the most intensive functions will need to be evaluated.
The objective is 0.5 sec for the whole image segmentation process, in order to leave 1 or 2 sec for the futur bot to perform actions.
