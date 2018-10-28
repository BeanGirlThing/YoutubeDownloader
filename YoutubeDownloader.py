import pytube
import prettytable
import configparser
import os
import imageio

# Dependency imports above


class main:  # Define the main class


    format = None # Create some basic variables the program needs to pass around
    file_format = None
    config_table = None
    videos = []
    video_table = None
    extra_dir = ""
    download_interface = []
    ffmpeg_executable = None

    config = configparser.ConfigParser() # Create a config object
    config.read("config.ini") # Read the config file
    download_location = config.get("config","download_location") # Create a variable containing the download location
    ffmpeg_permission = config.get("config","allow_ffmpeg_download") # Create a variable containing the value for 'allow_ffmpeg_download' in config

    def __init__(self): # Define the initializer function

        print("Welcome to Jessica's Youtube video converter") # Welcome message

        if not os.path.isdir(self.download_location): # If the download location path doesnt exist then
            self.close_with_message("Download directory does not exist, please change and retry") # Close the program with this message

        if self.ffmpeg_permission.upper() != "TRUE": # If the user has set 'allow_ffmpeg_download' to anything but true
            self.close_with_message("\nThe setting 'allow_ffmpeg_download' is set to "+self.ffmpeg_permission+"," #Close the program with this message
                                    " the setting needs to be 'true' for the program"
                                    " to work\n\nEnabling this setting will install ffmpeg"
                                    " the next time you start this program (Unless you"
                                    " already have FFMPEG installed\n")
        else: # If the config option is set to true
            imageio.plugins.ffmpeg.download("./") # Download ffmpeg in current folder
            for files in os.walk("./ffmpeg"): # Identify files in folder download created to contain ffmpeg
                for filename in files: # For every file name
                    if "exe" in str(filename): # If its the executable
                        self.ffmpeg_executable = str(filename[0]) # set the global definition of ffmpeg_executable to the filename


        while True: # Loop to query the user on whether they want the output files to be in audio or video format
            typeofoutput = input("Do you want the output files to be video [V] or audio [A]? ")
            if typeofoutput == "video" or typeofoutput == "v" or typeofoutput == "V": # If the user wants it as a video
                self.format = 0 # Set self.format to 0 implying "video" to the program
                break # Break the loop
            elif typeofoutput == "audio" or typeofoutput == "a" or typeofoutput == "A": # If the user wants audio
                self.format = 1 # Set self.format to 1 implying "audio" to the program
                break # Break the loop
            else: # If the input is unrecognised
                print("Please input either 'video', 'audio', 'v' or 'a' ")
                continue # Repeat the loop

        self.select_output_format()

        self.config_table = prettytable.PrettyTable(
            [
                "Setting",
                "Value"
            ]
        ) # Create the setting table
        if self.format == 0: # If the user wants a video
            self.config_table.add_row(
                [
                    "Output file format",
                    "Video ("+self.file_format+")"
                ]
            ) # Create a setting value with video in it
        elif self.format == 1: # If the user wants audio
            self.config_table.add_row(
                [
                    "Output file format",
                    "Audio ("+self.file_format+")"
                ]
            ) # Create a setting value with audio in it
        else: # If format is neither, which it never should be
            self.close_with_message("self.format shouldn't have any value apart from 1 or 0 yet it does, "
                                    "Quit tampering, "
                                    "Terminating program")

        self.config_table.add_row(
            [
                "Output file location",
                self.download_location
            ]
        ) # Create a setting value with the download location in it
        self.config_table.add_row(
            [
                "Sub Directory",
                "None"
            ]
        ) # Create a setting value with the sub directory set to none

        self.video_table = prettytable.PrettyTable(
            [
                "ID",
                "Title",
                "URL",
                "Length",
                "Views"
            ]
        ) # Create the video table

        while True: # Video adding loop
            print("\n"*50) # Clear the screen just to make it a bit easier to understand for the user
            print(self.config_table) # Print out the tables made prior for the user to look at
            self.generate_video_table() # Add any new video values to the video table
            print(self.video_table) # Then print the video table
            print("\nWelcome\n\n" 
                  "Type a URL and hit enter to have it added to the list\n"
                  "Type 'remove <ID>' to remove a video from the list\n" 
                  "Type 'complete' to download the videos and finish the program\n" 
                  "Type 'sldir <Name>' to select an existing directory (Must be in the root download folder)"
                  " and have downloads sent there instead\n" 
                  "Type 'exdir <Name>' to create a new directory in the download folder"
                  " and have downloads sent there instead\n"
                  "Type 'cldir' to clear the selected directory\n"
                  "Type 'exit' to exit the program\n")

            usr_input = input(">") # Get the users input

            if usr_input.split(" ")[0] == "exit": # If the user types exit

                self.close_with_message("Goodbye!")

            if usr_input.split(" ")[0] == "exdir": # If the user types exdir
                try: # Try catch

                    file_friendly_name = "".join(
                        [
                            c for c in usr_input.split(" ")[1] if c.isalpha() or c.isdigit() or c==' ']
                    ).rstrip().replace(
                        " ",
                        "_"
                    ) # Make sure the name given is directory friendly

                    os.mkdir(self.download_location+"/"+file_friendly_name) # Create a directory using that name
                    self.extra_dir = "/"+file_friendly_name # Set the 'extra_dir' value to that directory
                    self.config_table.del_row(2) # Update the config table...
                    self.config_table.add_row(
                        [
                            "Sub Directory",
                            self.extra_dir
                        ]
                    ) # With the new sub directory value
                except IndexError: # If the user just types 'exdir' and nothing else
                    print("Please make sure you input a name for the folder")
                    input("Press enter to continue")
                except OSError: # If the directory already exists
                    print("Directory already exists, please use 'sldir <Name>' instead")
                    input("Press enter to continue")

            elif usr_input.split(" ")[0] == "cldir": # If the user types cldir
                if self.extra_dir == "": # If self.extra_dir is empty
                    print("Sub directory hasnt been selected therefore cannot be reset, no action taken")
                    input("Press enter to continue")
                    continue
                else: # Otherwise
                    self.extra_dir = "" # Reset self.extra_dir
                    self.config_table.del_row(2) # Delete the row contining the data
                    self.config_table.add_row(
                        [
                            "Sub Directory",
                            "None"
                        ]
                    ) # Add the row back with the updated information
                    continue

            elif usr_input.split(" ")[0] == "sldir": # If the user types sldir
                if os.path.isdir(self.download_location+"/"+usr_input.split(" ")[1]): # Check that the directory they are requesting to select exists
                    self.extra_dir = "/"+usr_input.split(" ")[1] # Set self.extra_dir to the directory the user selected
                    self.config_table.del_row(2) # Delete the row containing the old data
                    self.config_table.add_row(
                        [
                            "Sub Directory",
                            self.extra_dir
                        ]
                    ) # Replace it with new data

                else: # If the path doesnt exist
                    print("The path "+self.download_location+"/"+usr_input.split(" ")[1]+" Does not exist")
                    input("Press enter to continue")


            elif usr_input.split(" ")[0] == "remove": # If the user tries to delete a value
                try: # Try catch
                    del self.videos[
                        int(
                            usr_input.split(" ")[1]
                        )
                    ] # Attempt to delete the video assigned to the number the user inputted

                except ValueError: # If the user puts anything in apart from a number
                    print("Value error, make sure you only put in the ID of the video you wish to delete")
                    input("Press enter to continue")

                    continue # Repeat the loop

                except IndexError: # If the user inputs a number thats not assigned to a value in the list
                    print("Please input a valid ID")
                    input("Press enter to continue")

                    continue # Repeat the loop

                except Exception as e: # If an unexpected error occours
                    print(str(e) + "   Unexpected error!, please try again!")
                    input("Press enter to continue")

                    continue # Repeat the loop

            elif usr_input.split(" ")[0] == "complete": # If the user types com
                self.download_and_complete() # Begin downloading the videos into the desired formats
                break

            else: # If neither options are chosen the program will assume it is a link to a video
                curr_video = self.get_video_information(usr_input) # Run the get video information function
                if curr_video == None: # If "get_video_information" returns None
                    continue # Repeat the loop
                self.videos.append(curr_video) # Otherwise append the value returned to the videos list

    def generate_video_table(self): # Generate video table function
        self.video_table.clear_rows() # Clear any current values from the video table
        for i in range (0,len(self.videos)): # Repeat until every value in the videos list is on the video table
            self.video_table.add_row(
                [
                    i,
                    self.videos[i][1],
                    self.videos[i][4],
                    self.videos[i][2],
                    self.videos[i][3]
                ]
            ) # Add values to the video table

    def get_video_information(self,url): # Get video information function
        try: # Try catch
            video = pytube.YouTube(url) # Attempt to get the video object based on the url inputted
            title = video.title # Get the video title
            length = video.length # Get the video length
            views = video.views # Get the videos view total
            video_object = [
                video,
                title,
                length,
                views,
                url
            ] # Put all of that information into a list
            return video_object # return that list

        except: # If the URL is invalid
            print("We have run into an error processing the URL\nPlease check that it is correct")
            input("Press enter to continue")
            return None

    def download_and_complete(self): # Download and complete function

        self.download_interface = [
            prettytable.PrettyTable(
                [
                    "In queue"
                ]
            ),
            prettytable.PrettyTable(
                [
                    "Video Title",
                    "Progress"
                ]
            ),
            prettytable.PrettyTable(
                [
                    "Complete"
                ]
            )
        ] # Create tables appropriate for the down

        for i in range(0,len(self.videos)): # Repeat for the number of items in the self.videos list

            self.download_interface[0].add_row(
                [
                    self.videos[i][1]
                ]
            ) # Add a row to the queue table containing the title for the video corrisponding to the number of i

        if self.format == 0: # If the user wants it in a video format

            for i in range(0,len(self.videos)): # Repeat for the amount of videos that have been added

                self.print_download_tables() #Print the download interface

                self.download_interface[0].del_row(0) # Delete the top value from the queue table
                self.download_interface[1].add_row(
                    [
                        self.videos[i][1],
                        "Downloading"
                    ]
                ) # Add that value back on the in progress table

                self.print_download_tables() # Print out the download interface

                current = self.videos[i][0] # Get the video object created in "get_video_information"

                filenm = self.videos[i][1] # Get the title of the video to be used as the file name
                filenm = "".join(
                    [
                        c for c in filenm if c.isalpha() or c.isdigit() or c==' '
                    ]
                ).rstrip().replace(
                    " ",
                    "_"
                ) # Make sure that the title is file name friendly

                if not os.path.isdir(self.download_location+self.extra_dir): # If the path to the output directory no-longer exists
                    self.close_with_message("Directory being used to output the downloads no-longer exists,"
                                            " terminating program")

                if self.file_format == ".mp4": # If the user has selected mp4 as their file format
                    current.streams.filter(
                        progressive=True,
                        file_extension="mp4"
                    ).order_by(
                        "resolution"
                    ).desc().first().download(
                        output_path=self.download_location
                                    +self.extra_dir,
                        filename=filenm
                    ) # Download the video

                else: # Otherwise
                    current.streams.filter(
                        progressive=True,
                        file_extension="mp4"
                    ).order_by(
                        "resolution"
                    ).desc().first().download(
                        output_path=self.download_location+self.extra_dir,
                        filename=filenm
                    ) # Download the video

                    self.download_interface[1].clear_rows() # Clear the in progress table
                    self.download_interface[1].add_row(
                        [
                            self.videos[i][1],
                            "Converting file formats"
                        ]
                    ) # Replace that with a new value
                    self.print_download_tables() # Print the download tables


                    os.system(
                        '.\\ffmpeg\\'
                        +self.ffmpeg_executable
                        + ' -loglevel panic -i '
                        + self.download_location
                        + self.extra_dir
                        + "/"
                        + filenm
                        + ".mp4"
                        + ' '
                        + self.download_location
                        + self.extra_dir
                        + "/"
                        + filenm
                        + self.file_format
                    )  # Use FFMPEG to convert the video to .mp3

                    self.download_interface[1].clear_rows() # Clear the in progress table
                    self.download_interface[1].add_row(
                        [
                            self.videos[i][1],
                            "Deleting temporary files"
                        ]
                    ) # Replace that with a new value
                    self.print_download_tables() # Print the download tables

                    os.remove(
                        self.download_location
                        + self.extra_dir
                        + "/"
                        + filenm
                        + ".mp4"
                    ) # Delete the temporary files

                self.download_interface[2].add_row(
                    [
                        self.videos[i][1]
                    ]
                ) # Add a row to the complete table containing the video that just completed
                self.download_interface[1].clear_rows() # Clear the progress table

        elif self.format == 1: # If the user wants it as audio

            for i in range(0,len(self.videos)): # Repeat for the amount of videos that have been added

                self.print_download_tables() # Print the download tables

                self.download_interface[0].del_row(0) # Clear the top row from the queue table
                self.download_interface[1].add_row(
                    [
                        self.videos[i][1],
                        "Downloading"
                    ]
                ) # Add the value just removed to the in progress table

                self.print_download_tables() # Print the download tables

                if not os.path.isdir(self.download_location+self.extra_dir): # Check the download path still exists
                    self.close_with_message("Directory being used to output the downloads no-longer exists,"
                                            " terminating program")

                filenm = self.videos[i][1] # Get the title of the video to be used as the file name
                filenm = "".join(
                    [
                        c for c in filenm if c.isalpha() or c.isdigit() or c==' '
                    ]
                ).rstrip().replace(
                    " ",
                    "_"
                ) # Make sure that the title is file name friendly

                current = self.videos[i][0] # get the video object created in "get_video_information"
                current.streams.filter(
                    only_audio=True,
                    file_extension="mp4"
                ).desc().first().download(
                    output_path=self.download_location
                                + self.extra_dir,
                    filename=filenm
                ) # Download the video as audio only

                self.download_interface[1].clear_rows() # Clear the progress table
                self.download_interface[1].add_row(
                    [
                        self.videos[i][1],
                        "Converting file formats"
                    ]
                ) # Replace that with a new value
                self.print_download_tables() # Print the download tables

                os.system(
                    '.\\ffmpeg\\'
                    +self.ffmpeg_executable
                    +' -loglevel panic -i '
                    + self.download_location
                    + self.extra_dir
                    + "/"+filenm+".mp4"
                    + ' '
                    + self.download_location
                    + self.extra_dir
                    + "/"
                    + filenm
                    + self.file_format
                ) # Use FFMPEG to convert the video to .mp3

                self.download_interface[1].clear_rows() # Clear the progress table
                self.download_interface[1].add_row(
                    [
                        self.videos[i][1],
                        "Deleting temporary files"
                    ]
                ) # Replace that with a new value
                self.print_download_tables() # Print out the download tables

                os.remove(self.download_location+ self.extra_dir +"/"+filenm+".mp4") # Delete the original mp3 file

                self.download_interface[2].add_row(
                    [
                        self.videos[i][1]
                    ]
                ) # Add the new completed video to the complete table
                self.download_interface[1].clear_rows() # Clear the progress table

        self.print_download_tables() # Print out the tables
        input("Press enter to continue")

    def print_download_tables(self): # Print download tables function
        print("\n"*50) # Clear the screen
        print("Download times can vary depending on your internet connection and the length of the video,"
              " this can take quite a while... go get a drink or something")
        for i in range(0,len(self.download_interface)): # Repeat for the number of items in the download interface list
            print(self.download_interface[i]) # Print out the table corrisponding to i

    def select_output_format(self): # Output format selection dialogue
        if self.format == 0: # If they want a video output
            formats = [
                ".avi",
                ".mp4",
                ".f4v",
                ".flv",
                ".mov",
                ".webm"
            ] # Define all of the acceptable formats
            print("What video format do you want the program to output?\n"
                  "[0] AVI \n"
                  "[1] MP4 \n"
                  "[2] F4V \n"
                  "[3] FLV \n"
                  "[4] MOV \n"
                  "[5] WEBM \n"
                  "Please pick one of the options above by entering their ID")

            while True: # Loop
                id = input("(ID)>") # Ask the user what file type they want
                try: # Try catch
                    self.file_format = formats[
                        int(
                            id
                        )
                    ] # Set their input as the self.file_format value
                    break # If it works then break the loop
                except ValueError: # If they put any value apart from a number
                    print("Please make sure you input a numerical value as the ID")
                    continue # Repeat the loop
                except IndexError: # If they put an option that is out of the range of the options
                    print("Please make sure you input a number within the range of values")
                    continue # Repeat the loop
                except: # If theres an unexpected error
                    print("An unexpected error has occoured, please check your input and try again")
                    continue # Repeat the loop

        if self.format == 1: # If the want an audio output
            formats = [
                ".aac",
                ".mp3",
                ".ogg",
                ".wav",
                ".flac",
                ".m4a"
            ] # Define all of the acceptable formats
            print("What audio format do you want the program to output?\n"
                  "[0] AAC \n"
                  "[1] MP3 \n"
                  "[2] OGG \n"
                  "[3] WAV \n"
                  "[4] FLAC \n"
                  "[5] M4A \n"
                  "Please pick one of the options above by entering their ID")

            while True: # Loop
                id = input("(ID)>") # Ask the user what file type they want
                try: # Try catch
                    self.file_format = formats[
                        int(
                            id
                        )
                    ] # Set their input as the self.file_format value
                    break # Break the loop
                except ValueError: # Id they put any value apart from a number
                    print("Please make sure you input a numerical value as the ID")
                    continue # Repeat the loop
                except IndexError: # If they put an option that is out of the range of options
                    print("Please make sure you input a number within the range of values")
                    continue # Repeat the loop
                except: # If theres an unexpected error
                    print("An unexpected error has occoured, please check your input and try again")
                    continue # Repeat the loop

    def close_with_message(self,message): # Define the close with message function
        print(message) # Print the message that was inputted
        input("Press enter to exit")
        exit() # Terminate the program


if __name__ == '__main__': # If the program is being run as a script and not imported
    main() # Run the main class
    print("Thank you for using my program\nGoodbye")
    input("Press enter to exit")
