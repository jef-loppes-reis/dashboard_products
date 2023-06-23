from .postgres import *

def setup(lib:str):
    from os.path import dirname
    from dotenv import load_dotenv
    import pecista
    load_dotenv(f'{dirname(pecista.__file__)}/{lib}/.env')