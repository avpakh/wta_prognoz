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
    player_id = models.IntegerField('id_player', blank=True, null=True, unique=True, primary_key=False)
    first_name = models.CharField('First name', max_length=100, blank=True, null=True)
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

class Tours(models.Model):

    G = 'G'
    I = 'I'
    P = 'P'
    D = 'D'
    F = 'F'
    PM = 'PM'

    LEVEL = [
        (G, 'G'),
        (I, 'I'),
        (P, 'P'),
        (D, 'D'),
        (F, 'F'),
        (PM, 'PM'),
    ]

    Hard = 'Hard'
    Clay = 'Clay'
    Grass = 'Grass'

    SURFACE = [
        (Hard, 'Hard'),
        (Clay, 'Clay'),
        (Grass, 'Grass'),
    ]

    id_tour = models.AutoField(primary_key=True)
    tourney_id = models.CharField('Tour_id', max_length=50, blank=True, null=True)
    tourney_name = models.CharField('Tourney_name', max_length=100, blank=True, null=True)
    draw_size = models.CharField('Draw_size', max_length=30, null=True, blank=True)
    tourney_level = models.CharField('Tourney_level', max_length=2, choices=LEVEL, default=G)
    surface = models.CharField('Surface', max_length=10, choices=SURFACE, default=Hard)
    tourney_date = models.DateField('Tourney_date', blank=True, null=True)


#match_num,\
#winner_id,winner_seed,winner_entry,winner_name,winner_hand,winner_ht,winner_ioc,\
#winner_age,loser_id,loser_seed,loser_entry,loser_name,loser_hand,loser_ht,loser_ioc,\
#loser_age,score,best_of,round,minutes,w_ace,w_df,w_svpt,w_1stIn,w_1stWon,w_2ndWon,w_SvGms,\
#w_bpSaved,w_bpFaced,l_ace,l_df,l_svpt,l_1stIn,l_1stWon,l_2ndWon,l_SvGms,l_bpSaved,l_bpFaced,\
#winner_rank,winner_rank_points,loser_rank,loser_rank_points


class Matches(models.Model):
    F = 'F'
    QF = 'QF'
    R128 = 'R128'
    R64 = 'R64'
    R32 = 'R32'
    R16 = 'R16'
    RR = 'RR'
    SF = 'SF'

    ROUND = [
        (F, 'Final'),
        (QF, 'QF'),
        (R128, 'R128'),
        (R64, 'R64'),
        (R32, 'R32'),
        (R16, 'R16'),
        (RR, 'RR'),
        (SF, 'SF'),

    ]

    ALT = 'Alt'
    Q = 'Q'
    LL = 'LL'
    SE = 'SE'
    WC = 'WC'

    ENTRY = [
        (ALT, 'Alt'),
        (Q, 'Q'),
        (LL, 'LL'),
        (SE, 'SE'),
        (WC, 'WC'),
    ]

    id_match = models.AutoField(primary_key=True)
    match_num = models.IntegerField('Match Num', null=True, blank=True)
    tourney = models.ForeignKey(Tours, blank=True, null=True, on_delete=models.PROTECT)
    winner = models.ForeignKey(Players, blank=True, null=True, on_delete=models.PROTECT, related_name='winner')
    winner_seed = models.CharField('Winner_seed', max_length=10, null=True, blank=True)
    winner_entry = models.CharField('Winner_entry', max_length=10, choices=ENTRY, default=WC)
    winner_age = models.FloatField('Winner_age', null=True, blank=True)
    loser = models.ForeignKey(Players, blank=True, null=True, on_delete=models.PROTECT, related_name='loser')
    loser_seed = models.CharField('Loser_seed', max_length=10, null=True, blank=True)
    loser_entry = models.CharField('Loser_entry', max_length=10, choices=ENTRY, default=WC)
    loser_age = models.FloatField('Loser_age', null=True, blank=True)
    # match_date = models.DateField('Match_date', blank=True, null=True)  # calculated by match num and drawsize
    round = models.CharField('Round', max_length=10, choices=ROUND, default=R128)
    minutes = models.IntegerField('Match_duration', null=True, blank=True)
    winner_rank = models.IntegerField('Winner_rank', null=True, blank=True)
    winner_rank_points = models.IntegerField('Winner_rank_points', null=True, blank=True)
    loser_rank = models.IntegerField('Winner_rank', null=True, blank=True)
    loser_rank_points = models.IntegerField('Winner_rank_points', null=True, blank=True)


class Dataset(models.Model):
    id_dataset = models.AutoField(primary_key=True)
    match_date = models.DateField('Match_date', blank=True, null=True)  # calculated by match num and drawsize
    winner_id = models.IntegerField('id_player_winner', blank=True, null=True)
    hand_class_winner = models.IntegerField('Hand_class_winner', blank=True, null=True)
    dob_winner = models.DateField('Date of birthday_winner', blank=True, null=True)
    height_winner = models.IntegerField('Height_winner', null=True, blank=True)
    loser_id = models.IntegerField('id_player_loser', blank=True, null=True)
    hand_class_loser = models.IntegerField('Hand_class_loser', blank=True, null=True)
    dob_loser = models.DateField('Date of birthday_loser', blank=True, null=True)
    height_loser = models.IntegerField('Height_loser', null=True, blank=True)
    tourney_level_class = models.IntegerField('Level of tourney_class', blank=True, null=True)
    surface_class = models.IntegerField('Surface_class')
    winner_seed_class = models.IntegerField('Winner_seed_class')
    winner_entry_class = models.IntegerField('Winner_entry_class')
    winner_age = models.FloatField('Winner_age', null=True, blank=True)
    loser_seed_class = models.IntegerField('Loser_seed_class')
    loser_entry_class = models.IntegerField('Loser_entry_class')
    loser_age = models.FloatField('Loser_age_class', null=True, blank=True)
    round_class = models.IntegerField('Round_class')
    minutes = models.IntegerField('Match_duration', null=True, blank=True)
    winner_rank = models.IntegerField('Winner_rank', null=True, blank=True)
    winner_rank_points = models.IntegerField('Winner_rank_points', null=True, blank=True)
    loser_rank = models.IntegerField('Winner_rank', null=True, blank=True)
    loser_rank_points = models.IntegerField('Winner_rank_points', null=True, blank=True)
    bio_phi_winner = models.FloatField('Bio_phi_winner', null=True, blank=True)
    bio_emo_winner = models.FloatField('Bio_emo_winner', null=True, blank=True)
    bio_int_winner = models.FloatField('Bio_int_winner', null=True, blank=True)
    critical_winner = models.IntegerField('Winner_count of zero days', null=True, blank=True)
    bio_phi_loser = models.FloatField('Bio_phi_loser', null=True, blank=True)
    bio_emo_loser = models.FloatField('Bio_emo_loser', null=True, blank=True)
    bio_int_loser = models.FloatField('Bio_int_loser', null=True, blank=True)
    critical_loser = models.IntegerField('Loser_count of zero days', null=True, blank=True)
    winner_index_mul = models.FloatField('Winner_idx_mul', null=True, blank=True)
    loser_index_mul = models.FloatField('Loser_idx_mul', null=True, blank=True)
