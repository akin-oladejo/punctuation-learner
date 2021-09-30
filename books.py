# This script uses Open Libary APIs to obtain the id of an author and to get links to books by them if available 

import json
import requests
from tabulate import tabulate
from utils import print_dict


# Get the  identifier an author on Open Libary
def get_id(author='J.K Rowling') -> str:
    url = 'https://openlibrary.org/search/authors.json?q='
    response =requests.get(url, params={'q':author})
    if response.status_code == 200:
        # print(json.dumps(response.json(), sort_keys=True, indent=4)) # print payload
        ret = json.loads(response.content)

        if ret['numFound']==0:
            raise Exception('Author not found!')# state that author not found

        # often, several authors have the same name, or one author occurs several times
        elif ret['numFound']>1:
            print(f'\nMultiple authors ({ret["numFound"]}) found!')

            # get summary of authors
            authors = []
            for num,author in enumerate(ret["docs"], start=1):
                row = []
                row.append(num)
                row.append(author["name"])
                row.append(author["top_work"])
                row.append(author["work_count"])
                authors.append(row)
            
            print(tabulate(authors, headers=['Number', 'Name', 'Top Work', 'Work Count'])) #print summary in a table
            
            option = int(input('\n\nEnter number of desired author: ')) # Prompt user to choose author

            author_key = ret["docs"][option-1]["key"] #fetch key of selected artist
        
        else: 
            author_key = ret["docs"][0]["key"] # if only one author is returned
    else:
        raise Exception('Request not successful') # Lazy handle for now

    return author_key

# J.K Rowling's key is OL23919A
def get_works(id, limit=None): #observe that the default id is J.K Rowling's
    if limit:
        url = f'https://openlibrary.org/authors/{id}/works.json?limit={limit}'
    else:
        url = f'https://openlibrary.org/authors/{id}/works.json'
        response = requests.get(url)

        if response.status_code == 200:
            ret = json.loads(response.content)
            works = list(ret.values())[-1] # entries in the works section of an author
            print_dict(works) # print prettily

        else:
            raise Exception('Could not retrieve works by author! Maybe try another.')

def get_books(id):
    # parameters = {
    #     'bibkeys':'OLID:'+id,
    #     'format':'json',
    #     'jscmd':'data'
    # }
    url = f'https://openlibrary.org/api/books?bibkeys={id}&format=json&jsmcd=data'
    response = requests.get(url)
    print(response.json())


if __name__=="__main__":
    author_id = get_id(author_name := input('Enter artist: '))
    get_works(author_id)
    # get_books(author_id)
    # get_books('OLID:OL7235056M')


# class DownloadWorks:
#     def __init__(self) -> None:
#         pass