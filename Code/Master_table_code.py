#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Summary: Clean and Combine Datasets
Date of last edits: 11/4/2022
Author: Zibing Liao
Reviewer: [insert name]
"""
import pandas as pd

# Waldorf
# Tripadvisor
waldorf_reviews = pd.read_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/Data/waldorf_reviews_tripadvisor.csv')
waldorf_reviews['hotel_name'] = 'Waldorf'
waldorf_reviews['source_name'] = 'Tripadvisor'
# Expedia
expedia_waldorf_reviews = pd.read_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/Data/expedia_waldorf_reviews.csv')
expedia_waldorf_reviews['hotel_name'] = 'Waldorf'
expedia_waldorf_reviews['source_name'] = 'Expedia'
expedia_waldorf_reviews = expedia_waldorf_reviews.rename(columns={'review_rating': 'rating'})
expedia_waldorf_reviews['rating'] = expedia_waldorf_reviews['rating'].str[0]
expedia_waldorf_reviews['rating'].astype(float)

# DoubleTree by Hilton Chicago
# Tripadvisor
doubletree_reviews = pd.read_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/Data/doubletree_reviews_tripadvisor.csv')
doubletree_reviews['hotel_name'] = 'DoubleTree'
doubletree_reviews['source_name'] = 'Tripadvisor'
# Expedia
expedia_doubletree_reviews = pd.read_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/Data/expedia_doubletree_reviews.csv')
expedia_doubletree_reviews['hotel_name'] = 'DoubleTree'
expedia_doubletree_reviews['source_name'] = 'Expedia'
expedia_doubletree_reviews = expedia_doubletree_reviews.rename(columns={'review_rating': 'rating'})
expedia_doubletree_reviews['rating'] = expedia_doubletree_reviews['rating'].str[0]
expedia_doubletree_reviews['rating'].astype(float)

# Hilton Garden Inn Chicago
# Tripadvisor
hiltongarden_reviews = pd.read_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/Data/hiltongarden_reviews_tripadvisor.csv')
hiltongarden_reviews['hotel_name'] = 'Hilton Garden Inn'
hiltongarden_reviews['source_name'] = 'Tripadvisor'

# Expedia
expedia_hiltongarden_reviews = pd.read_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/Data/expedia_hiltongarden_reviews.csv')
expedia_hiltongarden_reviews['hotel_name'] = 'Hilton Garden Inn'
expedia_hiltongarden_reviews['source_name'] = 'Expedia'
expedia_hiltongarden_reviews = expedia_hiltongarden_reviews.rename(columns={'review_rating': 'rating'})
expedia_hiltongarden_reviews['rating'] = expedia_hiltongarden_reviews['rating'].str[0]
expedia_hiltongarden_reviews['rating'].astype(float)

# Combine all datasets and export
master_table = pd.concat([waldorf_reviews, 
                          expedia_waldorf_reviews, 
                          doubletree_reviews, 
                          expedia_doubletree_reviews, 
                          hiltongarden_reviews, 
                          expedia_hiltongarden_reviews])

# Define the following periods:
# post-Covid period as Year > 2020, during-Covid as Year = 2020, pre-Covid as Year < 2020
period = []
for i in master_table['review_date']:
    if (i.endswith('2020') == True):
        x = 'during-Covid'    
        period.append(x)
    elif (i.endswith(('2021', '2022'))):     
        x = 'post-Covid'
        period.append(x)
    else:    
        x = 'pre-Covid'
        period.append(x)
master_table['period'] = period

# scale rating to 0-1
master_table['rating_rescale'] = master_table['rating'].astype(int)/5
master_table['review_content'].astype(str)


master_table.to_csv(r'/Users/zibingliao/Documents/GitHub/final-project-brand_careaway_sentimental_anlysis/Data/Master_table.csv', header=True)

master_table.groupby(['period', 'hotel_name', 'source_name']).describe()

