# -*- coding: utf-8 -*-
"""
Created on Sat Feb 06 18:02:10 2016

Facecook

@author: Nicolas
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#load files
aliments_df = pd.read_csv('aliments.csv', header=0) 
nutriments_df = pd.read_csv('nutriments.csv', header=0)
menu_df = pd.read_csv('menujournee.csv', header=0)

print 'menu_df : ', menu_df
print

nutriments_df = nutriments_df.drop(['nutriment'], axis = 1)

aliments_df = aliments_df.drop(['id','famille','allergene','vegetarien','visuel'], axis = 1)

merge_df = pd.merge(menu_df, aliments_df, on='nom')

merge_df = merge_df.replace({'<': ''}, regex=True)
merge_df = merge_df.replace({',': '.'}, regex=True)
merge_df = merge_df.replace({' ': ''}, regex=True)

list_conv = ['energie','proteines','lipides','dontAGS','glucides','sucre','fibres','sodium','calcium','magnesium','fer','vitamineC','vitamineD','eau']
merge_df[list_conv] = merge_df[list_conv].astype(float)

somme_df = merge_df.drop(['nom','repas'], axis = 1)

# gere les quantites
for index,row in somme_df.iterrows():
    for col in list(somme_df)[1:]:
        val = somme_df.loc[index,col] * somme_df.loc[index,'quantite (100g)']
        somme_df.set_value(index,col,val)

somme_df = somme_df.drop(['quantite (100g)'], axis = 1)

somme_df = pd.DataFrame(somme_df.sum(axis=0),columns=['Total']).T

somme_df = somme_df.append(nutriments_df, ignore_index=True)

print 'somme_df : ', somme_df
print

somme_df = somme_df.drop(somme_df.index[[1]])    #supprime la ligne d' unite des nutriments
somme_df = somme_df.reset_index(drop=True)
somme_df = somme_df.astype(float)

somme_df = somme_df.rename(index={0: 'total'})
somme_df = somme_df.rename(index={1: 'minH'})
somme_df = somme_df.rename(index={2: 'maxH'})
somme_df = somme_df.rename(index={3: 'targetH'})
somme_df = somme_df.rename(index={4: 'minF'})
somme_df = somme_df.rename(index={5: 'maxF'})
somme_df = somme_df.rename(index={6: 'targetF'})

somme_df = somme_df.transpose()

# calcul des desequilibres
somme_df['desequilibreH'] = (somme_df['targetH'] - somme_df['total']) / somme_df['total']
somme_df['desequilibreF'] = (somme_df['targetF'] - somme_df['total']) / somme_df['total']

print somme_df
print
print 'Top Carence (Homme) : ', somme_df['desequilibreH'].idxmin()
print 'Top Excedent (Homme) : ', somme_df['desequilibreH'].idxmax()
print
print 'Top Carence (Femme) : ', somme_df['desequilibreF'].idxmin()
print 'Top Excedent (Femme) : ', somme_df['desequilibreF'].idxmax()

somme_df = somme_df.drop(['desequilibreH','desequilibreF'], axis = 1)
somme_df.plot(kind='barh', title='Gauge Nutriments - Total sur une journee')  # normaliser en % des AJR pour chaque nutriment et creer un boxplot (avec min max)

# puis proposer une recette/menu permettant de corriger ce desequilibre
# attention, ne gere pas les importances des nutriments pour le moment
