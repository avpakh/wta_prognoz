import numpy as np
from django.shortcuts import render
import pandas as pd
from .models import Players
import requests
import urllib3
from urllib3 import ProxyManager, make_headers
import shutil
import datetime
from datetime import date


# Create your views here.


def update_db_matches(request):
    template_name = 'start.html'

    # Players_database
    url = 'http://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_matches_2022.csv'

    http = ProxyManager("http://kerio.skno.by:3210/")

    filename = 'players.csv'

    with open(filename, 'wb') as out:
        r = http.request('GET', url, preload_content=False)
        shutil.copyfileobj(r, out)

    df = pd.read_csv(filename, index_col=None)

    print (df.info())

    t = 1  / 0

    df['dob'] = df['dob'].fillna(0)
    df['height'] = df['height'].fillna(0)
    df['ioc'] = df['ioc'].fillna('')
    df['wikidata_id'] = df['wikidata_id'].fillna('')
    df['hand'] = df['hand'].fillna('')

    # df = df.loc[df['dob'] != 0]  # Ограничение на введенную даты рождения

    values = df.to_dict('records')

    for elm in values:
        player_id = elm.get('player_id')
        if not Players.objects.filter(player_id=player_id).exists():
            try:
                date_dob = datetime.datetime.strptime(str(int(elm.get('dob'))), "%Y%m%d").date()
            except:
                date_dob = date(1900, 1, 1)

            db = Players()
            db.player_id = elm.get('player_id')
            db.first_name = elm.get('name_first')
            db.last_name = elm.get('name_last')
            db.hand = elm.get('hand')
            db.dob = date_dob
            db.height = elm.get('height')
            db.save()

    return render(request, template_name, locals())


def update_db_players(request):
    template_name = 'start.html'

    # Players_database
    url = 'http://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_players'



    http = ProxyManager("http://kerio.skno.by:3210/")

    filename = 'players.csv'

    with open(filename, 'wb') as out:
        r = http.request('GET', url, preload_content=False)
        shutil.copyfileobj(r, out)

    df = pd.read_csv(filename, index_col=None )

    df['dob'] = df['dob'].fillna(0)
    df['height'] = df['height'].fillna(0)
    df['ioc'] = df['ioc'].fillna('')
    df['wikidata_id'] = df['wikidata_id'].fillna('')
    df['hand'] = df['hand'].fillna('')
    
    #df = df.loc[df['dob'] != 0]  # Ограничение на введенную даты рождения

    values = df.to_dict('records')

    for elm in values:
        player_id = elm.get('player_id')
        if not Players.objects.filter(player_id=player_id).exists():
            try:
                date_dob = datetime.datetime.strptime(str(int(elm.get('dob'))), "%Y%m%d").date()
            except:
                date_dob = date(1900,1,1)

            db = Players()
            db.player_id = elm.get('player_id')
            db.first_name = elm.get('name_first')
            db.last_name = elm.get('name_last')
            db.hand = elm.get('hand')
            db.dob = date_dob
            db.height = elm.get('height')
            db.save()

    return render(request, template_name, locals())

def start_page(request):

    template_name = 'start.html'

    update_db_matches(request)

    return render(request, template_name, locals())


