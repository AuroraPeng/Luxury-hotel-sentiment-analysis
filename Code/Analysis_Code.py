#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summary: Data Analysis
Date of last edits: 11/7/2022
Author: Zibing Liao
"""

import pandas as pd
import spacy
import nltk
from spacytextblob.spacytextblob import SpacyTextBlob
from sklearn.linear_model import LinearRegression
nlp = spacy.load("en_core_web_sm")
nlp.add_pipe('spacytextblob')
from scipy.stats.stats import pearsonr
import statistics
pd.options.mode.chained_assignment = None 
from scipy import stats
import numpy as np
import statsmodels.formula.api as smf
from statsmodels.formula.api import ols

# read dataset
master_table = pd.read_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/data/master_table.csv')

# there are rows with missing review contents; drop those rows to perform analysis
master_table2 = master_table.dropna(subset=['review_content'])

# create a polarity variable
# measures negativity vs positivity on a -1 to 1 scale
# -1 refers to negative sentiment and +1 refers to positive sentiment
polarity = []
for review in master_table2['review_content']:
    doc = nlp(review)
    polarity.append(doc._.blob.polarity)
master_table2['polarity'] = polarity

# create a subjectivity variable
# estimates the degree of subjectivity on a 0-1 scale, where 1 is completely subjective
# refers to personal opinions and judgments
sentiments = []
for review in master_table2['review_content']:
    doc2 = nlp(review)
    sentiments.append(doc2._.blob.subjectivity)
master_table2['sentiment'] = sentiments

# save the new table to csv
master_table2.to_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/data/master_table_sentiments.csv', header=True)


########################## Analysis ##########################################
# generate summary statistics for sentiments, polarity, and ratings by period and hotel
sentiment_summary = master_table2.groupby(['period', 'hotel_name'])['sentiment'].describe().reset_index()
polarity_summary = master_table2.groupby(['period', 'hotel_name'])['polarity'].describe().reset_index()
rating_summary = master_table2.groupby(['period', 'hotel_name'])['rating_rescale'].describe().reset_index()

# ols regression
# dependent variable is rating
# create dummies for hotel name (Waldorf, Hilton Garden Inn), period (pre-Covid, during-Covid)
# results are significant at 99% confidence level
dummies_hotel = pd.get_dummies(master_table2['hotel_name'])
dummies_period = pd.get_dummies(master_table2['period'])
master_table2 = pd.concat([master_table2, dummies_period], axis=1)
master_table2 = pd.concat([master_table2, dummies_hotel], axis=1)
regression_table = master_table2[['rating', 'pre-Covid', 'during-Covid', 'Hilton Garden Inn', 'Waldorf']]
regression_table = regression_table.rename(columns = {'Hilton Garden Inn': 'Hilton_Garden_Inn',
                                                      'during-Covid': 'during_Covid',
                                                      'pre-Covid': 'pre_Covid'})
regression_table["rating"] = regression_table["rating"].map(int)
reg_exp = 'rating ~ pre_Covid + during_Covid + Waldorf + Hilton_Garden_Inn'
olsr_model = smf.ols(formula=reg_exp, data=regression_table)
olsr_model_res = olsr_model.fit()
olsr_model_res.summary()

# test correlation and p-value between sentiments/polarity and ratings
# (0.30056493616891117, 1.9711863742884835e-246) shows a a week positive relationship
pearsonr(master_table2['rating'], master_table2['sentiment'])
# (0.4788922385076078, 0.0) shows a a week positive relationship
pearsonr(master_table2['rating'], master_table2['polarity'])

