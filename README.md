# file-visualizer

visualize any file as a png image

REQUIREMENTS: 
  python 3.x
  png module: https://pypi.org/project/pypng/

Version 1:
with this version you have 4 modes

  mode 1:
    step 1: type the name of a file in the same directory as the program
    step 2: type the name of the output png file you want to generate (extension must be ".png" or else the image will not be visable)
    the program will then generate a png image with the file name you inputted in step 2. This PNG image contains all the data within the file as pixels (3 bytes per pixel)
    and the program will autoselect an appropriate image size needed to store all the bytes as well as appending additional null bytes if necessary
    
  mode 2:
    step 1: type the name of a png image that was encoded with this program in mode 1, in the same directory as the program
    step 2: type the name of the file you want to revert the image back to (extension must be the same if you want the file to be usable)
    the program will then convert the png image back into its original file with the specified file name
    
  mode 3 (EXPIRIMENTAL):
    step 1: make sure the config file and all the "generated_image[number].png" files are all in the same directory as the program
    step 2: type in the name of the config file that was generated from this program in mode 4, in the same directory as the program
    the program will process all the image files and generate the original file that the images were created from
    
  mode 4 (EXPIRIMENTAL):
    step 1: type the name of a file in the same directory as the program
    step 2: type in an integer value to be used as the dimesions for the generated images
    the program will generate as many images as necessary to store all the data from the original file. 
    since the images are stuck to a specific size, the program will not lower the dimensions if less space is necessary and will add additional null bytes
    a configuration text file will also be generated as a key to decode the images back to their original state
    
NOTE: MODES 3 AND 4 ARE EXPIRIMENTAL BECAUSE IF THERE ARE NULL BYTES THAT HAPPEN TO BE BETWEEN 2 IMAGES, THE PROGRAM WILL CUT THEM OFF, AND POSSIBLY REMOVE DATA FROM THE FILE MAKING IT CORRPUTED. I HAVE NEVER HAD THIS HAPPEN TO ME PERSONALLY, BUT MAKE SURE THAT BEFORE YOU DELETE THE FILE GENERATED IN MODE 4. CHECK TO MAKE SURE YOU CAN PROPERLY USE MODE 3 TO CONVERT THE IMAGES BACK INTO THE ORIGINAL FILE
