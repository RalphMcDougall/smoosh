# Smoosh

This is a tool for concatenating a collection of photos and videos into one video that can be shared.

## Installation
Clone this repo, then run `setup.bat` in command prompt to install the dependencies. 
It will be useful to add the repo to your system path to allow the tool to be run from any directory.
On Windows this is done through searching for "Edit the system environment variables" and then selecting "Environment Variables". Select "Path" under the user variables, then "Edit", then "New". Enter the full path to the repo, and then save / apply all changes. You will now have to restart your command prompt before it will work.

Linux support still needs to be added, but it should be easy enough...

## Running the tool
In command prompt, navigate to a directory containing _only_ the photos and videos that are to be concatenated. If you have added the repo to your system path, you can run `smoosh` and it will start. Note that the tool applies a whitelist on the prefixes and file types. 

A video file with the name of the directory will be created. 

## The order of the photos and videos
The primary use-case for this tool is for me to concatenate media from my action camera. The date / time associated with each item is entirely inconsistent as it resets its internal time for some reason. As such, the files are assumed to be in the order of the number contained within their name. On my camera the names of the files is a short prefix followed by a number indicated the entry of the item in the camera's gallery. This is what is used to order the photos / videos.