import os
import sys
import pickle


class setting:
    def __init__(self):
        if sys.platform == 'linux':
            self.pklFile = os.path.expanduser('~/.local/share/SYPl/設定.pkl')
        elif sys.platform == 'win32':
            self.pklFile = os.path.expanduser('~\\AppData\\Roaming\\SYPl\\設定.pkl')
        self.set = dict()
        self.chekFile()

    def chekFile(self):
        if not os.path.exists(self.pklFile[:-6]):
            os.mkdir(self.pklFile[:-6])
        if not os.path.isfile(self.pklFile):
            with open(self.pklFile, 'wb') as f:
                pickle.dump(self.set, f)

    def save(self, param, arg):
        with open(self.pklFile, 'rb') as f:
            self.set = pickle.load(f)
        self.set[param] = arg

        with open(self.pklFile, 'wb') as f:
            pickle.dump(self.set, f)

    def getParam(self, param):
        with open(self.pklFile, 'rb') as f:
            self.set = pickle.load(f)

        if param in self.set:
            return self.set[param]
        else:
            return None
