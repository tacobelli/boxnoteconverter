#!/usr/bin/python
# This file searches for and converts boxnotes to text files
# Written by Tony Iacobelli
# 8/4/2019

import json
import os
import getpass
import platform
import glob


# Ask the user how they would like to use the script
print('How would you like to find the Box Notes that need to be converted?')
print('1: Manually Enter Directory to scan and convert Box Notes in.')
print('2: Search Box Drive directory for Box Notes and automatically convert those files.')
print('3: Search Box Sync directory for Box Notes and automatically convert those files.')
run_mode = int(input('Please enter your selection: '))

# Figure out which run mode we are in and take appropriate actions
if run_mode == 1:
    # Define the box note file name
    print("What is the full path of the directory to scan?")
    print("IMPORTANT: On Windows, all back slashes (\\) must be escaped.")
    print("Do not escape spaces in file names.")
    directory_to_search = input("")
    if (directory_to_search[-1:] == "/") or (directory_to_search[-1:] =="\\"):
        directory_to_search=directory_to_search[:-1]
    platform_name = platform.system()
    if platform_name == "Windows":
        glob_filter = str(directory_to_search + '\\**\\*.boxnote')
    elif platform_name == "Darwin":
        glob_filter = str(directory_to_search + '/**/*.boxnote')
elif run_mode == 2:
    # Get the username of who we are currently running as to find the default box sync directory
    username = getpass.getuser()
    print('Checking if Box Drive Folders exist in their default directories')
    # Get the platform name of what we are running on so we can find the default box sync directory
    platform_name = platform.system()

    # Find the Default Box Drive Directory on Windows
    if platform_name == "Windows":
        box_drive_default_path = str('C:\\Users\\' + username + '\Box')
        does_box_drive_exist = (os.path.exists(box_drive_default_path))

    # Find the Default Box Drive Directory on Mac
    elif platform_name == "Darwin":
        box_drive_default_path = str('/Users/' + username + '/Box')
        does_box_drive_exist = (os.path.exists(box_drive_default_path))

    # Throw an error if we're on something else
    else:
        print('ERROR: Unsupported OS Detected. Exiting')
        exit()

    # If Box Drive isn't in its default directory, ask the user where it is
    if does_box_drive_exist == False:
        print('Unable to detect Box Drive in its default directory.')
        directory_to_search = input('Please enter the full directory you would like to search: ')
        glob_filter = str(directory_to_search + '\**\*.boxnote')
    else:
        print('Found Box Drive default directory, searching there')
        directory_to_search = box_drive_default_path
        glob_filter = str(directory_to_search + '\**\*.boxnote')

elif run_mode == 3:
    # Get the username of who we are currently running as to find the default box sync directory
    username = getpass.getuser()
    print('Checking if the Box Sync Folder exist in its default directory')
    # Get the platform name of what we are running on so we can find the default box sync directory
    platform_name = platform.system()

    #Find the Default Box Sync Directory on Windows
    if platform_name == "Windows":
        box_sync_default_path = str('C:\\Users\\' + username + '\Box Sync')
        does_box_sync_exist = (os.path.exists(box_sync_default_path))

    # Find the Default Box Sync Directory on Mac
    elif platform_name == "Darwin":
        box_sync_default_path = str('/Users/' + username + '/Box Sync')
        does_box_sync_exist = (os.path.exists(box_sync_default_path))

    #Throw an error if we're on something else
    else:
        print('ERROR: Unsupported OS Detected. Exiting')
        exit()

    #If Box Sync isn't in its default directory, ask the user where it is
    if does_box_sync_exist == False:
        print('Unable to detect Box Sync in its default directory.')
        directory_to_search = input('Please enter the full directory you would like to search: ')
        glob_filter = str(directory_to_search + '/**/*.boxnote')
    else:
        print('Found Box Sync default directory, searching there')
        directory_to_search = box_sync_default_path
        glob_filter = str(directory_to_search + '/**/*.boxnote')
else:
    print('ERROR: Number was not in range, exiting.')
    exit()

#Search either Box Sync or Box Drive directories for Box Notes
print(glob_filter)
boxnotes_to_convert=(glob.glob(glob_filter,recursive=True))

for boxnote_file_name in boxnotes_to_convert:
    # Open The Box Note file in read only mode
    print('Converting ',boxnote_file_name)
    raw_file = open(boxnote_file_name, "r")

    # Read the file
    file = raw_file.read()

    # Make the File a Nested Dictionary
    json_file = json.loads(file)

    # Define what the actual content of the note is
    note_content = (json_file['atext']['text'])

    # Create a new file that is a txt file with the same name
    converted_file_name = boxnote_file_name.replace('.boxnote', '.txt')

    # Make sure that there is not already a file that exists with that same name
    file_exists_check = (os.path.exists(converted_file_name))
    # file_exists_check=True
    if file_exists_check == True:
        print('There is a file already named', converted_file_name,'! Here are your options:')
        print('1: Exit')
        print('2: Overwrite the existing file')
        what_to_do = int(input('Please type the number of the option you would like: '))
        if what_to_do == 1:
            exit()
        elif what_to_do == 2:
            print('Overwriting Existing File.')
        else:
            print('ERROR: number was not in range. Exiting...')
            exit()

    # Output Results to the specified file
    output_file = open(converted_file_name, "w+")
    output_file.write(note_content)
    output_file.close()
    print('Done, moving to next file.')
print('All files found and converted, exiting.')
exit()
