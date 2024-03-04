# spify
Cross-platform program that saves spotify songs by recording them and automaticly naming them from spotify window title (only tested on windows 10)
# to use the python file:
1. Install dependencies `pip install -r ./requirements.txt`
1. Install ffmpeg/ffprobe to an enviroment PATH location
2. Start Spotify
3. Start python file
3. Click play on Spotify, the program should sense the action and start recording
4. When done playing songs pause Spotify, this should cause the program to exit
# To use the exe file:
1. Make sure that  ffmpeg/ffprobe are in the correct directory
2. Follow python instuctions
## Issues 
### 1. Error -[Errno -9998]:
python: change the input device index to a microphone type(best if you use VB-Cable or similar)
## To build:
* install pyinstaller via pip
* put ffmpeg/ffprobe excecutables in working directory
* modify pyaudio/pydub module to look for the ffmpeg/ffprobe excecutables in working directory
* running pyinstaller:
```
py -m pip install pyinstaller
pyinstaller main.spec
```

will build a one-file exe in the directory`./dist`. For further messing around building main.py with the command `pyinstaller main.py` will regenorate the *.spec file and output a multi-file build in `./dist/main`
