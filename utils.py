from colorama import init, Back, Style
import string
from os import path
import os

from colorama.ansi import Fore

init() #initialize colorama

# my version of the dataloader for txt files
class Loader:
    def __init__(self, path_url):
        self._path = path_url
        self._training_files = [] # path to training data files
        self._labels = set() # labels (author names)
        self.verify_dataset(self._path) # verify dataset and populate training list, labels
        

    def verify_dataset(self, path_url):
        # logic to verify that the dataset exists, contains sub-authors, warn if there are stray files/folders
        # and make sure that the sub folders (which should house an author's books) contain .txt files

        if path.exists(path_url): # check that path exists
            if path.isdir(path_url): # check that path is a folder
                l1 = os.listdir(path_url) # l1 means child of dataset path
                for l1_sub in l1: 
                    sub_path = path.join(path_url,l1_sub) # assign location of sub to a variable
                    if path.isfile(sub_path): # if parent folder contains stray files i.e files not in label folder
                        print(Fore.BLUE, f"'{sub_path}' is not in a label folder; it will be not be used in training", Style.RESET_ALL)

                    elif path.isdir(sub_path): # what to do when the child is a directory; this is the desired case
                        self._labels.add(l1_sub)
                        l2 = os.listdir(sub_path) # l2 means grandchild of dataset path
                        for l2_sub in l2:
                            sub_path2 = path.join(sub_path, l2_sub) # assign location of grandchild to a variable
                            if path.isdir(sub_path2): #if a dir is found inside a label, ignore it
                                print(Fore.LIGHTBLUE_EX, f"'{sub_path2}' is another folder inside a label folder; it will be not be used in training", Style.RESET_ALL)
                            elif path.isfile(sub_path2):
                                if l2_sub.endswith('.txt'):
                                    self._training_files.append(sub_path2)
                                    pass
                                elif not l2_sub.endswith('.txt'): # if a granchild is not a .txt file
                                    print(Fore.CYAN, f"'{sub_path2}' file is not a .txt file; it will be not be used in training", Style.RESET_ALL)
            else: raise Exception("Path is not a directory! :(")
        else: raise Exception("Path does not exist! Stap playin' wimme")

    # def training_files(self):
    #     ret = []
    #     for item in self._training_files: 
    #         ret.append(item.lstrip('data').replace('\\','/'))
    #     return ret

    def extract_punc(self):
        for i in self._training_files:
            with open(i) as obj:
                obj.read()
        self._punc = [i for i in self._data if i in string.punctuation or i == '\n']
    
    def punc(self):
        return self._punc

    # def labels(self):
    #     return self._labels


file_url = 'data'
data = Loader(file_url)
# data.training_files()
print(data._labels)
print(data._training_files)


"""-----------------------------------Utility Divider-----------------------------------------"""

# custom function for better dictionary output
def print_dict(obj:dict):
    for el in obj: #list each entry, seperated by a line with green background
        print(el)
        print(Back.GREEN+'\n')
        print(Style.RESET_ALL)
