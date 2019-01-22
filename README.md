# Image Palettizer
A program that applies a .gpl palette to an image by finding the nearest color in the palette for each pixel using the CIECAM02 UCS color space. This provides more accurate-to-eye results than can be achieved with a run of the mill graphics editor. Just run main.py, and follow the prompts.


## Requirements
Requires Python 3 and the following packages:
- numpy
- imageio
- colorspacious
- tqdm
- qprompt
- psutil


## Installation
Just download the repository and unzip it, or clone with `git clone https://github.com/PureAsbestos/Image-palettizer.git`.


## Usage
To begin, you’ll need two things: a palette in .gpl format, and an image (png, jpeg, etc.) When you run main.py, you’ll get several prompts, asking specifically what you want to do. You can drag and drop files onto the terminal to provide file paths when prompted (remember to hit *Enter*!). The output image will be saved in the subdirectory `./output` as `output-TIMESTAMP.png`. See *Features* for specific capabilities.
### Example
![Mona Lisa Palettization](https://github.com/PureAsbestos/Image-palettizer/blob/master/mona-lisa.png)
Palette can be found here: [Dawnbringer's 16 color palette](http://pixeljoint.com/forum/forum_posts.asp?TID=12795)

## Features
Besides the core features that have been discussed, this program offers:
- The ability to dither with 9 common error-diffusion methods
- The ability to dither with 4 sizes of Bayer matrix (2x2, 3x3, 4x4, 8x8)
- The ability to dither using a loaded image as the threshold matrix (this is especially useful for dithering with a blue-noise texture, but any texture can be used)
- The ability to work with large images (note that *extremely* wide images may take up too much RAM)


## To-do
- Improve code commentary
- Add the ability to run with command-line arguments
- Add a Bayer matrix generator
- Add the ability to work with multiple images, videos, and animated gifs (encode videos as gifs?)
