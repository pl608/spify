from pydub import AudioSegment
from pyaudio import PyAudio, paInt16
from time import sleep, time
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
from sys import argv
if argv[-1] != 'main.py':
    album = argv[-1]
    print('Set Album To: ',album)
path = album+'/'
try: os.mkdir(path)
except FileExistsError: pass
except: print(Exception)
class Record_Spotify():
    def save_file(self,chunk,width):
        global path
        data = chunk#in case it gets deleted by stuff
        filename = data['title']+' - '+data['author']+'.wav'
        filename = filename.replace(':','')
        filename = filename.replace('/','')
        filename = filename.replace('?','')
        filename = filename.replace('!','')
        filename = filename.replace('"','')
        filename = path+filename
        print(filename)
        wf = wave.open(filename, 'wb')
        wf.setnchannels(2)
        wf.setsampwidth(width)
        wf.setframerate(44100)
        wf.writeframes(b''.join(data['chunks']))
        wf.close()
        #self.chunks[index] = None
        if self.convert_files == True:
            Thread(target=self.convert_file,args=(filename,)).start()
    def convert_file(self,file_name,delete_after_convert=True, add_meta=True, add_author_meta=False, add_album_meta=True):
        open(file_name,'rb')
        sound= AudioSegment.from_file(file_name)
        #input('sound')
        out_name = file_name.replace(file_name.split('.')[-1:][0],self.format)
        if out_name == file_name:
            out_name = file_name.replace('.'+file_name.split('.')[-1:][0],'')
            out_name += 're_write.'+self.format
        sound.export(out_name,format=self.format)# its having trouble finding ffmpeg/probe
        if delete_after_convert==True:
            os.remove(file_name)
        sound = None
        if add_meta==True:
            music = MP3(out_name,ID3=EasyID3)
            file_name = file_name.split('/')[-1:][0]
            
            music['title'] = file_name.split(' - ')[0].replace('.'+file_name.split('.')[-1:][0], '')
            music['artist'] = file_name.split(' - ')[1].replace('.'+file_name.split('.')[-1:][0], '')
            music['album'] = self.album
            
            music.save()
    def get_index(self,search='CABLE Output (VB-Audio Virtual '):
        #return int(input('index: '))
        #return 9
        p = PyAudio()
        for i in range(p.get_device_count()):
            name = p.get_device_info_by_index(i)["name"]
            if name == search:
                self.status(f'\nSetting Device Index To: {i} ({name})\n')
                return i
        return 0
    def __str__(self):
        return self._status
    def __init__(self, auto_start=True, search='CABLE Output (VB-Audio Virtual ', print_status=True, Album=album, record_on_thread=True):
        self._pairwindow()
        self.title,self.author = '',''
        self.print_status = print_status
        self.recording = False
        self.index = self.get_index(search=search)
        self.album = Album
        self.format = 'mp3'
        self.raw = ''
        self.convert_files = True
        self._status = 'Starting...'
        if auto_start==True and record_on_thread==True:
            self.thread = Thread(target=self.record_save,name='Recording Thread')
            self.thread.start()
        elif auto_start==True and record_on_thread == False:
            self.record_save()
    def _pairwindow(self):
        self.status('Finding Spotify window...',end='')
        i = 0
        while len(gw.getWindowsWithTitle('Spotify')) != 1:
            self.status('\rFinding Spotify window'+'.' * (i%4) + ' ' * (((i%4)-4)*-1), end='')
            #self.status("\r"+str(len(gw.getWindowsWithTitle('Spotify'))), end='')
            sleep(.1)
            i += 1
        self.win = gw.getWindowsWithTitle('Spotify')[0]
        self.status(f' - Paired Window')
        self.status(f'\nWindow title: {self.win.title}\n\n')
    def _getdata(self):
        try:
            title = self.win.title
            if 'Spotify' not in title:
                self.author = title.split(' - ')[0]
                self.title = ''.join(title.split(' - ',1)[1])
                #self.raw = str(title)
                return True
            else: return False
        except Exception as e:
            print(e)
            return False, e
    def _wait_till_start(self):
        self.status('waiting for Spotify to start playing...',end='')
        i = 0
        while self._getdata() == False:
            sleep(.1)
            self.status(f'\rWaiting for Spotify to start playing'+'.' * (i%4) + ' ' * (((i%4)-4)*-1), end='')
            i += 1
        self.status('\nSpotify Started')
    def status(self,msg: str,end=''):
        self._status = msg+end
        try:
            print(msg+end,end='')
        except Exception as e:
            print(e)
    def record_save(self):
        self.chunks = []
        self._wait_till_start()
        ch = 0
        chunk_data = {'title':self.title,'author':self.author,'chunks':[]}
        p = PyAudio()
        stream = p.open(format=paInt16,
                channels=2,
                rate=44100 ,
                input_device_index=self.index,
                frames_per_buffer=2048,
                input=True)
        stream.start_stream()
        ii = time()
        while True:
            d = self._getdata()
            if d == True and self.title == chunk_data['title'] and self.author == chunk_data['author']:
                data = stream.read(2048)
                chunk_data['chunks'].append(data)
                i = int((time()-ii)*4)
                self.recording = True
                print(f'\rRecording {self.title} sung by {self.author}'+'.' * (i%4) + ' ' * (((i%4)-4)*-1),end = '')
            elif d == True or (self.title != chunk_data['title']):
                print(f"\rSaving {chunk_data['title']} - {chunk_data['author']}   "+''*15+'\n')
                #self.chunks.append(chunk_data)
                Thread(target=self.save_file,name=f'saving {ch}',args=(chunk_data,p.get_sample_size(paInt16))).start()
                chunk_data = {'title':self.title,'author':self.author,'chunks':[]}
                ch += 1
            if d == False:
                self.recording = False
                print('\nDone Recording(Caused by music pause or windows closure)')
                print(f"\nSaving {chunk_data['title']} - {chunk_data['author']}   "+''*15)
                Thread(target=self.save_file,name=f'saving {ch}',args=(chunk_data,p.get_sample_size(paInt16))).start()
                chunk_data = {'title':self.title,'author':self.author,'chunks':[]}
                break
            #else:
            #    print(f"self.title: {self.title}\nchunk title: {chunk_data['title']}\nself.author: {self.author}\nchunk author: {chunk_data['author']}")
    


if __name__ == '__main__':
    rec = Record_Spotify(print_status=False)
    #last_status = ''
    #while True:
    #   if last_status != str(rec):
    #        print(f'\r{str(rec)}',end=' '*10)
    #        last_status = str(rec)
    #rec.record_play()
    #while True:
    #   self.status('\r'+str(rec._get_data())+'            ', end = '')
    #for dir, dirs, files in os.walk('nate and 12323'):
    #    for x in files:
    #        #if '.mp3' not in x:
    #        self.status('Converting ',x)
    #        convert_file(dir+"/"+x,'Notable')

