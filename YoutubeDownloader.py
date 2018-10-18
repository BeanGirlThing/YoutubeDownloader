import pytube
import prettytable
import configparser
import os

# Dependency imports above


class main:  # Define the main class


    format = None # Create some basic variables the program needs to pass around
    file_format = None
    config_table = None
    videos = []
    video_table = None

    config = configparser.ConfigParser() # Create a config object
    config.read("config.ini") # Read the config file
    download_location = config.get("config","download_location") # Create a variable containing the download location

    def __init__(self): # Define the initializer function

        print("Welcome to Jessica's Youtube video converter")

        if not os.path.isdir(self.download_location): # If the download location path doesnt exist then
            print("Download directory does not exist, please change and retry")
            exit() # Terminate the program

        print("This program uses ffmpeg to work, (If already installed type Y) do you wish to install this program and continue?\n(If no then the program will exit)")
        cont = input("Y/N: ") # Query the user as to wether they are happy for the program to install ffmpeg (if missing)
        if cont.upper() == "Y": # If they agree
            import imageio # Import image IO which will sometimes just randomly jump into installing ffmpeg
            imageio.plugins.ffmpeg.download() # If it doesnt then run the download
        elif cont.upper() == "N": # If the user disagrees
            print("Goodbye!")
            exit() # Terminate the program
        else: # If they put in an unrecognised character or string
            print("Invalid response, assuming N")
            print("Goodbye!")
            exit() # Terminate the program

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

        self.config_table = prettytable.PrettyTable(["Setting","Value"]) # Create the setting table
        if self.format == 0: # If the user wants a video
            self.config_table.add_row(["Output file format","Video ("+self.file_format+")"]) # Create a setting value with video in it
        elif self.format == 1: # If the user wants audio
            self.config_table.add_row(["Output file format","Audio ("+self.file_format+")"]) # Create a setting value with audio in it
        else: # If format is neither, which it never should be
            print("self.format shouldn't have any value apart from 1 or 0 yet it does, "
                  "Quit tampering, "
                  "Terminating program")
            exit() # Terminate the program

        self.config_table.add_row(["Output file location",self.download_location]) # Create a setting value with the download location in it
        self.video_table = prettytable.PrettyTable(["ID", "Title", "URL", "Length", "Views"]) # Create the video table

        while True: # Video adding loop
            print(self.config_table) # Print out the tables made prior for the user to look at
            self.generate_video_table() # Add any new video values to the video table
            print(self.video_table) # Then print the video table
            print("Welcome\n" 
                  "Type a URL and hit enter to have it added to the list\n"
                  "Type 'del <ID>' to remove a video from the list\n"
                  "Type 'com' to download the videos and finish the program\n")

            usr_input = input(">") # Get the users input

            if usr_input[0]+usr_input[1]+usr_input[2] == "del": # If the user tries to delete a value
                try: # Try catch
                    del self.videos[int(usr_input.split(" ")[1])] # Attempt to delete the video assigned to the number the user inputted
                except ValueError: # If the user puts anything in apart from a number
                    print("Value error, make sure you only put in the ID of the video you wish to delete")
                    continue # Repeat the loop
                except IndexError: # If the user inputs a number thats not assigned to a value in the list
                    print("Please input a valid ID")
                    continue # Repeat the loop
                except Exception as e: # If an unexpected error occours
                    print(str(e) + "   Unexpected error!, please try again!")
                    continue # Repeat the loop

            elif usr_input[0]+usr_input[1]+usr_input[2] == "com": # If the user types com
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
            self.video_table.add_row([i,self.videos[i][1],self.videos[i][4],self.videos[i][2],self.videos[i][3]]) # Add values to the video table

    def get_video_information(self,url): # Get video information function
        try: # Try catch
            video = pytube.YouTube(url) # Attempt to get the video object based on the url inputted
            title = video.title # Get the video title
            length = video.length # Get the video length
            views = video.views # Get the videos view total
            video_object = [video,title,length,views,url] # Put all of that information into a list
            return video_object # return that list
        except: # If the URL is invalid
            print("We have run into an error processing the URL\nPlease check that it is correct")
            return None

    def download_and_complete(self): # Download and complete function
        print("Download times can vary depending on your internet connection and the length of the video, this can take quite a while... go get a drink or something")

        if self.format == 0: # If the user wants it in a video format
            for i in range(0,len(self.videos)): # Repeat for the amount of videos that have been added
                print("Downloading - "+self.videos[i][1]) # tell the user the title of the current video being downloaded
                current = self.videos[i][0] # Get the video object created in "get_video_information"
                filenm = self.videos[i][1] # Get the title of the video to be used as the file name
                filenm = "".join([c for c in filenm if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(" ","_") # Make sure that the title is file name friendly

                if self.file_format == ".mp4":
                    current.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download(output_path=self.download_location,filename=filenm) # Download the video
                else:
                    current.streams.filter(progressive=True, file_extension="mp4").order_by("resolution").desc().first().download(output_path=self.download_location,filename=filenm)  # Download the video
                    print("File downloaded, Converting from mp4 to "+self.file_format)
                    os.system('ffmpeg -loglevel panic -i ' + self.download_location + "/" + filenm + ".mp4" + ' ' + self.download_location + "/" + filenm + self.file_format)  # Use FFMPEG to convert the video to .mp3
                    print("Converted! Removing raw download file (This will take tenths of a second)")
                    os.remove(self.download_location+"/"+filenm+".mp4")
                print("Done!")

        elif self.format == 1: # If the user wants it as audio
            for i in range(0,len(self.videos)): # Repeat for the amount of videos that have been added
                print("Downloading - "+self.videos[i][1]) # Tell the user the title of the current video being downloaded
                filenm = self.videos[i][1] # Get the title of the video to be used as the file name
                filenm = "".join([c for c in filenm if c.isalpha() or c.isdigit() or c==' ']).rstrip().replace(" ","_") # Make sure that the title is file name friendly
                current = self.videos[i][0] # get the video object created in "get_video_information"
                current.streams.filter(only_audio=True,file_extension="mp4").desc().first().download(self.download_location,filename=filenm) # Download the video as audio only
                print("File downloaded, converting from mp4 (Audio) to "+self.file_format)
                os.system('ffmpeg -loglevel panic -i ' + self.download_location+"/"+filenm+".mp4" + ' ' + self.download_location + "/" + filenm + self.file_format) # Use FFMPEG to convert the video to .mp3
                print("Removing raw download file (This will take tenths of a second)")
                os.remove(self.download_location+"/"+filenm+".mp4") # Delete the original mp3 file
                print("Done!")



    def select_output_format(self):
        if self.format == 0:
            formats = [".avi",".mp4",".f4v",".flv",".mov",".webm"]
            print("What video format do you want the program to output?\n"
                  "[0] AVI \n"
                  "[1] MP4 \n"
                  "[2] F4V \n"
                  "[3] FLV \n"
                  "[4] MOV \n"
                  "[5] WEBM \n"
                  "Please pick one of the options above by entering their ID")

            while True:
                id = input("(ID)>")
                try:
                    self.file_format = formats[int(id)]
                    break
                except ValueError:
                    print("Please make sure you input a numerical value as the ID")
                    continue
                except IndexError:
                    print("Please make sure you input a number within the range of values")
                    continue
                except:
                    print("An unexpected error has occoured, please check your input and try again")
                    continue

        if self.format == 1:
            formats = [".aac",".mp3",".ogg",".wav",".flac",".m4a"]
            print("What audio format do you want the program to output?\n"
                  "[0] AAC \n"
                  "[1] MP3 \n"
                  "[2] OGG \n"
                  "[3] WAV \n"
                  "[4] FLAC \n"
                  "[5] M4A \n"
                  "Please pick one of the options above by entering their ID")

            while True:
                id = input("(ID)>")
                try:
                    self.file_format = formats[int(id)]
                    break
                except ValueError:
                    print("Please make sure you input a numerical value as the ID")
                    continue
                except IndexError:
                    print("Please make sure you input a number within the range of values")
                    continue
                except:
                    print("An unexpected error has occoured, please check your input and try again")
                    continue




if __name__ == '__main__': # If the program is being run as a script and not imported
    main() # Run the main class
    print("Thank you for using my program\nGoodbye")