from __future__ import print_function  # ensures print function compatibility with Python3
import numpy as np

# safely deal with file paths
import os

# library for loading the image
from nipy.core.api import Image          # for Image object
from nipy import load_image, save_image  # for loading and saving .nii.gz images
from nipype.interfaces import dcmstack   # for saving the file

# library for viewing the image
import matplotlib.pyplot as plt

#-------------------------------------------------------------------------------
# FUNCTION DEFINITIONS
#-------------------------------------------------------------------------------

def remove_keymap_conflicts(new_keys_set):
    for prop in plt.rcParams:
        if prop.startswith('keymap.'):
            keys = plt.rcParams[prop]
            remove_list = set(keys) & new_keys_set
            for key in remove_list:
                keys.remove(key)

"""
Generate an image volume slice viewer

@param volume Image volume data
"""
def multi_slice_viewer(volume):
    # Matplotlib has some functions attached to keys, so make sure we overwrite them
    remove_keymap_conflicts({'j', 'k'})
    fig, ax = plt.subplots()
    # assign the volume to the axis for the figure
    ax.volume = volume
    # set the index of the slice to display - initialize to the halfway point
    print(volume.shape)
    ax.index = volume.shape[2] // 2
    # show the image slice
    ax.imshow(volume[:, :, ax.index])
    print("Displaying slice:", ax.index)
    # attach the key press event monitoring function to the figure
    fig.canvas.mpl_connect('key_press_event', process_key)

"""
Handle key press events

@param event A key press event
"""
def process_key(event):
    # Since this function is attached to a figure now, we need to grab the context for that figure
    fig = event.canvas.figure
    ax = fig.axes[0]
    
    # handle key press events
    if event.key == 'j':
        previous_slice(ax)
    elif event.key == 'k':
        next_slice(ax)
        
    # draw the updated figure
    fig.canvas.draw()
    
"""
Change the slice of the volume being displayed
to the previous slice

@param ax The axis handle for the figure where the image is being displayed
"""
def previous_slice(ax):
    # get the volume being displayed
    volume = ax.volume
    # change the index of the volume being displayed
    ax.index = (ax.index - 1) % volume.shape[2] # the modulus division enables wrapping the scrolling
    print("Changing to slice:", ax.index)
    # change the slice being displayed
    ax.images[0].set_array(volume[:, :, ax.index])

"""
Change the slice of the volume being displayed
to the next slice

@param ax The axis handle for the figure where the image is being displayed
"""
def next_slice(ax):
    # get the volume being displayed
    volume = ax.volume
    # change the index of the volume being displayed
    ax.index = (ax.index + 1) % volume.shape[2] # the modulus division enables wrapping the scrolling
    print("Changing to slice:", ax.index)
    # change the slice being displayed
    ax.images[0].set_array(volume[:, :, ax.index])


def main():
    # turn interactive plotting on
    plt.ion()

    # Specify the path to the file
    path = "BOLD.nii"
    path = os.path.abspath(path)
    print(path)  # Python3 syntax for printing

    # Make sure that the file exists and is actually a file
    if not os.path.exists(path) or not os.path.isfile(path):
        print("The filename entered is invalid")

    # Load the image sequence
    sequence = load_image(path)

    # Grab the data for one volume directly from the sequence
    imageVolume = sequence.get_data()[:,:,:,0]

    # Now view the image using the above functions
    multi_slice_viewer(imageVolume)

    # Keep the program from closing itself until the user hits Enter
    raw_input("Press Enter to exit")

if __name__ == '__main__':
    main()
