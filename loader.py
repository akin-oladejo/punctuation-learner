# my version of the dataloader for txt files
from os import path
import os
from utils import warn, print_dict
import string

class Loader:
    def __init__(self, path_url):
        agr = string.punctuation # list punctuations
        self._punc_map = dict(zip(agr, range(len(agr)))) # create a mapping of punctuation to number
        self._path = path_url
        self._training_files = {} # path to training files
        self.verify_dataset(self._path) # verify dataset and populate training list
        self._puncs = self.extract_punc() # extract the punctuation in each book
        print(self._puncs)
        # self._conv = map(self.conv_punc, self._punc)
        # self.conv()

        
    def verify_dataset(self, path_url):
        # logic to verify that the dataset exists, contains sub-authors, warn if there are stray files/folders
        # and make sure that the sub folders (which should house an author's books) contain .txt files

        if path.exists(path_url): # check that path exists
            if path.isdir(path_url): # check that path is a folder
                l1 = os.listdir(path_url) # l1 means child of dataset path

                # alert that the main folder is empty if there are no children
                if len(l1)<1: 
                    warn("Folder empty!")
                
                for l1_sub in l1: 
                    sub_path = path_url + '/' + l1_sub # assign location of sub to a variable
                    if path.isfile(sub_path): # if parent folder contains stray files i.e files not in label folder
                        warn(f"'{sub_path}' is not in a label folder; it will not be used in training", typ='file')

                    elif path.isdir(sub_path): # what to do when the child is a directory; this is the desired case
                        if not self._training_files.get(l1_sub): self._training_files[l1_sub] = []
                        l2 = os.listdir(sub_path) # l2 means grandchild of dataset path
                        
                        # alert that a child folder is empty if it does not contain children
                        if len(l2)<1:
                            warn(f"'{l1_sub}' folder is empty; it will not be used in training", typ='special')

                        for l2_sub in l2:
                            sub_path2 = sub_path + '/' + l2_sub # assign location of grandchild to a variable
                            if path.isdir(sub_path2): #if a dir is found inside a label, ignore it
                                warn(f"'{sub_path2}' is another folder inside a label folder; it will be not be used in training", typ='folder')
                            
                            # what to do if grandchild is a file
                            elif path.isfile(sub_path2):

                                # what to do if grandchild is a text file; this is the desired case
                                if l2_sub.endswith('.txt'): 
                                    with open(sub_path2) as f:
                                        if len(f.readlines()) < 100:
                                            warn(f"'{l2_sub}' does not contain enough text to train; it will not be used in training", typ='file')
                                        
                                        # alas, we have gotten to a file good enough? to train with
                                        else: self._training_files[l1_sub].append(sub_path2) # add file path to author list
                                elif not l2_sub.endswith('.txt'): # if a granchild is not a .txt file
                                    warn(f"'{sub_path2}' file is not a .txt file; it will not be used in training", typ='special')
                
                if len(self._training_files)<1: # if no .txt files found at all
                    warn("No label or data found in directory after search! 'Data! We need more data!'")
            else: warn("Path is not a directory! :(")
        else: warn("Path does not exist! Stap playin' wimme")


    # write a function that creates a dictionary. Each key represents an author. 
    # The value of that key is a list that contains the punctuation in each book
    def extract_punc(self):
        # write logic to extract punc from only the actual text, maybe by stripping the pre and post sections
        
        ret = {}
        for i, j in self._training_files.items():
            for book in j:
                book_name = book.split('/')[-1]
                with open(book) as f:
                    text = f.read()
                    if not ret.get(i): ret[i] = []
                    ret[i].append({book_name:[i for i in text if i in string.punctuation]})
        return ret

    def conv_punc(self, punc):
        return(self._punc_map[punc])

    def punc(self):
        return self._punc

    def conv(self):
        print(list(self._conv))