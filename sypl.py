#!/usr/bin/env python3
import os
import sys
import logging
from dateutil.parser import isoparse
from threading import Thread
import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage
from yandex_music import Client, exceptions
import eyed3
import requests
import utils
import setting

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename="error.log", level=logging.ERROR, format=format)

LARGE_FONT = ("Verdana", 12, 'bold')
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


class metadata:
    def set(file, **kwargs):
        audiofile = eyed3.load(file)
        audiofile.initTag()

        audiofile.tag.artist = kwargs['artist']
        audiofile.tag.title = kwargs['title']
        audiofile.tag.album = kwargs['album']
        audiofile.tag.track_num = kwargs['track_num']
        audiofile.tag.year = kwargs['year']
        audiofile.tag.genre = kwargs['genre']

        with open('cover.jpg', 'wb') as f:
            kwargs['images'] = kwargs['images'].replace('%%', '400x400')
            kwargs['images'] = 'http://' + kwargs['images']
            p = requests.get(kwargs['images'])
            f.write(p.content)
            # FIXME add exception
            audiofile.tag.images.set(3,
                                     open('cover.jpg', 'rb').read(),
                                     'image/jpeg')
        audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION,
                           encoding='utf-8')


class GoYandex(setting.setting):
    def __init__(self):
        self.client = Client()
        super().__init__()
        self.selectPL = None
        self.startLoadPl = False
        self.startDownload = False
        self.this = None
        self.listTrack = []
        self.playListsInfo = dict()

    def generateToken(self, login, pas):
        try:
            token = self.client.generate_token_by_username_and_password(
                    username=login,
                    password=pas
                    )
            self.save('token', token)
            return False
        except Exception as e:
            if e.args[0].startswith('invalid_grant'):
                err = e.args[0][14:]
                logging.getLogger(err)
            else:
                err = e.args[0]
                logging.getLogger(err)
            return err

    def authorizationToken(self, token):
        try:
            self.client = Client.from_token(token)
        except Exception as e:
            logging.getLogger(e.args[0])

    def getPlayListsInfo(self):
        # FIXME: убрать после теста долгой загрузки
        # time.sleep(5)
        try:
            PersonalPlaylistBlocks = self.client.landing(
                        blocks=['personalplaylists']
                    ).blocks[0]
        except Exception as e:
            logging.getLogger(e.args[0])
            return False

        for plLst in PersonalPlaylistBlocks.entities:
            if plLst.data.data.play_counter is not None:
                pc = plLst.data.data.play_counter
                pc.description = pc.description.replace('&nbsp;', ' ')
                pc.description = pc.description.replace('&mdash;', '–')
            self.playListsInfo[plLst.data.data.generated_playlist_type] = plLst.data.data
        return True

    def playListGet(self):
        if not self.getPlayListsInfo():
            return

        if self.this.playlistType not in self.playListsInfo:
            # FIXME: выбрать поле для вывода информации
            print('Не удалось найти плейлист')
            logging.getLogger('Не удалось найти плейлист')
            self.startLoadPl = False
            return

        DailyPlaylist = self.playListsInfo[self.this.playlistType]

        self.listTrack.clear()
        self.selectPL = self.client.users_playlists(user_id=DailyPlaylist.uid,
                                                    kind=DailyPlaylist.kind)
        plTitle = self.selectPL[0].title
        plCount = self.selectPL[0].track_count
        self.this.setTitle(plTitle)

        for counter, track in enumerate(self.selectPL[0].tracks, 1):
            self.listTrack.append(track.track)
            self.this.setTitle(f'{plTitle} - {counter}/{plCount}')

            if self.this.playlistType != 'podcasts':
                try:
                    artist = track.track.artists[0].name
                except IndexError:
                    artist = '<BREAK>'
            else:
                artist = track.track.albums[0].title
            self.this.addRow(counter, track.track.title,
                             artist, utils.timeStr(track.track.duration_ms))

            if not self.startLoadPl:
                self.this.setTitle(f'{plTitle} - {counter}/{plCount} - BREAK')
                break
        else:
            duration = utils.timeStr(self.selectPL[0].duration_ms, 0)
            self.this.setTitle(f'{plTitle} - {duration}')
            self.this.setNormalStatus()
            self.startLoadPl = False

    def saveTracks(self):
        ''' Скачивание треков и задание id3-тегов '''
        self.this.showPrigressBar()
        self.this.setValuePrigressBar(0)

        for num, track in enumerate(self.listTrack, 1):
            if self.this.playlistType != 'podcasts':
                artist = track.artists[0].name
            else:
                artist = track.albums[0].title
            path = self.this.getPath()
            fileName = f'[{track.real_id}] {artist} - {track.title}'
            fileName = utils.delSpecCh(fileName)
            fileName = f'{path}{fileName}.mp3'
            print(fileName)
            if os.path.isfile(fileName):
                # Трек уже скачан и находится в папке
                self.this.setValuePrigressBar((num / len(self.listTrack)) * 100)
                continue

            track.download(fileName)
            # FIXME add exception ()
            metadata.set(fileName, artist=artist,
                         title=track.title,
                         album=track.albums[0].title,                    # FIX
                         track_num=track.albums[0].track_position.index,
                         year=track.albums[0].year,
                         genre=track.albums[0].genre,
                         images=track.og_image)

            self.this.setValuePrigressBar((num / len(self.listTrack)) * 100)
            if not self.startDownload:
                # Пользователь прервал скачивание
                break

        self.this.setNormalStatus()
        self.this.hidePrigressBar()
        self.startDownload = False


class Window(tk.Frame):
    '''Общие параметры окон'''
    def __init__(self, master=None, yandex=None):
        super().__init__(master)
        self.master, self.yandex = master, yandex
        self.isClose = True
        self.display_name = yandex.client['me']['account']['display_name']
        self.birthday = yandex.client['me']['account']['birthday']
        self.region = yandex.client['me']['account']['region']
        self.now = yandex.client['me']['account']['now']
        self.registered_at = yandex.client['me']['account']['registered_at']
        self.initUI()

    def initUI(self):
        if self.display_name is None:
            self.master.title('SYPl')
        else:
            self.setTitle(f'Hello, {self.display_name}!')
        self.path = __file__[:-7]
        if sys.platform == 'linux':
            ico = PhotoImage(file=self.path + 'img/favicon.png')
            self.master.call('wm', 'iconphoto', self.master._w, ico)
        elif sys.platform == 'win32':
            self.master.iconbitmap(self.path + 'img/favicon.ico')

    def setTitle(self, newTitle):
        self.master.title(f'SYPl - {newTitle}')


class WindowAuthorization(Window):
    '''
    Окно авторизации и сохрание токена после успешной авторизации
    '''
    def __init__(self, master=None, yandex=None):
        master.geometry("355x500")
        master.resizable(width=False, height=False)
        master.configure(background='white')
        super().__init__(master, yandex)
        self.createWindow()

    def createWindow(self):
        style = ttk.Style()
        style.configure('TFrame', background="#fff")

        addpix = 30

        frImg = ttk.Frame(self.master)
        frImg.pack(pady=50, padx=30, anchor=tk.W)
        frEntryLog = ttk.Frame(self.master, width=200, height=150)
        frEntryLog.pack(padx=30)

        render = PhotoImage(file=self.path + 'img/authorization.png')
        img = tk.Label(frImg, image=render, background='white')
        img.image = render
        img.pack()

        LableLogin = tk.Label(self.master,
                              text="Enter your username, email or phone",
                              foreground='#999', background='white',
                              font=('Arial', 9))
        LableLogin.place(x=30, y=158+addpix)

        self.textLogin = tk.StringVar()
        Entrlogin = tk.Entry(frEntryLog, textvariable=self.textLogin,
                             font=('Arial', 16), width=23)
        Entrlogin.pack(pady=30)

        LablePass = tk.Label(self.master, text="Password",
                             foreground='#999', background='white',
                             font=('Arial', 9))
        LablePass.place(x=30, y=217+addpix)

        self.textPass = tk.StringVar()
        EntrPass = tk.Entry(frEntryLog, textvariable=self.textPass,
                            font=('Arial', 16), width=23, show="*")
        EntrPass.pack()

        self.BLog = tk.Button(frEntryLog, text="Log in", bd=0,
                              command=self.clikLogin,
                              width=32, height=2, bg="#fadd61",
                              font=('Arial', 11), relief="flat")

        # FIXME в GNOME не работает почему-то изменение фона
        self.BLog.bind("<Enter>", lambda event,
                       b=self.BLog: b.configure(bg="#f7c412"))
        self.BLog.bind('<Leave>', lambda event,
                       b=self.BLog: b.configure(bg="#fadd61"))
        self.BLog.pack(pady=10)

    def clikLogin(self):
        '''
        Обработка кнопки 'Log in': генерация и сохранение токена
        '''
        error = self.yandex.generateToken(self.textLogin.get(),
                                          self.textPass.get())
        if error:
            self.showError(error)
        else:
            self.isClose = False
            self.master.destroy()

    def showError(self, err):
        error = tk.Label(self.master,
                         text=err,
                         foreground='#ff0000', background='white',
                         font=('Arial', 12))
        error.place(x=10, y=450)


class WindowMain(Window):
    '''
    Окно с таблицей треков и полем с указанием места сохранения
    '''
    def __init__(self, master=None, yandex=None, setting=None):
        self.SavePathString = tk.StringVar()
        self.setting = setting
        master.minsize(width=750, height=400)
        master.configure(background='white')
        super().__init__(master, yandex)
        self.yandex.this = self
        self.playlistType = None
        self.bPhotos = dict()
        self.lBttns = dict()
        self.thread = None
        self.createWindow()
        self.initInfo()

    def initInfo(self):
        thread = Thread(target=self.yandex.getPlayListsInfo)
        thread.start()

    def createWindow(self):
        style = ttk.Style()
        style.configure('TFrame', background="#ffdb4d")

        frButtons = ttk.Frame(self.master)
        frMesg = ttk.Frame(frButtons)
        frTable = ttk.Frame(self.master)
        frBottom = ttk.Frame(self.master)

        self.createButton(
            frButtons, 'playlistOfTheDay',
            'PlaylistOftheDay100.png', 'PlaylistOftheDayCancel100.png',
            '#7ad537', '#1fba5b', self.loadPlaylistOftheDay)
        self.createButton(
            frButtons, 'recentTracks',
            'Premiere100.png', 'PremiereCancel100.png',
            '#fc990e', '#fc5c12', self.loadRecentTracks)
        self.createButton(
            frButtons, 'neverHeard',
            'DejaVu100.png', 'DejaVuCancel100.png',
            '#ec38fe', '#9438f6', self.loadNeverHeard)
        self.createButton(
            frButtons, 'missedLikes',
            'SecretStash100.png', 'SecretStashCancel100.png',
            '#329cf7', '#0064d2', self.loadMissedLikes)
        self.createButton(
            frButtons, 'podcasts',
            'PodcastsWeekly100.png', 'PodcastsWeeklyCancel100.png',
            '#dcedff', '#b6daff', self.loadPodcasts)

        self.labTitle = tk.Label(frMesg, padx="15", fg="#000", bg="#ffdb4d",
                                 wraplength=215, font=LARGE_FONT)
        self.lablInf1 = tk.Label(frMesg, padx="3", fg="#000", bg="#ffdb4d",
                                 wraplength=215, font=MEDIUM_FONT,
                                 justify=tk.LEFT, anchor=tk.W)
        self.lablInf2 = tk.Label(frMesg, padx="3", fg="#000", bg="#ffdb4d",
                                 wraplength=215, font=MEDIUM_FONT,
                                 justify=tk.LEFT, anchor=tk.W)

        self.bar = ttk.Progressbar(frMesg, length=100)

        self.labTitle.pack(fill=tk.BOTH, side=tk.TOP, expand=0, ipady=4)
        self.lablInf1.pack(fill=tk.BOTH, expand=1, ipady=0)
        self.lablInf2.pack(fill=tk.BOTH, expand=1, ipady=0)

        self.table = ttk.Treeview(frTable)
        self.table["columns"] = ("Title", "Artist", "Duration")
        self.table.column("#0", width=50, minwidth=50, stretch=tk.NO)
        self.table.column("Title", width=250, minwidth=250)
        self.table.column("Artist", width=250, minwidth=250)
        self.table.column("Duration", width=70, minwidth=70, stretch=tk.NO)

        self.table.heading("#0", text="#", anchor=tk.W)
        self.table.heading("Title", text="Title", anchor=tk.W)
        self.table.heading("Artist", text="Artist", anchor=tk.W)
        self.table.heading("Duration", text="Duration", anchor=tk.W)

        sb = tk.Scrollbar(frTable, orient="vertical", relief="flat")
        sb.config(command=self.table.yview)
        self.table.config(yscrollcommand=sb.set)
        sb.pack(side=tk.RIGHT, fill='y')

        self.pathSaveFolder = tk.Entry(frBottom, relief="flat", cursor="arrow",
                                       textvariable=self.SavePathString)

        self.pathSaveFolder.configure(state='readonly')
        self.pathSaveFolder.bind('<Button-1>', self.chooseFolder)

        folder = self.setting.getParam('folder')
        if folder is None:
            folder = os.getcwd()
        self.SavePathString.set(folder)

        self.bSave = tk.Button(frBottom, text="Save", bg='#fadd61',
                               command=self.dowloadTracks, width=10,
                               relief="flat", pady="5")
        self.bSave.bind(
            '<Enter>', lambda event, b=self.bSave: b.configure(bg="#f7c412"))  # #f7c412
        self.bSave.bind(
            '<Leave>', lambda event, b=self.bSave: b.configure(bg="#fadd61"))
        self.bSave.configure(state='disabled')

        self.LablStatus = tk.Label(frBottom, pady="0", fg="#777", bg="#fff",
                                   font=SMALL_FONT, justify=tk.LEFT,
                                   anchor=tk.W)

        frButtons.pack(side=tk.TOP, fill=tk.BOTH, expand=0, pady=0)
        frTable.pack(fill=tk.BOTH, expand=1)
        frBottom.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=10)
        self.LablStatus.pack(fill=tk.X, side=tk.BOTTOM, ipady=3)

        for butt in self.lBttns:
            self.lBttns[butt].pack(side=tk.LEFT, expand=0)
        frMesg.pack(side=tk.TOP, fill=tk.X, expand=0)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.pathSaveFolder.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
        self.bSave.pack(side=tk.RIGHT, expand=0)

    def addRow(self, num, title, artist, dura):

        self.table.insert("", num, iid=None, text=num,
                          values=(title, artist, dura))

    def getPath(self):
        return self.SavePathString.get()

    def showPrigressBar(self):
        self.bar.pack(fill=tk.BOTH, side=tk.BOTTOM)

    def hidePrigressBar(self):
        self.bar.pack_forget()

    def setValuePrigressBar(self, value):
        self.bar['value'] = value

    def setNormalStatus(self):
        self.bSave['text'] = 'Save'
        self.bSave.configure(state='normal')
        self.pathSaveFolder.configure(state='readonly')

    def chooseFolder(self, event):
        if self.pathSaveFolder['state'] == 'readonly':
            title = 'Select directory to download tracks'
            folder = filedialog.askdirectory(
                       title=title,
                       initialdir=self.SavePathString.get())
            if folder:
                self.SavePathString.set(folder+'/')
                self.setting.save('folder', folder+'/')

    def getTracks(self):
        if self.yandex.startDownload:
            return

        if self.yandex.startLoadPl:
            self.yandex.startLoadPl = False
        else:
            self.yandex.startLoadPl = True
            thread = Thread(target=self.yandex.playListGet)
            thread.start()

    def dowloadTracks(self):
        if self.yandex.startDownload:
            self.yandex.startDownload = False
            self.bSave.configure(state='disabled')
        else:
            self.yandex.startDownload = True
            thread = Thread(target=self.yandex.saveTracks)
            thread.start()
            self.bSave['text'] = 'Stop'

    def setRunStatus(self, playList):
        if self.yandex.startDownload:
            return

        if not self.yandex.startLoadPl:
            if self.playlistType is not None:
                self.lBttns[self.playlistType]['image'] = self.bPhotos[self.playlistType]
            self.lBttns[playList]['image'] = self.bPhotos[playList+'Cancel']
            self.playlistType = playList
            self.pathSaveFolder.configure(state='disabled')
            self.table.delete(*self.table.get_children())
        else:
            self.pathSaveFolder.configure(state='readonly')

    def loadPlaylistOftheDay(self):
        self.setRunStatus('playlistOfTheDay')
        self.getTracks()

    def loadRecentTracks(self):
        self.setRunStatus('recentTracks')
        self.getTracks()

    def loadNeverHeard(self):
        self.setRunStatus('neverHeard')
        self.getTracks()

    def loadMissedLikes(self):
        self.setRunStatus('missedLikes')
        self.getTracks()

    def loadPodcasts(self):
        self.setRunStatus('podcasts')
        self.getTracks()

    def createButton(self, frame, nameButtom,
                     bPhoto, bPhotoCancel,
                     Enter, Leave,
                     command):
        bPhoto = f'img/{bPhoto}'
        bPhotoCancel = f'img/{bPhotoCancel}'
        self.bPhotos[nameButtom] = PhotoImage(file=self.path+bPhoto)
        self.bPhotos[nameButtom+'Cancel'] = PhotoImage(
            file=self.path+bPhotoCancel)
        self.lBttns[nameButtom] = tk.Button(
            frame, width=100, height=100,
            bg=Leave, relief="flat", command=command)
        self.lBttns[nameButtom]['image'] = self.bPhotos[nameButtom]
        self.lBttns[nameButtom].bind(
            '<Enter>', lambda event, b=[nameButtom, Enter]:
            self.fnbuttonBEnter(event, b))
        self.lBttns[nameButtom].bind(
            '<Leave>', lambda event, b=[nameButtom, Leave]:
            self.fnbuttonBLeave(event, b))

    def fnbuttonBLeave(self, event, data):
        if self.playlistType == data[0]:
            return
        self.lBttns[data[0]].configure(bg=data[1])
        self.lBttns[data[0]]['image'] = self.bPhotos[data[0]]
        self.LablStatus['text'] = ''

    def fnbuttonBEnter(self, event, data):
        self.lBttns[data[0]].configure(bg=data[1])

        if data[0] in self.yandex.playListsInfo:
            if self.yandex.playListsInfo[data[0]].play_counter is None:
                text = self.yandex.playListsInfo[data[0]].description_formatted
            else:
                text = self.yandex.playListsInfo[data[0]].play_counter.description

            self.LablStatus['text'] = text
            self.labTitle['text'] = self.yandex.playListsInfo[data[0]].title
            track_count = self.yandex.playListsInfo[data[0]].track_count
            durStr = self.yandex.playListsInfo[data[0]].duration_ms
            durStr = utils.timeStr(durStr, 0)
            updated = isoparse(self.yandex.playListsInfo[data[0]].modified)
            updated = updated.strftime('%d.%m.%Y %a')
            self.lablInf1['text'] = f'{track_count} tracks, duration {durStr}'
            self.lablInf2['text'] = f'Updated on {updated}'


class WM:
    def __init__(self):
        self.setting = setting.setting()
        logger = logging.getLogger('yandex_music')
        logger.setLevel(logging.ERROR)
        self.root = None
        self.windowClose = False
        try:
            self.yandex = GoYandex()
        except exceptions.NetworkError as e:
            logging.error(e)
            print(e)
            self.windowClose = True

        if sys.platform == 'linux':
            self.checkDisplay()

        self.run()

    def run(self):
        # Если нет токена, то генерируем его из логина и пароля
        if self.setting.getParam('token') is None:
            self.showWindowAuthorization()

        if self.windowClose:
            sys.exit()

        self.yandex.authorizationToken(self.setting.getParam('token'))
        self.showWindowMain()

    def showWindowAuthorization(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.processingExit)
        self.showWindow = WindowAuthorization(master=self.root,
                                              yandex=GoYandex())
        self.showWindow.mainloop()

    def showWindowMain(self):
        self.root = tk.Tk()
        self.root.protocol('WM_DELETE_WINDOW', self.processingExit)
        self.showWindow = WindowMain(master=self.root,
                                     yandex=self.yandex,
                                     setting=self.setting)
        self.showWindow.mainloop()

    def processingExit(self):
        self.windowClose = self.showWindow.isClose
        self.root.destroy()

    def checkDisplay(self):
        if not os.environ.get('DISPLAY', False):
            logging.error('Display not found')
            print('Display not found')
            self.windowClose = True


if __name__ == '__main__':
    WM()
