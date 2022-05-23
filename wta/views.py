import numpy as np
from django.shortcuts import render
import pandas as pd
from .models import Players, Tours, Matches, Dataset
import requests
import urllib3
from urllib3 import ProxyManager, make_headers, PoolManager
import shutil
import datetime
import math
from datetime import date
from math import sin


# Create your views here.


def update_db_matches(request):
    template_name = 'start.html'

    years_range = range(1928, datetime.datetime.now().year + 1)  # range period wta from 1928 till now

    for _year in years_range:

        url = 'http://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_matches_' + str(_year) + '.csv'

        http = PoolManager()
        # http = ProxyManager("http://kerio.skno.by:3210")

        filename = 'matches.csv'

        with open(filename, 'wb') as out:
            r = http.request('GET', url, preload_content=False)
            shutil.copyfileobj(r, out)

        df = pd.read_csv(filename, index_col=None)
        print(_year)
        df['tourney_id'] = df['tourney_id'].fillna('')
        df['tourney_date'] = df['tourney_date'].fillna(0)
        df['match_num'] = df['match_num'].fillna(0)
        df['winner_id'] = df['winner_id'].fillna(0)
        df['winner_seed'] = df['winner_seed'].fillna(0)
        df['winner_entry'] = df['winner_entry'].fillna('')
        df['winner_age'] = df['winner_age'].fillna('0')
        df['loser_id'] = df['loser_id'].fillna(0)
        df['loser_seed'] = df['loser_seed'].fillna(0)
        df['loser_entry'] = df['loser_entry'].fillna('')
        df['loser_age'] = df['loser_age'].fillna('0')
        df['round'] = df['round'].fillna('')
        df['minutes'] = df['minutes'].fillna(0)
        df['winner_rank'] = df['winner_rank'].fillna(0)
        df['winner_rank_points'] = df['winner_rank_points'].fillna(0)
        df['loser_rank'] = df['winner_rank'].fillna(0)
        df['loser_rank_points'] = df['loser_rank_points'].fillna(0)

        values = df.to_dict('records')

        for elm in values:
            tourney_id = elm.get('tourney_id')
            match_num = elm.get('match_num')
            winner_id = elm.get('winner_id')
            loser_id = elm.get('loser_id')

            if ((Tours.objects.filter(tourney_id=tourney_id).exists()) and (
            Players.objects.filter(player_id=winner_id).exists())
                    and (Players.objects.filter(player_id=loser_id).exists())):
                db = Matches()
                db.tourney = Tours.objects.get(tourney_id=tourney_id)
                db.match_num = match_num
                db.winner = Players.objects.get(player_id=winner_id)
                db.winner_age = elm.get('winner_age')
                db.winner_seed = elm.get('winner_seed')
                db.winner_entry = elm.get('winner_entry')
                db.loser = Players.objects.get(player_id=loser_id)
                db.loser_seed = elm.get('loser_seed')
                db.loser_entry = elm.get('loser_entry')
                db.loser_age = elm.get('loser_age')
                db.round = elm.get('round')
                db.minutes = elm.get('minutes')
                db.winner_rank = elm.get('winner_rank')
                db.winner_rank_points = elm.get('winner_rank_points')
                db.loser_rank = elm.get('loser_rank')
                db.loser_rank_points = elm.get('loser_ank_points')
                db.save()

    return render(request, template_name, locals())


def update_db_tours(request):
    template_name = 'start.html'

    years_range = range(2021, datetime.datetime.now().year + 1)  # range period wta from 1928 till now

    for _year in years_range:

        url = 'http://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_matches_' + str(_year) + '.csv'

        http = PoolManager()

        filename = 'tours.csv'

        with open(filename, 'wb') as out:
            r = http.request('GET', url, preload_content=False)
            shutil.copyfileobj(r, out)

        df = pd.read_csv(filename, index_col=None)

        print(_year)

        df['tourney_id'] = df['tourney_id'].fillna('')
        df['tourney_name'] = df['tourney_name'].fillna('')
        df['surface'] = df['surface'].fillna('')
        df['draw_size'] = df['draw_size'].fillna('')
        df['tourney_level'] = df['tourney_level'].fillna('')
        df['tourney_date'] = df['tourney_date'].fillna(0)

        values = df.to_dict('records')

        for elm in values:
            tourney_id = elm.get('tourney_id')
            if not Tours.objects.filter(tourney_id=tourney_id).exists():
                try:
                    tourney_date = datetime.datetime.strptime(str(int(elm.get('tourney_date'))), "%Y%m%d").date()
                except:
                    tourney_date = date(1900, 1, 1)

                db = Tours()
                db.tourney_id = elm.get('tourney_id')
                db.tourney_name = elm.get('tourney_name')
                db.surface = elm.get('surface')
                db.draw_size = elm.get('draw_size')
                db.tourney_level = elm.get('tourney_level')
                db.tourney_date = tourney_date
                db.save()

    return render(request, template_name, locals())


def update_db_players(request):
    template_name = 'start.html'

    # Players_database
    url = 'http://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_players.csv'

    http = PoolManager()

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

    # df = df.loc[df['dob'] != 0]

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


def GetBiorhythms(_dob, _match_day):
    pi = math.pi
    elapsed_days = _match_day - _dob  # time delta
    print(elapsed_days)

    elapsed_days_float = elapsed_days.total_seconds()  # total seconds from query date
    elapsed_days_float /= 60  # seconds to minutes conversion
    elapsed_days_float /= 60  # minutes to hours conversion
    elapsed_days_float /= 24  # hours to days conversion

    try:

        physical = sin(2 * pi * (elapsed_days_float) / 23)
        emotional = sin(2 * pi * (elapsed_days_float) / 28)
        intellectual = sin(2 * pi * (elapsed_days_float) / 33)

        list_of_cycles = [(100 * physical) + 100, (100 * emotional) + 100, (100 * intellectual) + 100]

        return list_of_cycles

    except Exception as er3:
        print('Error in Biorhythms Formulas', str(er3))


def get_date_match(_tour_date, _match_num, _round, _size, _idtour):
    obj_tourney = Tours.objects.get(id_tour=_idtour)

    select_matches = Matches.objects.all().filter(tourney=obj_tourney)

    return {'_idtour': _idtour, 'tour_date': _tour_date, 'match_nun': _match_num, 'round': _round, 'size': _size,
            'len_m': len(select_matches)}


def create_dataset(request):
    template_name = 'start.html'

    objects_match = Matches.objects.all()

    '''
    birthday = datetime.date(1974,4,8)

    # get todays date
    today = datetime.date.today()

    # calculate age in days since birth

    v1,v2,v3 = GetBiorhythms(birthday,today)

    print (v1,v2,v3)
    '''

    v_data = []

    count_m = 0
    for obj in objects_match:

        count_m = count_m + 1

        # Условия для включения в Dataset
        # 1. Наличие у игроков дней рождения признак для невключения 1900-01-01
        # 2. Наличие даты турнира

        if ((obj.winner.dob != datetime.date(1900, 1, 1)) or (
                obj.loser.dob != datetime.date(1900, 1, 1)) or obj.tourney.tourney_date != datetime.date(1900, 1, 1)):
            # db = Dataset()
            # db.winner_id = obj.winner.pk
            # db.dob_winner = obj.winner.dob
            # db.height_winner = obj.winner.height
            # db.loser_id = obj.loser.pk
            # db.dob_loser = obj.loser.dob
            # db.height_loser = obj.loser.height
            vv = get_date_match(obj.tourney.tourney_date, obj.match_num, obj.round, obj.tourney.draw_size,
                                obj.tourney.id_tour)
            v_data.append(vv)

            print(count_m)

    df = pd.DataFrame(v_data)

    df.to_csv('matches.csv')

    print('Finish')

    print(count_m)

    return render(request, template_name, locals())


def start_page(request):
    template_name = 'start.html'

    # update_db_players(request)

    # update_db_tours(request)

    # update_db_matches(request)

    create_dataset(request)

    return render(request, template_name, locals())
