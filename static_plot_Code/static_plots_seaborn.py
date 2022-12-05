#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 24 17:51:26 2022

@author: yuchenzhou
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from wordcloud import WordCloud, STOPWORDS



# should change the file path when running it
data = pd.read_csv('/Users/yuchenzhou/Desktop/master_table.csv')



def get_columns(df):
    data_rating = df[['review_date','hotel_name','rating']]
    year = []
    for index, content in data_rating.iterrows():
        lasttwo = content['review_date'][-4:]
        year.append(lasttwo)

    data_rating['year'] = year 
    return data_rating


def get_mean_rating(df):
    data_rating_mean = data_rating.groupby(['hotel_name','year'])['rating'].mean() 
    data_rating_mean = data_rating_mean.to_frame()
    data_rating_mean = data_rating_mean.reset_index()
    data_rating_mean = data_rating_mean.drop(index=[12,13,14,15,16,17,18,31,44])
    return data_rating_mean



data_rating = get_columns(data)
data_rating_mean = get_mean_rating(data_rating)



## The first static plot : Average Hotel Ratings Over The Years
def mean_rating_plot(df):
    fig, ax = plt.subplots(figsize=(12,8))
    ax = sns.lineplot(x = 'year', y = 'rating', hue = 'hotel_name', data = df, legend=True,
                     palette=sns.color_palette(),
                     style = 'hotel_name', markers = True,size = 'hotel_name')
    ax.set_title('Average Hotel Ratings Over The Years',fontsize=20)
    # plt.savefig('Average_Hotel_Ratings_Over_The_Years.png')
mean_rating_plot(data_rating_mean)



## The second static plot: Most Common Hotel Ratings Over The Years
def get_mode_rating(df):
    data_rating_mode = df.groupby(['hotel_name','year'])['rating'].agg(pd.Series.mode) 
    data_rating_mode = data_rating_mode.to_frame()
    data_rating_mode = data_rating_mode.reset_index()
    data_rating_mode = data_rating_mode.drop(index=[12,13,14,15,16,17,18,31,44])
    return data_rating_mode
data_rating_mode = get_mode_rating(data_rating)



def mode_rating_plot(df):
    fig, ax = plt.subplots(figsize=(10,6))
    ax = sns.lineplot(x = 'year', y = 'rating', hue = 'hotel_name', data = df, legend=True,
                     palette=sns.color_palette(),
                     style = 'hotel_name',size = 'hotel_name',sizes=(4, 1))
    ax.set_title('Most Common Hotel Ratings Over The Years',fontsize=20)
    # plt.savefig('Most_Common_Hotel_Ratings_Over_The_Years.png')

mode_rating_plot(data_rating_mode)


## The third static plot: Minimum Hotel Ratings Over The Years
def get_min_rating(df):

    data_rating_min = df.groupby(['hotel_name','year'])['rating'].min() # group by time as well 
    data_rating_min = data_rating_min.to_frame()
    data_rating_min = data_rating_min.reset_index()
    data_rating_min = data_rating_min.drop(index=[12,13,14,15,16,17,18,31,44])
    return data_rating_min
data_rating_min = get_min_rating(data_rating)

def min_rating_plot(df):
    fig, ax = plt.subplots(figsize=(12,8))
    ax = sns.lineplot(x = 'year', y = 'rating', hue = 'hotel_name', data = df, legend=True,
                  palette=sns.color_palette(),
                 style = 'hotel_name', markers = True,size = 'hotel_name',sizes=(4, 1))
    ax.set_title('Minimum Hotel Ratings Over The Years',fontsize=20)   
    # plt.savefig('Minimum_Hotel_Ratings_Over_The_Years.png')
min_rating_plot(data_rating_min)


## The fourth static plot: Share of Guest Number in different years (all hotels)
def get_guest_data(df):
    data_guest = df[['hotel_name','review_date']]
    year2 = []
    for index, content in data_guest.iterrows():
        lasttwo = content['review_date'][-2:]
        year2.append(lasttwo)

    data_guest['year'] = year2 
    
    return data_guest

def guestdata_plot(df):
    data_guest_new = df.groupby(['hotel_name','year'])['hotel_name'].count() # group by time as well 
    data_guest_new = data_guest_new.to_frame()
    data_guest_new.columns = ['guest_number']
    data_guest_new = data_guest_new.reset_index()
    data_guest_new = pd.DataFrame(data_guest_new,index=[8,9,10,11,27,28,29,30,40,41,42,43])
    return data_guest_new

data_guest = get_guest_data(data)
guest_data_new = guestdata_plot(data_guest)

def pie_all(df):
    fig, ax = plt.subplots(figsize=(12,8))
    ax=sns.set_style ("whitegrid")
    ax = sns.barplot(x="year", y="guest_number", hue="hotel_name", data= df,
                palette=sns.color_palette("hls", 8))
    ax.set_title('Guest Number Over the Years',fontsize=20)
    # plt.savefig('Share_of_Guest_Number_in_different_years_all.png')
    
pie_all(guest_data_new)


## The fifth static plot: Share of Guest Number in different years (Hilton Garden Inn)
def pie_HG(df):
    fig, ax = plt.subplots(figsize=(8,6))
    ax=sns.set_style ("whitegrid")
    ax = sns.barplot(x="year", y="guest_number", data=df[df['hotel_name']=='Hilton Garden Inn'],
                palette=sns.color_palette("hls", 8))
    ax.set_title('Guest Number Over the Years of Hilton Garden Inn',fontsize=18)
    # plt.savefig('Share_of_Guest_Number_in_different_years_Hilton_Garden_Inn.png')
    
pie_HG(guest_data_new)


## The sixth static plot: Share of Guest Number in different years (Double Tree)
def pie_DT(df):
    fig, ax = plt.subplots(figsize=(8,6))
    ax=sns.set_style ("whitegrid")
    ax = sns.barplot(x="year", y="guest_number", data=df[df['hotel_name']=='DoubleTree'],
                    palette=sns.color_palette("hls", 8))
    ax.set_title('Guest Number Over the Years of Double Tree',fontsize=18)
    # plt.savefig('Share_of_Guest_Number_in_different_years_Double_Tree.png')

pie_DT(guest_data_new)


## The seventh static plot: Share of Guest Number in different years (Waldorf)
def pie_WD(df):
    fig, ax = plt.subplots(figsize=(8,6))
    ax=sns.set_style ("whitegrid")
    ax = sns.barplot(x="year", y="guest_number", data=df[df['hotel_name']=='Waldorf'],
                    palette=sns.color_palette("hls", 8))
    ax.set_title('Guest Number Over the Years of Waldorf',fontsize=18)
    # plt.savefig('Share_of_Guest_Number_in_different_years_Waldorf.png')

pie_WD(guest_data_new)


## The eighth static plot: word cloud of all hotels
df = pd.read_csv(url, encoding ="latin-1")

comment_words = ''
stopwords = set(STOPWORDS)
 

for val in df['review_content']:
    
    val = str(val)

    tokens = val.split()

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)


fig, ax = plt.subplots(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
# plt.savefig('wordcloud_all.png')


## The ninth static plot: word cloud of Double Tree
df = pd.read_csv(url, encoding ="latin-1")
df = df[df['hotel_name']=='DoubleTree']

comment_words = ''
stopwords = set(STOPWORDS)
 

for val in df['review_content']:
    
    val = str(val)

    tokens = val.split()

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)


fig, ax = plt.subplots(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
# plt.savefig('wordcloud_Double_Tree.png')



## The tenth static plot: word cloud of Hilton Garden Inn
df = pd.read_csv(url, encoding ="latin-1")
df = df[df['hotel_name']=='Hilton Garden Inn']

comment_words = ''
stopwords = set(STOPWORDS)
 

for val in df['review_content']:
    
    val = str(val)

    tokens = val.split()

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)


fig, ax = plt.subplots(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
# plt.savefig('wordcloud_Hilton_Garden_Inn.png')



## The eleventh static plot: word cloud of Waldorf
df = pd.read_csv(url, encoding ="latin-1")
df = df[df['hotel_name']=='Waldorf']

comment_words = ''
stopwords = set(STOPWORDS)
 

for val in df['review_content']:
    
    val = str(val)

    tokens = val.split()

    for i in range(len(tokens)):
        tokens[i] = tokens[i].lower()
     
    comment_words += " ".join(tokens)+" "
 
wordcloud = WordCloud(width = 800, height = 800,
                background_color ='white',
                stopwords = stopwords,
                min_font_size = 10).generate(comment_words)


fig, ax = plt.subplots(figsize=(8,8))
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad = 0)
# plt.savefig('wordcloud_Waldorf.png')



































