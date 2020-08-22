#!/usr/bin/env python3
from dateutil.parser import isoparse
import logging
import os
import requests
import sys
import tempfile
from threading import Thread
import time
import tkinter as tk
from tkinter import ttk, filedialog, PhotoImage

import eyed3
from yandex_music import Client, exceptions

import setting
import utils

format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(filename="error.log", level=logging.ERROR, format=format)

LARGE_FONT = ("Verdana", 12, 'bold')
MEDIUM_FONT = ("Verdana", 10)
SMALL_FONT = ("Verdana", 8)


class MetadataMP3:
    def __init__(self, file):
        self.audiofile = eyed3.load(file)
        self.audiofile.initTag()

    def set_tags(self, **kwargs):
        for tag in kwargs:
            setattr(self.audiofile.tag, tag, kwargs[tag])

    def set_image(self, image):
        url_image = f"http://{image.replace('%%', '400x400')}"
        res = requests.get(url_image)
        with tempfile.TemporaryFile(delete=False) as fp:
            fName = fp.name
            fp.write(res.content)
            fp.close()
            # FIXME add exception
            self.audiofile.tag.images.set(3, open(fName, 'rb').read(), 'image/jpeg')
            os.remove(fName)

    def save(self):
        self.audiofile.tag.save(version=eyed3.id3.ID3_DEFAULT_VERSION, encoding='utf-8')


class GoYandex():
    def __init__(self, setting):
        self.client = Client()
        super().__init__()
        self.select_PL = None
        self.start_load_Pl = False
        self.start_download = False
        self.this = None
        self.list_track = []
        self.setting = setting
        self.play_lists_info = dict()

    def generate_token(self, login, pas):
        try:
            token = self.client.generate_token_by_username_and_password(username=login, password=pas)
            self.setting.save('token', token)
            return False
        except Exception as e:
            if e.args[0].startswith('invalid_grant'):
                err = e.args[0][14:]
                logging.getLogger(err)
            else:
                err = e.args[0]
                logging.getLogger(err)
            return err

    def authorization_token(self, token):
        try:
            self.client = Client.from_token(token)
        except Exception as e:
            logging.getLogger(e.args[0])

    def get_play_lists_info(self):
        # FIXME: убрать после теста долгой загрузки
        # time.sleep(5)
        # run in Thread
        try:
            personal_playlist_blocks = self.client.landing(blocks=['personalplaylists']).blocks[0]
        except Exception as e:
            logging.getLogger(e.args[0])
            return False

        for plLst in personal_playlist_blocks.entities:
            if plLst.data.data.play_counter is not None:
                pc = plLst.data.data.play_counter
                pc.description = pc.description.replace('&nbsp;', ' ')
                pc.description = pc.description.replace('&mdash;', '–')
            self.play_lists_info[plLst.data.data.generated_playlist_type] = plLst.data.data
        return True

    def get_play_list(self):
        # run in Thread
        if not self.get_play_lists_info():
            return

        if self.this.play_list_type not in self.play_lists_info:
            # FIXME: выбрать поле для вывода информации
            print('Не удалось найти плейлист')
            logging.getLogger('Не удалось найти плейлист')
            self.start_load_Pl = False
            return

        daily_play_list = self.play_lists_info[self.this.play_list_type]

        self.list_track.clear()
        self.select_PL = self.client.users_playlists(user_id=daily_play_list.uid, kind=daily_play_list.kind)
        plTitle = self.select_PL[0].title
        plCount = self.select_PL[0].track_count
        self.this.set_title(plTitle)

        for counter, track in enumerate(self.select_PL[0].tracks, 1):
            self.list_track.append(track.track)
            self.this.set_title(f'{plTitle} - {counter}/{plCount}')

            if self.this.play_list_type != 'podcasts':
                try:
                    artist = track.track.artists[0].name
                except IndexError:
                    artist = '<BREAK>'
            else:
                artist = track.track.albums[0].title
            self.this.add_row(counter, track.track.title, artist, utils.timeStr(track.track.duration_ms))

            if not self.start_load_Pl:
                self.this.set_title(f'{plTitle} - {counter}/{plCount} - BREAK')
                break
        else:
            duration = utils.timeStr(self.select_PL[0].duration_ms, 0)
            self.this.set_title(f'{plTitle} - {duration}')
            self.this.set_normal_status()
            self.start_load_Pl = False

    def save_tracks(self):
        ''' Скачивание треков и задание id3-тегов '''
        # run in Thread
        self.this.show_prigress_bar()
        self.this.set_prigress_bar(0)

        for num, track in enumerate(self.list_track, 1):
            if self.this.play_list_type != 'podcasts':
                if len(track.artists):
                    artist = track.artists[0].name
                else:
                    artist = ''
            else:
                artist = track.albums[0].title
            path = self.this.get_path()
            file_name = f'[{track.real_id}] {artist} - {track.title}'
            file_name = utils.delSpecCh(file_name)
            file_name = f'{path}{file_name}.mp3'
            print(file_name)
            if os.path.isfile(file_name):
                # Трек уже скачан и находится в папке
                self.this.set_prigress_bar((num / len(self.list_track)) * 100)
                continue

            track.download(file_name)
            # FIXME add exception ()
            mp3file = MetadataMP3(file_name)
            mp3file.set_tags(artist=artist,
                             title=track.title,
                             album=track.albums[0].title,                    # FIX
                             track_num=track.albums[0].track_position.index,
                             year=track.albums[0].year,
                             genre=track.albums[0].genre)
            mp3file.set_image(track.og_image)
            mp3file.save()

            self.this.set_prigress_bar((num / len(self.list_track)) * 100)
            if not self.start_download:
                # Пользователь прервал скачивание
                break

        self.this.set_normal_status()
        self.this.hide_prigress_bar()
        self.start_download = False


class Window(tk.Frame):
    '''Общие параметры окон'''
    def __init__(self, master=None, yandex=None):
        super().__init__(master)
        self.master, self.yandex = master, yandex
        self.isClose = True
        self.account = yandex.client['me']['account']
        self.initUI()

    def initUI(self):
        if self.account['display_name'] is None:
            self.master.title('SYPl')
        else:
            self.set_title(f"Hello, {self.account['display_name']}!")
        self.path = __file__[:-7]
        ico = PhotoImage(file=self.path + 'img/favicon32.png')
        self.master.call('wm', 'iconphoto', self.master._w, ico)

    def set_title(self, newTitle):
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
        self.create_window()

    def create_window(self):
        style = ttk.Style()
        style.configure('TFrame', background="#fff")

        addpix = 30

        frImg = ttk.Frame(self.master)
        frImg.pack(pady=50, padx=30, anchor=tk.W)
        frEntry_log = ttk.Frame(self.master, width=200, height=150)
        frEntry_log.pack(padx=30)

        render = PhotoImage(file=self.path + 'img/authorization.png')
        img = tk.Label(frImg, image=render, background='white')
        img.image = render
        img.pack()

        labellogin = tk.Label(self.master, text="Enter your username, email or phone",
                              foreground='#999', background='white', font=('Arial', 9))
        labellogin.place(x=30, y=158 + addpix)

        self.text_login_var = tk.StringVar()
        entrylogin = tk.Entry(frEntry_log, textvariable=self.text_login_var, font=('Arial', 16), width=23)
        entrylogin.pack(pady=30)

        labelpass = tk.Label(self.master, text="Password", foreground='#999', background='white', font=('Arial', 9))
        labelpass.place(x=30, y=217 + addpix)

        self.text_pass_var = tk.StringVar()
        entrypass = tk.Entry(frEntry_log, textvariable=self.text_pass_var, font=('Arial', 16), width=23, show="*")
        entrypass.pack()

        self.button_login = tk.Button(frEntry_log, text="Log in", bd=0, command=self.clik_login, width=32, height=2,
                                      bg="#fadd61", font=('Arial', 11), relief="flat")

        # FIXME в GNOME не работает почему-то изменение фона
        self.button_login.bind("<Enter>", lambda event, b=self.button_login: b.configure(bg="#f7c412"))
        self.button_login.bind('<Leave>', lambda event, b=self.button_login: b.configure(bg="#fadd61"))
        self.button_login.pack(pady=10)

    def clik_login(self):
        '''
        Обработка кнопки 'Log in': генерация и сохранение токена
        '''
        error = self.yandex.generate_token(self.text_login_var.get(), self.text_pass_var.get())
        if error:
            self.show_error(error)
        else:
            self.isClose = False
            self.master.destroy()

    def show_error(self, err):
        error = tk.Label(self.master, text=err, foreground='#ff0000', background='white', font=('Arial', 12))
        error.place(x=10, y=450)


class WindowMain(Window):
    '''
    Окно с таблицей треков и полем с указанием места сохранения
    '''
    def __init__(self, master=None, yandex=None):
        self.save_path_var = tk.StringVar()
        master.minsize(width=750, height=400)
        master.configure(background='white')
        super().__init__(master, yandex)
        self.yandex.this = self
        self.play_list_type = None
        self.bPhotos = dict()
        self.lBttns = dict()
        self.thread = None
        self.create_window()
        self.init_info()

    def init_info(self):
        # loading yandex playlist
        threadYd = Thread(target=self.yandex.get_play_lists_info)
        threadYd.start()

        # drawing count of listening playlistOfTheDay in row
        threadCount = Thread(target=self.change_button_img)
        threadCount.start()

    def create_window(self):
        style = ttk.Style()
        style.configure('TFrame', background="#ffdb4d")

        frButtons = ttk.Frame(self.master)
        frMesg = ttk.Frame(frButtons)
        frTable = ttk.Frame(self.master)
        frBottom = ttk.Frame(self.master)

        self.create_button(frButtons, 'playlistOfTheDay', 'PlaylistOftheDay100.png', 'PlaylistOftheDayCancel100.png',
                           '#7ad537', '#1fba5b', self.load_playlistOftheDay)
        self.create_button(frButtons, 'recentTracks', 'Premiere100.png', 'PremiereCancel100.png',
                           '#fc990e', '#fc5c12', self.load_recentTracks)
        self.create_button(frButtons, 'neverHeard', 'DejaVu100.png', 'DejaVuCancel100.png',
                           '#ec38fe', '#9438f6', self.load_neverHeard)
        self.create_button(frButtons, 'missedLikes', 'SecretStash100.png', 'SecretStashCancel100.png',
                           '#329cf7', '#0064d2', self.load_missedLikes)
        self.create_button(frButtons, 'podcasts', 'PodcastsWeekly100.png', 'PodcastsWeeklyCancel100.png',
                           '#dcedff', '#b6daff', self.load_podcasts)

        self.label_title = tk.Label(frMesg, padx="15", fg="#000", bg="#ffdb4d", wraplength=215, font=LARGE_FONT)
        self.label_inf1 = tk.Label(frMesg, padx="3", fg="#000", bg="#ffdb4d", wraplength=215, font=MEDIUM_FONT,
                                   justify=tk.LEFT, anchor=tk.W)
        self.label_inf2 = tk.Label(frMesg, padx="3", fg="#000", bg="#ffdb4d", wraplength=215, font=MEDIUM_FONT,
                                   justify=tk.LEFT, anchor=tk.W)

        self.bar = ttk.Progressbar(frMesg, length=100)

        self.label_title.pack(fill=tk.BOTH, side=tk.TOP, expand=0, ipady=4)
        self.label_inf1.pack(fill=tk.BOTH, expand=1, ipady=0)
        self.label_inf2.pack(fill=tk.BOTH, expand=1, ipady=0)

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

        scrollbar = tk.Scrollbar(frTable, orient="vertical", relief="flat")
        scrollbar.config(command=self.table.yview)
        self.table.config(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill='y')

        self.path_save_folder = tk.Entry(frBottom, relief="flat", cursor="arrow", textvariable=self.save_path_var)

        self.path_save_folder.configure(state='readonly')
        self.path_save_folder.bind('<Button-1>', self.choose_folder)

        folder = self.yandex.setting.get_param('folder')
        if folder is None:
            folder = os.getcwd()
        self.save_path_var.set(folder)

        self.bSave = tk.Button(frBottom, text="Save", bg='#fadd61', command=self.dowload_tracks, width=10,
                               relief="flat", pady="5")
        self.bSave.bind('<Enter>', lambda event, b=self.bSave: b.configure(bg="#f7c412"))  # #f7c412
        self.bSave.bind('<Leave>', lambda event, b=self.bSave: b.configure(bg="#fadd61"))
        self.bSave.configure(state='disabled')

        self.label_status = tk.Label(frBottom, pady="0", fg="#777", bg="#fff",
                                     font=SMALL_FONT, justify=tk.LEFT, anchor=tk.W)

        frButtons.pack(side=tk.TOP, fill=tk.BOTH, expand=0, pady=0)
        frTable.pack(fill=tk.BOTH, expand=1)
        frBottom.pack(side=tk.BOTTOM, fill=tk.BOTH, padx=5, pady=10)
        self.label_status.pack(fill=tk.X, side=tk.BOTTOM, ipady=3)

        for butt in self.lBttns:
            self.lBttns[butt].pack(side=tk.LEFT, expand=0)
        frMesg.pack(side=tk.TOP, fill=tk.X, expand=0)

        self.table.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        self.path_save_folder.pack(fill=tk.BOTH, side=tk.LEFT, expand=1)
        self.bSave.pack(side=tk.RIGHT, expand=0)

    def add_row(self, num, title, artist, dura):

        self.table.insert("", num, iid=None, text=num, values=(title, artist, dura))

    def get_path(self):
        return self.save_path_var.get()

    def show_prigress_bar(self):
        self.bar.pack(fill=tk.BOTH, side=tk.BOTTOM)

    def hide_prigress_bar(self):
        self.bar.pack_forget()

    def set_prigress_bar(self, value):
        self.bar['value'] = value

    def set_normal_status(self):
        self.bSave['text'] = 'Save'
        self.bSave.configure(state='normal')
        self.path_save_folder.configure(state='readonly')

    def choose_folder(self, event):
        if self.path_save_folder['state'] == 'readonly':
            title = 'Select directory to download tracks'
            folder = filedialog.askdirectory(title=title, initialdir=self.save_path_var.get())
            if folder:
                folder = f'{folder}/'
                self.save_path_var.set(folder)
                self.yandex.setting.save('folder', folder)

    def get_tracks(self):
        if self.yandex.start_download:
            return

        if self.yandex.start_load_Pl:
            self.yandex.start_load_Pl = False
        else:
            self.yandex.start_load_Pl = True
            thread = Thread(target=self.yandex.get_play_list)
            thread.start()

    def dowload_tracks(self):
        if self.yandex.start_download:
            self.yandex.start_download = False
            self.bSave.configure(state='disabled')
        else:
            self.yandex.start_download = True
            thread = Thread(target=self.yandex.save_tracks)
            thread.start()
            self.bSave['text'] = 'Stop'

    def set_run_status(self, playList):
        if self.yandex.start_download:
            return

        if not self.yandex.start_load_Pl:
            if self.play_list_type is not None:
                self.lBttns[self.play_list_type]['image'] = self.bPhotos[self.play_list_type]
            self.lBttns[playList]['image'] = self.bPhotos[f'{playList}Cancel']
            self.play_list_type = playList
            self.path_save_folder.configure(state='disabled')
            self.table.delete(*self.table.get_children())
        else:
            self.path_save_folder.configure(state='readonly')

    def load_playlistOftheDay(self):
        self.set_run_status('playlistOfTheDay')
        self.get_tracks()

    def load_recentTracks(self):
        self.set_run_status('recentTracks')
        self.get_tracks()

    def load_neverHeard(self):
        self.set_run_status('neverHeard')
        self.get_tracks()

    def load_missedLikes(self):
        self.set_run_status('missedLikes')
        self.get_tracks()

    def load_podcasts(self):
        self.set_run_status('podcasts')
        self.get_tracks()

    def create_button(self, frame, nameButtom, bPhoto, bPhotoCancel, Enter, Leave, command):
        bPhoto = f'img/{bPhoto}'
        bPhotoCancel = f'img/{bPhotoCancel}'
        self.bPhotos[nameButtom] = PhotoImage(file=f'{self.path}{bPhoto}')
        self.bPhotos[f'{nameButtom}Cancel'] = PhotoImage(file=f'{self.path}{bPhotoCancel}')
        self.lBttns[nameButtom] = tk.Button(frame, width=100, height=100, bg=Leave, relief="flat", command=command)
        self.lBttns[nameButtom]['image'] = self.bPhotos[nameButtom]
        self.lBttns[nameButtom].bind('<Enter>', lambda event, b=[nameButtom, Enter]: self.fn_btn_Enter(event, b))
        self.lBttns[nameButtom].bind('<Leave>', lambda event, b=[nameButtom, Leave]: self.fn_btn_leave(event, b))

    def change_button_img(self):
        # run in Thread
        brk = 0
        count = 0
        while 'playlistOfTheDay' not in self.yandex.play_lists_info:
            # wite loging to yandex
            time.sleep(.1)
            if brk > 100:
                break
            brk += 1
        else:
            count = self.yandex.play_lists_info['playlistOfTheDay'].play_counter.value

        if not count:
            return

        imgPPM = utils.Image(file=self.path + 'img/PlaylistOftheDay100Num.ppm')
        imgPPM.addCount(count, 10, 83, [(77, 200, 73), (82, 201, 79)])
        self.bPhotos['playlistOfTheDay'] = imgPPM.PhotoImage()
        self.lBttns['playlistOfTheDay']['image'] = self.bPhotos['playlistOfTheDay']

        imgPPM.darker(44, 57, 33)
        self.bPhotos['playlistOfTheDayCancel'] = imgPPM.PhotoImage()

    def fn_btn_leave(self, event, data):
        if self.play_list_type == data[0]:
            return
        self.lBttns[data[0]].configure(bg=data[1])
        self.lBttns[data[0]]['image'] = self.bPhotos[data[0]]
        self.label_status['text'] = ''

    def fn_btn_Enter(self, event, data):
        self.lBttns[data[0]].configure(bg=data[1])

        if data[0] in self.yandex.play_lists_info:
            if self.yandex.play_lists_info[data[0]].play_counter is None:
                text = self.yandex.play_lists_info[data[0]].description_formatted
            else:
                text = self.yandex.play_lists_info[data[0]].play_counter.description

            self.label_status['text'] = text
            self.label_title['text'] = self.yandex.play_lists_info[data[0]].title
            track_count = self.yandex.play_lists_info[data[0]].track_count
            durStr = self.yandex.play_lists_info[data[0]].duration_ms
            durStr = utils.timeStr(durStr, 0)
            updated = isoparse(self.yandex.play_lists_info[data[0]].modified)
            updated = updated.strftime('%d.%m.%Y %a')
            self.label_inf1['text'] = f'{track_count} tracks, duration {durStr}'
            self.label_inf2['text'] = f'Updated on {updated}'


class WM:
    def __init__(self):
        self.setting = setting.Setting()
        logger = logging.getLogger('yandex_music')
        logger.setLevel(logging.ERROR)
        self.root = None
        self.windowClose = False
        try:
            self.yandex = GoYandex(setting=self.setting)
        except exceptions.NetworkError as e:
            logging.error(e)
            print(e)
            self.windowClose = True

        if sys.platform == 'linux':
            self.checkDisplay()

        self.run()

    def run(self):
        # Если нет токена, то генерируем его из логина и пароля
        if self.setting.get_param('token') is None:
            self.show_window_authorization()

        if self.windowClose:
            sys.exit()

        self.yandex.authorization_token(self.setting.get_param('token'))
        self.root = tk.Tk()
        self.show_window_main()

    def show_window_authorization(self):
        self.root.protocol('WM_DELETE_WINDOW', self.processingExit)
        self.show_window = WindowAuthorization(master=self.root, yandex=self.yandex)
        self.show_window.mainloop()

    def show_window_main(self):
        self.root.protocol('WM_DELETE_WINDOW', self.processingExit)
        self.show_window = WindowMain(master=self.root, yandex=self.yandex)
        self.show_window.mainloop()

    def processingExit(self):
        self.windowClose = self.show_window.isClose
        self.root.destroy()

    def checkDisplay(self):
        if not os.environ.get('DISPLAY', False):
            logging.error('Display not found')
            print('Display not found')
            self.windowClose = True


if __name__ == '__main__':
    WM()
