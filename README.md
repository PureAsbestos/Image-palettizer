# Image palettizer
A program that applies a .gpl palette to an image by finding the nearest color using the cam02 color space. Just run main.py, and follow the prompts.


REQUIREMENTS:
Requires Python 3 with the NumPy, imageio, and colorspacious packages.


INSTALLATION:
Just download the repository and unzip it.


USAGE:
You’ll need two things, a palette in .gpl format, and an image (png, jpeg, etc.) When you run main.py, you’ll get a prompt asking, “Where is the palette?” You’ll need to provide the file path to a valid .gpl file at this point. You can most likely drag and drop the file onto the terminal to accomplish this. Then, it will ask, “Where is the image?” Provide the image path. The program will then apply the palette to the image by finding the closest color in the palette for each pixel. The output image will be saved in the same directory as main.py as ‘output.png.’


TODO:
- Add example images.
- Improve code commentary.
- Squash a bug that causes the output image to have slightly incorrect coloring.
