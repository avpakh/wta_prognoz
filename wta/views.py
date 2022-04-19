from django.shortcuts import render
import pandas as pd
from .models import Players


# Create your views here.

def update_db(request):
    template_name = 'start.html'

    url = 'https://raw.githubusercontent.com/JeffSackmann/tennis_wta/master/wta_players.csv'
    df = pd.read_csv(url, index_col=None)
    print(df.info())
    df = df.

    return render(request, template_name, locals())
