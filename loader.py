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
        self._data = self.conv_punc(self._puncs) # convert the punctuation to numerical embeddings
        self._train, self._valid = self.split_data(self._data) # split data into train and validation subsets
        print(self._train)
        print('--------------------')
        print(self._valid)

        
    def verify_dataset(self, path_url):
        '''logic to verify that the dataset exists, contains sub-authors, warn if there are stray files/folders,
        make sure that the sub folders (which should house an author's books) contain .txt files
        and there are at least two .txt files for each other so train-validate can occur'''

        if path.exists(path_url): # check that path exists
            if path.isdir(path_url): # check that path is a folder
                l1 = os.listdir(path_url) # l1 means child of dataset path

                # alert that the main folder is empty if there are no children
                if len(l1)<1: 
                    warn("Folder empty!")
                
                for l1_sub in l1: 
                    sub_path = path_url + '/' + l1_sub # assign location of sub to a variable
                    if path.isfile(sub_path): # if parent folder contains stray files i.e files not in author folder
                        warn(f"'{sub_path}' is not in an author folder; it will not be used in training", typ='file')

                    elif path.isdir(sub_path): # what to do when the child is a directory; this is the desired case
                        txt_count = 0 # counter for the number of txt files found in author folder

                        if not self._training_files.get(l1_sub): self._training_files[l1_sub] = []
                        l2 = os.listdir(sub_path) # l2 means grandchild of dataset path

                        for l2_sub in l2:
                            sub_path2 = sub_path + '/' + l2_sub # assign location of grandchild to a variable
                            if path.isdir(sub_path2): #if a folder is found inside an author folder, ignore it
                                warn(f"'{sub_path2}' is another folder inside an author folder; it will be not be used in training", typ='folder')
                            
                            # what to do if grandchild is a file
                            elif path.isfile(sub_path2):

                                # if a granchild is not a .txt file, ignore
                                if not l2_sub.endswith('.txt'): 
                                    warn(f"'{sub_path2}' file is not a .txt file; it will not be used in training", typ='special')

                                # what to do if grandchild is a text file; this is the desired case
                                elif l2_sub.endswith('.txt'): 
                                    with open(sub_path2) as f:
                                        if len(f.readlines()) < 100:
                                            warn(f"'{sub_path2}' does not contain enough text to train; it will not be used in training", typ='file')
                                        
                                        # alas, we have gotten to a file good enough? to train with
                                        else: 
                                            txt_count += 1 # increase the count of .txt files for that author
                                            self._training_files[l1_sub].append(sub_path2) # add file path to author list
                                
                        
                        # for train-validate purposes, at least two books are needed for each author
                        if txt_count < 2:
                            self._training_files.pop(l1_sub)
                            warn(f"At least two works by '{l1_sub}' are needed to train, {txt_count} found. 'Data! We need more data!'", typ='special')
                        
                if len(self._training_files)==0: # if no .txt files found at all
                    warn("No author found in directory after search!")
                
            else: warn("Path is not a directory! :(")
        else: warn("Path does not exist! Stap playin' wimme")


    def extract_punc(self):
        '''create a dictionary. Each key represents an author. The value of that key is a list that
        contains each book's punctuation as seperate sub-lists'''
        ret = {}
        for i, j in self._training_files.items():
            for book in j:
                # book_name = book.split('/')[-1]
                with open(book) as f:
                    text = f.read()
                    if not ret.get(i): ret[i] = []
                    # ret[i].append({book_name:[i for i in text if i in string.punctuation]})
                    ret[i].append([i for i in text if i in string.punctuation])
        return ret


    def conv_punc(self, punc:dict)->dict:
        '''
        Convert the punctuation of the books to numerical representation
        Parameter
        ---------
        punc: dict : this is the dictionary that contains the punctuations of all the books

        returns
        -------`
        ret: dict: this is the converted (to numbers) version of the punctuation of all the books
        '''
        ret = {}
        for author, books in punc.items():
            if not ret.get(author): ret[author] = [] # create author elements, identical to self._punc
            for book in books:
                # convert punctuations to numerical representations
                ret[author].append(list(map(lambda x: self._punc_map[x], book))) 
        return ret


    def split_data(self, data)->tuple:
        '''
        Split the data so that the last book by each author becomes validation data
        '''
        train = {}
        valid = {}
        for author in data.keys():
            train[author] = data[author][:-1]
            valid[author] = data[author][-1]
        return train, valid


    def puncs(self):
        return self._puncs


    def data(self):
        print(self._data)