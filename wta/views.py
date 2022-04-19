import numpy as np
from django.shortcuts import render
import pandas as pd
from .models import Players

# Create your views here.

def update_db(request):
    template_name = 'start.html'

    # Players_database
    url = 'https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_players.csv'
    df = pd.read_csv(url, index_col=None)

    df['dob'] = df['dob'].fillna(0)
    df['height'] = df['height'].fillna(0)
    df['ioc'] = df['ioc'].fillna('')
    df['wikidata_id'] = df['wikidata_id'].fillna('')
    df['hand'] = df['hand'].fillna('')
    
    df = df.loc[df['dob'] != 0]

    values = df.to_dict('records')

    print(values)

    return render(request, template_name, locals())
