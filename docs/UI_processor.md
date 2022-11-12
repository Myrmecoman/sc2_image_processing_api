# In depth explanation of the UI_processor class

The UI_processor class is the main class in charge of screenshoting and processing the interface. It has many variables and is fully multithreaded. It takes about 0.3 sec to run completely, but sometimes you only need 1 information. Therefore you can disable any processing you want and only keep the one you are interested in (for example, how many minerals do i have ?).
This class only have a constructor. You can specify debug=True to generate the segmented images and print the results of the process.
Don't hesitate to read the code, it has comments and the class is quite a short read.


### game

Cropped image of the camera view in the game.

![a](./docs_images/game.png?raw=true "a")

### minimap

Just the cropped minimap.

![a](./docs_images/minimap.png?raw=true "a")

### building

Cropped image of the bottom right screen, corresponding to the building screen for workers, unit production and ability usage.

![a](./docs_images/building.png?raw=true "a")

### selected group

Cropped image of the select units icons.

![a](./docs_images/selected_group.png?raw=true "a")

### supply left and supply right

Left part of the supply info, which is your current supply, right part of the supply info, your max supply. Both are int.

![a](./docs_images/supply.png?raw=true "a")

### minerals

Your bank of minerals. It is an int.

![a](./docs_images/mineral.png?raw=true "a")

### gas

Your bank of gas. It is an int.

![a](./docs_images/gas.png?raw=true "a")

### idle workers

Your number of idle workers. It is an int.

![a](./docs_images/idle_workers.png?raw=true "a")

### army units

Your number of army units. It is an int.

![a](./docs_images/army_units.png?raw=true "a")

### selected single

The name of the selected unit if you only clicked on one. It is a string.

![a](./docs_images/selected_single.png?raw=true "a")

### mineral extraction info

Provides your number of workers on the mineral patches visible on screen. Example : when the game starts you have 12/16 workers. Also provides the location to select the corresponding command center using the mouse. It is a list of ((int, int), (int, int)) corresponding to (( nb_workers/workers_max ), ( position_x, position_y )).

![a](./docs_images/mineral_extraction0.png?raw=true "a")

### gas extraction info

Provides your number of workers on the gas refineries visible on screen. Also provides the location to select the corresponding refinery using the mouse. It is a list of ((int, int), (int, int)) corresponding to (( nb_workers/workers_max ), ( position_x, position_y )).

![a](./docs_images/gas_extraction0.png?raw=true "a")

### base locations

Provides rough base locations on the map. It is a list of tuples (int, int).

### resource mask

An image of the minimap with resources only.

![a](./docs_images/ressources.png?raw=true "a")

### allies mask

An image of the minimap with ally positions only.

![a](./docs_images/allies.png?raw=true "a")

### enemies mask

An image of the minimap with enemy positions only. If the enemy was not scouted it will obviously be empty.

![a](./docs_images/enemies.png?raw=true "a")

### enemy starting base

The enemy starting base position on the minimap. It is a tuple of int.

![a](./docs_images/enemy_location.png?raw=true "a")

### our starting base

Our starting base position on the minimap. It is a tuple of int.

![a](./docs_images/our_location.png?raw=true "a")

### Building availability

Tells if a building is avfailable for construction, this uses saturation values.

![a](./docs_images/building.png?raw=true "a")
![a](./docs_images/right_window_availability.png?raw=true "a")
