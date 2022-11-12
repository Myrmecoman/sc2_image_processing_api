# In depth explanation of the cam_processor class

This class should be able to extract any information from the game window that is basically doable without a convolutional neural network. It can do color based detection to find mineral patches for example.

### mineral_patches

Provides screen positions of mineral patches. It is a list of tuples of type (int, int).
For now this fails to see the smallest patches since they are similar in size with the mineral harvested by the workers and I must filter those. It also does not find yellow minerals for now.

![a](./docs_images/mineral_patches.png?raw=true "a")

### Building authorized

Tells if the building is authorized to be built here. This detects the red markings on the game screen.
