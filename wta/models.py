from django.db import models
from django.contrib.postgres.indexes import BrinIndex

# Create your models here.
# DB players

class Players(models.Model):
    LEFT = 'L'
    RIGHT = 'R'
    UNIVERSAL  = 'U'

    WORKING_HAND = [
        (LEFT, 'Left'),
        (RIGHT, 'Right'),
        (UNIVERSAL, 'Universal'),
    ]

    player_id =  models.IntegerField('id_player',blank=True,null=True,unique=True,primary_key=False)
    first_name = models.CharField('First name',max_length=100,blank=True,null=True)
    last_name = models.CharField('Last name', max_length=100, blank=True, null=True)
    hand = models.CharField('Hand',max_length=1, choices=WORKING_HAND, default=UNIVERSAL)
    dob = models.DateField('Date of birthday',blank=True,null=True)
    height = models.IntegerField('Height',null=True,blank=True)

    class Meta:
        ordering = ['player_id']
        indexes = (
            BrinIndex(fields=['player_id','first_name','last_name']),
        )

        verbose_name = 'Player'
        verbose_name_plural = 'Players'

    def __unicode__(self):
        return u" %s %s " % (self.first_name,self.last_name)

    def __str__(self):
        return self.last_name

class Rankings(models.Model):
    id_rankings = models.AutoField(primary_key=True)
    ranking_date = models.DateField('Date of birthday',blank=True,null=True)
    rank =  models.IntegerField('Rank',null=True,blank=True)
    player = models.ForeignKey(Players,blank=True,null=True,on_delete=models.PROTECT)
    points = models.IntegerField('Points',null=True,blank=True)
    tours = models.IntegerField('Tours',null=True,blank=True)

    class Meta:
        ordering = ['ranking_date']
        indexes = (
            BrinIndex(fields=['ranking_date','rank','player']),
        )

        verbose_name = 'Ranking'
        verbose_name_plural = 'Rankings'

    def __unicode__(self):
        return u" %s %s " % (self.ranking_date,self.rank)

    def get_rank(self,_player,_date):
        rank = Rankings.objects.get(player=_player,ranking_date=_date)
        return rank



#tourney_id,tourney_name,surface,draw_size,tourney_level,tourney_date,match_num,\
#winner_id,winner_seed,winner_entry,winner_name,winner_hand,winner_ht,winner_ioc,\
#winner_age,loser_id,loser_seed,loser_entry,loser_name,loser_hand,loser_ht,loser_ioc,\
#loser_age,score,best_of,round,minutes,w_ace,w_df,w_svpt,w_1stIn,w_1stWon,w_2ndWon,w_SvGms,\
#w_bpSaved,w_bpFaced,l_ace,l_df,l_svpt,l_1stIn,l_1stWon,l_2ndWon,l_SvGms,l_bpSaved,l_bpFaced,\
#winner_rank,winner_rank_points,loser_rank,loser_rank_points


class Matches(models.Model):
    id_match = models.AutoField(primary_key=True)
    

    
