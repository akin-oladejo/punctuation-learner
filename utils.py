from colorama import init, Back, Style
import string


from colorama.ansi import Fore

init() #initialize colorama


def warn(msg, typ='exception'): #print colored text to terminal
    '''
    Raise exceptions and print colored text to the terminal
    
    Parameters
    ----------
    msg: str
         message to be printed
    typ: str
         values are 'exception' (default), 'file', 'folder', 'special'
    '''

    if typ == 'exception':
        raise Exception(msg)

    elif typ == 'file': style = Fore.BLUE
    elif typ == 'folder': style = Fore.LIGHTBLUE_EX
    elif typ == 'special': style = Fore.CYAN

    print(style, msg, Style.RESET_ALL)

"""-----------------------------------Utility Divider-----------------------------------------"""

# custom function for better dictionary output
def print_dict(obj:dict)->None:
    for el, val in obj.items(): #list each entry, seperated by a line with green background
        print(el)
        print(val)
        print(Back.GREEN+'\n')
        print(Style.RESET_ALL)

"""-----------------------------------Utility Divider-----------------------------------------"""