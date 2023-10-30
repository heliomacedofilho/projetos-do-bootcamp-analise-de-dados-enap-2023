import pickle
import os
import pandas as pd
import requests
import plotly.express as px
import plotly.io as pio
import math
from geojson_rewind import rewind
pio.renderers.default = 'iframe'

def build_path(subfolder = 'merge'):
    folderpath = os.path.join(os.getcwd(), os.pardir, 
                              'projetoPNCP', 'dados', subfolder)
    folderpath = os.path.abspath(folderpath)
    if not os.path.exists(folderpath): 
        os.makedirs(folderpath)
    return folderpath
    
def save_data(figure, tipo_mapa, detalhe, subfolder = 'app'):
    filepath = os.path.join(build_path(subfolder), f'{tipo_mapa}-{detalhe}.pkl')
    
    with open(filepath, 'wb') as pickle_file:
        pickle.dump(figure, pickle_file)   