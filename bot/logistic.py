# Загрузка библиотек
import requests
from sklearn import preprocessing

import numpy as np
import pandas as pd
import tensorflow as tf
import joblib
import pickle

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import LinearSVC, SVC
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.cluster import KMeans
from sklearn.linear_model import LogisticRegression

from keras.models import Sequential

def clean_dataset(df):
    assert isinstance(df, pd.DataFrame), "df needs to be a pd.DataFrame"
    df.dropna(inplace=True)
    indices_to_keep = ~df.isin([np.nan, np.inf, -np.inf]).any(1)
    return df[indices_to_keep].astype(np.float64)

def model_compile():

# Загрузка данных
    dest = 'dataset.csv' # локальный
    df = pd.read_csv(dest,sep='^')

# Приведение дат к единому формату
    df['match_date'] = pd.to_datetime(df['match_date'].str.strip(), format='%Y-%m-%d')
    df['dob_winner'] = pd.to_datetime(df['dob_winner'].str.strip(), format='%Y-%m-%d')
    df['dob_loser'] = pd.to_datetime(df['dob_loser'].str.strip(), format='%Y-%m-%d')
    df['diff_phi1']  = df['bio_phi_winner'] -  df['bio_phi_loser']
    df['diff_emo1']  = df['bio_emo_winner'] -  df['bio_emo_loser']
    df['diff_int1']  = df['bio_int_winner'] -  df['bio_int_loser']
    df['diff_age1'] = (df['dob_winner'] - df['dob_loser']).dt.days
    df['diff_phi2']  = df['bio_phi_loser'] - df['bio_phi_winner']
    df['diff_emo2']  = df['bio_emo_loser'] - df['bio_emo_winner']
    df['diff_int2']  = df['bio_int_loser'] -  df['bio_int_winner']
    df['diff_age2'] = (df['dob_loser'] - df['dob_winner']).dt.days
    df['combine_winner'] = df['bio_phi_winner'] + df['bio_emo_winner'] +  df['bio_int_winner']
    df['combine_loser'] = df['bio_phi_loser'] + df['bio_emo_loser'] + df['bio_int_loser']
    df['age_winner'] =  (df['match_date'] - df['dob_winner'] ).dt.days
    df['age_loser'] =   (df['match_date'] - df['dob_loser'] ).dt.days
    df['diff1'] = df['combine_winner'] - df['combine_loser']
    df['diff2'] = df['combine_loser'] - df['combine_winner']
    df['diff_rank1'] = df['winner_rank']- df['loser_rank']
    df['diff_rank2'] = df['loser_rank'] - df['winner_rank']

    df_winner = df
    df_loser  = df

    df_winner = df_winner.drop(columns=['age_loser','combine_loser','loser_id','height_loser','loser_rank','loser_rank_points','height_loser','hand_class_loser','dob_loser','bio_phi_loser','bio_emo_loser','bio_int_loser','loser','critical_loser','diff_age2','diff2','diff_phi2','diff_emo2','diff_int2','diff_rank2'])
    df_winner['y'] = 1

    df_loser = df_loser.drop(columns=['age_winner','combine_winner','winner_id','height_winner','winner_rank','winner_rank_points','height_winner','hand_class_winner','dob_winner','bio_phi_winner','bio_emo_winner','bio_int_winner','winner','critical_winner','diff_age1','diff1','diff_phi1','diff_emo1','diff_int1','diff_rank1'])
    df_loser['y'] = 0

    df_winner.rename(columns = {'age_winner':'age','combine_winner':'combine','winner':'player', 'hand_class_winner': 'hand_class','winner_id':'player_id',
                            'dob_winner': 'dob', 'height_winner' : 'height', 'winner_rank':'rank', 'winner_rank_points':'points', 'bio_phi_winner': 'bio_phi',
                            'bio_emo_winner' : 'bio_emo',  'bio_int_winner' : 'bio_int' , 'critical_winner':'critical','diff_age1':'diff_age',
                            'diff_phi1':'diff_phi','diff_emo1':'diff_emo','diff_int1':'diff_int','diff1':'diff','diff_rank1':'diff_rank'}, inplace = True)
    df_loser.rename(columns = {'age_loser':'age','combine_loser': 'combine','loser':'player', 'hand_class_loser': 'hand_class','loser_id':'player_id',
                           'dob_loser': 'dob', 'height_loser' : 'height', 'loser_rank':'rank', 'loser_rank_points':'points', 'bio_phi_loser':
                           'bio_phi', 'bio_emo_loser' : 'bio_emo',  'bio_int_loser' : 'bio_int' , 'critical_loser':'critical',
                            'diff_age2':'diff_age',  'diff_phi2':'diff_phi','diff_emo2':'diff_emo','diff_int2':'diff_int','diff2':'diff','diff_rank2':'diff_rank'}, inplace = True)


    joint_dataset = pd.concat([df_winner, df_loser], axis=0)

    joint_dataset = joint_dataset.drop(columns = ['id_testdataset',	'match_date','tourney_name','tourney_location','height','critical','dob','player','player_id','tier','court','round','surface','hand_class'],axis=1)

    #joint_dataset = joint_dataset.loc[joint_dataset['hand_class'].notnull()]

    #joint_dataset['surface'] = joint_dataset['surface'].replace({'Hard': 0, 'Carpet': 1,'Clay':2,'Grass':3,'Greenset':4})

    #joint_dataset['hand_class'] = joint_dataset['hand_class'].replace({'R': 0, 'L': 1,'U':2})

    #joint_dataset['round'] = joint_dataset['round'].replace({'1st Round': 0, '2nd Round': 1,'3rd Round':2,'4th Round':3,'Quarterfinals':4,'Semifinals':5,'The Final':6,'Round Robin':7,'Third Place':8})

    #joint_dataset['court'] = joint_dataset['court'].replace({'Outdoor': 0, 'Indoor': 1})

    temp = clean_dataset(joint_dataset)
    y = temp['y']
    temp = temp.drop(columns=['y'])
    X =temp

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=1)


    ANN_model = Sequential()

    ANN_model.add(tf.keras.layers.InputLayer(input_shape=(13, )))
    # No hidden layers
    ANN_model.add(tf.keras.layers.Dense(128, activation='relu')),
    ANN_model.add(tf.keras.layers.Dense(128, activation='relu')),
    ANN_model.add(tf.keras.layers.Dense(128, activation='relu')),
    ANN_model.add(tf.keras.layers.Dense(128, activation='relu')),
    ANN_model.add(tf.keras.layers.Dense(128, activation='relu')),
    ANN_model.add(tf.keras.layers.Dense(128, activation='relu')),

    ANN_model.add(tf.keras.layers.Dense(1, activation='sigmoid'))

    optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001)
    ANN_model.compile(optimizer=optimizer,
                  loss='binary_crossentropy',
                  metrics=['accuracy'])

    '''
    history = ANN_model.fit(X_train, y_train,
                        epochs=250, batch_size=64,
                        validation_split=0.2,
                        shuffle=False)

    ANN_model.save('D:\\Projects\\Bots\\models\\my_tf_model')
    '''

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, shuffle=True, random_state=1)
    log_reg_model = LogisticRegression(max_iter=2500, random_state=42)
    # Train (fit) the model
    log_reg_model.fit(X_train, y_train)

    pkl_filename = "pickle_model.pkl"
    with open(pkl_filename, 'wb') as file:
        pickle.dump(log_reg_model, file)

    history = None

    return  history