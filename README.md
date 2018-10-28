# Youtube Downloader

Small project I have been working on this week that is now fully operational, It does exactly what the title
says, it downloads youtube videos into either an audio or video format

The executable version of the program can be found [here :heart:](https://github.com/Merhlim/YoutubeDownloader/wiki/Executable)

## Features

* Allows you to queue multiple videos for download
* No ad's!
* Allows download into both audio and video forms
* Allows the selection of multiple different file types (flac, ogg, webm, wav, e.t.c.)

## FFMPEG

This program uses FFMPEG to work

The program should install it itself if it detects that FFMPEG is missing

If that fails then manually install it from [here](https://ffmpeg.zeranoe.com/builds/) and add it to your 
computers PATH

Please contact me if you have any issues --> [Contact](http://merhlim.me/)

## Special thanks

The writer of [Pytube](https://pypi.org/project/pytube/) @nficano

The writers of [PrettyTable](https://pypi.org/project/PrettyTable/) 

The writers of [Configparser](https://pypi.org/project/configparser/)

The writers of [Imageio](https://pypi.org/project/imageio/) @imageio

And of course [FFMPEG](https://ffmpeg.zeranoe.com/builds/)

:heart:

## Installation

If your running the program from source then it requires these python modules:
* pytube
* configparser
* prettytable
* imageio

Which can all be installed from pypy (pip install)

Make sure you put the installation location into the config file otherwise the program will exit
