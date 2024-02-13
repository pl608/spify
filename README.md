# spify
 saves spotifysong by recording and names them correctly
# to use the python file:
1. Install dependencies `pip install pydub pygetwindow mutagen pyaudio`
1. Install ffmpeg/ffprobe to an enviroment variable
2. Start Spotify
3. Start python file
3. Click play on Spotify, the program should sense the action and start recoding
4. When done playing songs pause Spotify, this should cause the program to close
# To use the exe file:
1. Make sure that  ffmpeg/ffprobe are in *the working directory* (or path)
2. Follow python instuctions
## Issues 
### 1. Error -[Errno -9998]:
python: change the input device index to a microphone type(best if you use VB-Cable)
exe: not much you can do... its currently hard coded in
## To build:
First install pyinstaller via pip
```
py -m pip install pyinstaller
pyinstaller main.spec
```
Then running pyinstaller
will build a one-file exe in the directory`./dist`. For further messing around building main.py with the command `pyinstaller main.py` will regenorate the *.spec file and output a multi-file build in `./dist/main`


