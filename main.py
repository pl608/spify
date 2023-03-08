from pydub import AudioSegment
from pyaudio import PyAudio, paInt16
from time import sleep
import pygetwindow as gw
import os
import wave
#from  eyed3 import id3
#import eyed3
from threading import Thread
from mutagen.mp3 import MP3  
from mutagen.easyid3 import EasyID3  
import mutagen.id3  
from mutagen.id3 import ID3, TIT2, TIT3, TALB, TPE1, TRCK, TYER
def save_file(chunk,width):
    data = chunk#in case it gets deleted by stuff
    filename = data['title']+' - '+data['author']+'.wav'
    wf = wave.open(filename, 'wb')
    wf.setnchannels(2)
    wf.setsampwidth(width)
    wf.setframerate(44100)
    wf.writeframes(b''.join(data['chunks']))
    wf.close()
    #self.chunks[index] = None
    Thread(target=convert_file,args=(filename,'','mp3')).start()
def convert_file(file_name,album_meta = 'Spotify',format='mp3',delete_after_convert=True, add_meta=True, add_author_meta=False, add_album_meta=True):
    sound= AudioSegment.from_file(file_name)
    out_name = file_name.replace(file_name.split('.')[-1:][0],format)
    if out_name == file_name:
        out_name = file_name.replace('.'+file_name.split('.')[-1:][0],'')
        out_name += 're_write.'+format
    sound.export(out_name,format=format)
    if delete_after_convert==True:
        os.remove(file_name)
    sound = None
    if add_meta==True:
        #tag = id3.Tag()
        #tag.link()
        music = MP3(out_name,ID3=EasyID3)
        file_name = file_name.split('/')[-1:][0]
        music['title'] = file_name.split(' - ')[0].replace('.'+file_name.split('.')[-1:][0], '')
        if add_author_meta == True and len(file_name.split(' - ')) >= 2:
            #tag.author = file_name.split(' - ')[1].replace('.'+file_name.split('.')[-1:][0], '')
            music['author'] = file_name.split(' - ')[1].replace('.'+file_name.split('.')[-1:][0], '')
        if add_album_meta and album_meta != '':
            music['album'] = album_meta
            #tag.album = album_meta
        music.save()
class Record_Spotify():
    def __init__(self):
        self._pair_window()
        self.title,self.author = '',''
    def _pair_window(self):
        self.win = gw.getWindowsWithTitle('Spotify')[0]
        print('Paired Window')
        print(f'Window title: {self.win.title}')
    def _get_data(self):
        try:
            title = self.win.title
            if 'Spotify' not in title:
                self.author = title.split(' - ')[0]
                self.title = title.split(' - ',1)[1]
                return True
            else: return False
        except Exception as e:
            return False, e
    def _wait_till_start(self):
        print('waiting for Spotify to start playing...',end='')
        i = 0
        while self._get_data() == False:
            sleep(.1)
            print(f'\rWaiting for Spotify to start playing'+'.' * (i%4) + ' ' * (((i%4)-4)*-1), end='')
            i += 1
        print('\nSpotify Started')
    def record_play(self):
        self.chunks = []
        
        self._wait_till_start()
        ch = 0
        chunk_data = {'title':self.title,'author':self.author,'chunks':[]}
        p = PyAudio()
        stream = p.open(format=paInt16,
                channels=2,
                rate=44100 ,
                input_device_index=26,
                frames_per_buffer=1024,
                input=True)
        while True:
            d = self._get_data()
            if d == True and self.title == chunk_data['title'] and self.author == chunk_data['author']:
                data = stream.read(1024)
                chunk_data['chunks'].append(data)
                print(f'\rRecording {self.title} sung by {self.author}',end = '')
            elif d == True or (self.title != chunk_data['title']):
                print(f'\rSaving {self.title} - {self.author}   '+''*10)
                #self.chunks.append(chunk_data)
                Thread(target=save_file,name=f'saving {ch}',args=(chunk_data,p.get_sample_size(paInt16))).start()
                chunk_data = {'title':self.title,'author':self.author,'chunks':[]}
                ch += 1
            elif d == False:
                print('\nDone Recording(Caused by music pause or windows closure)')
                break
        


if __name__ == '__main__':
    rec = Record_Spotify()
    rec.record_play()
    #while True:
    #   print('\r'+str(rec._get_data())+'            ', end = '')
    #for dir, dirs, files in os.walk('nate and 12323'):
    #    for x in files:
    #        #if '.mp3' not in x:
    #        print('Converting ',x)
    #        convert_file(dir+"/"+x,'Notable')

