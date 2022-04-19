# Generated by Django 4.0.2 on 2022-04-19 07:20

import django.contrib.postgres.indexes
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Matches',
            fields=[
                ('id_match', models.AutoField(primary_key=True, serialize=False)),
                ('match_num', models.IntegerField(blank=True, null=True, verbose_name='Match Num')),
                ('winner_seed', models.IntegerField(blank=True, null=True, verbose_name='Winner_seed')),
                ('winner_entry',
                 models.CharField(choices=[('Alt', 'Alt'), ('Q', 'Q'), ('LL', 'LL'), ('SE', 'SE'), ('WC', 'WC')],
                                  default='WC', max_length=10, verbose_name='Winner_entry')),
                ('winner_age', models.FloatField(blank=True, null=True, verbose_name='Winner_age')),
                ('loser_seed', models.IntegerField(blank=True, null=True, verbose_name='Loser_seed')),
                ('loser_entry',
                 models.CharField(choices=[('Alt', 'Alt'), ('Q', 'Q'), ('LL', 'LL'), ('SE', 'SE'), ('WC', 'WC')],
                                  default='WC', max_length=10, verbose_name='Loser_entry')),
                ('loser_age', models.FloatField(blank=True, null=True, verbose_name='Loser_age')),
                ('match_date', models.DateField(blank=True, null=True, verbose_name='Match_date')),
                ('round', models.CharField(
                    choices=[('F', 'Final'), ('QF', 'QF'), ('R128', 'R128'), ('R64', 'R64'), ('R32', 'R32'),
                             ('R16', 'R16'), ('RR', 'RR'), ('SF', 'SF')], default='R128', max_length=10,
                    verbose_name='Round')),
                ('minutes', models.IntegerField(blank=True, null=True, verbose_name='Match_duration')),
                ('winner_rank', models.IntegerField(blank=True, null=True, verbose_name='Winner_rank')),
                ('winner_rank_points', models.IntegerField(blank=True, null=True, verbose_name='Winner_rank_points')),
                ('loser_rank', models.IntegerField(blank=True, null=True, verbose_name='Winner_rank')),
                ('loser_rank_points', models.IntegerField(blank=True, null=True, verbose_name='Winner_rank_points')),
            ],
        ),
        migrations.CreateModel(
            name='Players',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('player_id', models.IntegerField(blank=True, null=True, unique=True, verbose_name='id_player')),
                ('first_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='First name')),
                ('last_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Last name')),
                ('hand', models.CharField(choices=[('L', 'Left'), ('R', 'Right'), ('U', 'Universal')], default='U',
                                          max_length=1, verbose_name='Hand')),
                ('dob', models.DateField(blank=True, null=True, verbose_name='Date of birthday')),
                ('height', models.IntegerField(blank=True, null=True, verbose_name='Height')),
            ],
            options={
                'verbose_name': 'Player',
                'verbose_name_plural': 'Players',
                'ordering': ['player_id'],
            },
        ),
        migrations.CreateModel(
            name='Tours',
            fields=[
                ('id_tour', models.AutoField(primary_key=True, serialize=False)),
                ('tourney_id', models.CharField(blank=True, max_length=50, null=True, verbose_name='Tour_id')),
                ('tourney_name', models.CharField(blank=True, max_length=100, null=True, verbose_name='Tourney_name')),
                ('draw_size', models.IntegerField(blank=True, null=True, verbose_name='Draw_size')),
                ('tourney_level',
                 models.CharField(choices=[('G', 'G'), ('I', 'I'), ('P', 'P'), ('D', 'D'), ('F', 'F'), ('PM', 'PM')],
                                  default='G', max_length=2, verbose_name='Tourney_level')),
                ('surface',
                 models.CharField(choices=[('Hard', 'Hard'), ('Clay', 'Clay'), ('Grass', 'Grass')], default='Hard',
                                  max_length=10, verbose_name='Surface')),
                ('tourney_date', models.DateField(blank=True, null=True, verbose_name='Tourney_date')),
            ],
        ),
        migrations.CreateModel(
            name='Rankings',
            fields=[
                ('id_rankings', models.AutoField(primary_key=True, serialize=False)),
                ('ranking_date', models.DateField(blank=True, null=True, verbose_name='Date of birthday')),
                ('rank', models.IntegerField(blank=True, null=True, verbose_name='Rank')),
                ('points', models.IntegerField(blank=True, null=True, verbose_name='Points')),
                ('tours', models.IntegerField(blank=True, null=True, verbose_name='Tours')),
                ('player', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                             to='wta.players')),
            ],
            options={
                'verbose_name': 'Ranking',
                'verbose_name_plural': 'Rankings',
                'ordering': ['ranking_date'],
            },
        ),
        migrations.AddIndex(
            model_name='players',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['player_id', 'first_name', 'last_name'],
                                                            name='wta_players_player__050e88_brin'),
        ),
        migrations.AddField(
            model_name='matches',
            name='loser',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='loser', to='wta.players'),
        ),
        migrations.AddField(
            model_name='matches',
            name='tourney',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='wta.tours'),
        ),
        migrations.AddField(
            model_name='matches',
            name='winner',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    related_name='winner', to='wta.players'),
        ),
        migrations.AddIndex(
            model_name='rankings',
            index=django.contrib.postgres.indexes.BrinIndex(fields=['ranking_date', 'rank', 'player'],
                                                            name='wta_ranking_ranking_dad0a3_brin'),
        ),
    ]
