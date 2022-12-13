#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 10:05:21 2022

@author: yuchenzhou
"""

import pandas as pd
import matplotlib.pyplot as plt
import os
import pandas_datareader.data as web

from shiny import App, render, ui, reactive
import pandas as pd
import seaborn as sns



app_ui = ui.page_fluid(
    ui.row(ui.column(12, ui.h1('Dashbord : Hotel Experiences of Hilton Group during and post Covid19 in Chicago Area'), ui.hr()),align='center'), 

    
 ##############################
     ui.row(ui.column(6, ui.em(ui.h2("Guest Number Over the Years")), 
                  
                  align='center'),
            ui.column(6, ui.em(ui.h2("Rating Trend Over the Years")), 
                  
                  align='center'),        
            
            ), 
    
    ui.row(ui.column(4, ui.input_select(id='guest_share', 
                                        label='Choose the hotel you want to see',
                                        choices=['Overall','DoubleTree','Hilton Garden Inn','Waldorf']),
                                        offset=1,
                                        align='center'),
           
           
           ui.column(4, ui.input_select(id='rating_aggregation', 
                                        label='Choose the aggregation method',
                                        choices=['Mean','Mode','Minimum']),
                                        offset=2, 
                                        align='center')),
    
   

    
    ui.row(ui.column(6, ui.output_plot('guest_share_plot')),
           ui.column(6, ui.output_plot('rating_plot'))),
    
    
    
    
    #############################
    
    ui.row(ui.column(6, ui.em(ui.h2("Most Frequent Words in Comments")), 
                  offset=3, 
                  align='center')), 
    
    
    ui.row(ui.column(8, ui.input_select(id='word_cloud', 
                                        label='choose the hotel you want to see',
                                        choices=['Overall','DoubleTree','Hilton Garden Inn','Waldorf']),
                                        offset=2,
                                        align='center'
                                        )),
    
    
    ui.row(ui.column(12, ui.output_plot('word_cloud_plot'))
           )
    
    
)




def server(input, output, session):
    @reactive.Calc
    def data_rating_agg(): 
        # should change the path when running it
        data = pd.read_csv('/Users/yuchenzhou/Desktop/master_table.csv')
        def get_columns(df):
            
            data_rating = df[['review_date','hotel_name','rating']]
            year = []
            for index, content in data_rating.iterrows():
                lasttwo = content['review_date'][-2:]
                year.append(lasttwo)
    
            data_rating['year'] = year 
            return data_rating
         
        data_rating = get_columns(data)
        
        def get_mean_rating(df):
            data_rating_mean = data_rating.groupby(['hotel_name','year'])['rating'].mean() 
            data_rating_mean = data_rating_mean.to_frame()
            data_rating_mean = data_rating_mean.reset_index()
            data_rating_mean = data_rating_mean.drop(index=[12,13,14,15,16,17,18,31,32,33,44])
            return data_rating_mean
        
        data_rating_mean = get_mean_rating(data_rating)

        def get_mode_rating(df):
            data_rating_mode = df.groupby(['hotel_name','year'])['rating'].agg(pd.Series.mode) 
            data_rating_mode = data_rating_mode.to_frame()
            data_rating_mode = data_rating_mode.reset_index()
            data_rating_mode = data_rating_mode.drop(index=[12,13,14,15,16,17,18,31,32,33,44])
            return data_rating_mode
        
        data_rating_mode = get_mode_rating(data_rating)
        
        def get_min_rating(df):
        
            data_rating_min = df.groupby(['hotel_name','year'])['rating'].min() 
            data_rating_min = data_rating_min.to_frame()
            data_rating_min = data_rating_min.reset_index()
            data_rating_min = data_rating_min.drop(index=[12,13,14,15,16,17,18,31,32,33,44])
            return data_rating_min
        data_rating_min = get_min_rating(data_rating)
        
        
        return data_rating_mean,data_rating_mode,data_rating_min
    
    
    
    @output
    @render.plot
    def rating_plot():
        
        def mean_rating_plot():
            data_rating_mean,data_rating_mode,data_rating_min = data_rating_agg()
            import seaborn as sns
            fig, ax = plt.subplots(figsize=(12,8))
            ax = sns.lineplot(x = 'year', y = 'rating', hue = 'hotel_name', data =data_rating_mean, legend=True,
                             palette=sns.color_palette(),
                             style = 'hotel_name', markers = True,size = 'hotel_name')
            ax.set_title('Average Hotel Ratings Over The Years',fontsize=15)

        def mode_rating_plot():
            data_rating_mean,data_rating_mode,data_rating_min = data_rating_agg()

            import seaborn as sns
            fig, ax = plt.subplots(figsize=(10,6))
            ax = sns.lineplot(x = 'year', y = 'rating', hue = 'hotel_name', data = data_rating_mode, legend=True,
                             palette=sns.color_palette(),
                             style = 'hotel_name',size = 'hotel_name',sizes=(4, 1))
            ax.set_title('Most Common Hotel Ratings Over The Years',fontsize=15)    
    
        def min_rating_plot():
            data_rating_mean,data_rating_mode,data_rating_min = data_rating_agg()
            import seaborn as sns
            fig, ax = plt.subplots(figsize=(12,8))
            ax = sns.lineplot(x = 'year', y = 'rating', hue = 'hotel_name', data = data_rating_min, legend=True,
                              palette=sns.color_palette(),
                             style = 'hotel_name', markers = True,size = 'hotel_name',sizes=(4, 1))
            ax.set_title('Minimum Hotel Ratings Over The Years',fontsize=15)   
    
        if input.rating_aggregation() == 'Mean':
            return mean_rating_plot()
        elif input.rating_aggregation() == 'Mode':
            return mode_rating_plot()
        else:
            return min_rating_plot()

    
    @reactive.Calc   
    def data_guest():
        # should change the path when running it
        data = pd.read_csv('/Users/yuchenzhou/Desktop/master_table.csv')
        def get_guest_data(df):
            data_guest = df[['hotel_name','review_date']]
            year2 = []
            for index, content in data_guest.iterrows():
                lasttwo = content['review_date'][-2:]
                year2.append(lasttwo)
        
            data_guest['year'] = year2 
            return data_guest
        data_guest = get_guest_data(data)
        
        def guestdata_plot(df):
            data_guest_new = df.groupby(['hotel_name','year'])['hotel_name'].count() # group by time as well 
            data_guest_new = data_guest_new.to_frame()
            data_guest_new.columns = ['guest_number']
            data_guest_new = data_guest_new.reset_index()
            data_guest_new = pd.DataFrame(data_guest_new,index=[8,9,10,11,27,28,29,30,40,41,42,43])
            return data_guest_new
        
        guest_data_new = guestdata_plot(data_guest)
        
        return guest_data_new
        
    
    @output
    @render.plot
    def guest_share_plot():
        guest_data_new = data_guest()
        def bar_DT():
            import seaborn as sns
            fig, ax = plt.subplots(figsize=(8,6))
            ax=sns.set_style ("whitegrid")
            ax = sns.barplot(x="year", y="guest_number", data=guest_data_new[guest_data_new['hotel_name']=='DoubleTree'],
                            palette=sns.color_palette("hls", 8))
            ax.set_title('Guest Number Over the Years of Double Tree',fontsize=15)
        
        def bar_HGI():
            import seaborn as sns
            fig, ax = plt.subplots(figsize= (8,6))
            ax=sns.set_style ("whitegrid")
            ax = sns.barplot(x="year", y="guest_number", data=guest_data_new[guest_data_new['hotel_name']=='Hilton Garden Inn'],
                            palette=sns.color_palette("hls", 8))
            ax.set_title('Guest Number Over the Years of Hilton Garden Inn',fontsize=15)
        
        def bar_WDF():
            import seaborn as sns
            fig, ax = plt.subplots(figsize=(8,6))
            ax=sns.set_style ("whitegrid")
            ax = sns.barplot(x="year", y="guest_number", data=guest_data_new[guest_data_new['hotel_name']=='Waldorf'],
                            palette=sns.color_palette("hls", 8))
            ax.set_title('Guest Number Over the Years of Waldorf',fontsize=15)  
        
        def bar_all():
            import seaborn as sns
            fig, ax = plt.subplots(figsize=(12,8))
            ax=sns.set_style ("whitegrid")
            ax = sns.barplot(x="year", y="guest_number", hue="hotel_name", data=guest_data_new,
                            palette=sns.color_palette("hls", 8))
            ax.set_title('Guest Number Over the Years',fontsize=15)           
        
        if input.guest_share() == 'DoubleTree':
            return bar_DT()
        elif input.guest_share() == 'Hilton Garden Inn':
            return bar_HGI()
        elif input.guest_share() == 'Waldorf':
            return bar_WDF()
        else:
            return bar_all()
    
    @output
    @render.plot

    
    def word_cloud_plot():
        from wordcloud import WordCloud, STOPWORDS
        import matplotlib.pyplot as plt
        import pandas as pd

        def word_waldorf():
            # should change the path when running it
            df = pd.read_csv(r"/Users/yuchenzhou/Desktop/master_table.csv", encoding ="latin-1")
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

            fig, ax = plt.subplots(figsize=(10,10))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad = 0)
         
            
        def word_Hilton_Garden_Inn():
            # should change the path when running it
            df = pd.read_csv(r"/Users/yuchenzhou/Desktop/master_table.csv", encoding ="latin-1")
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
 
            fig, ax = plt.subplots(figsize=(10,10))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad = 0)     
        
        def word_Double_Tree():
            # should change the path when running it
            df = pd.read_csv(r"/Users/yuchenzhou/Desktop/master_table.csv", encoding ="latin-1")
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

            fig, ax = plt.subplots(figsize=(10,10))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad = 0)      
            
        def word_all():
            # should change the path when running it
            df = pd.read_csv(r"/Users/yuchenzhou/Desktop/master_table.csv", encoding ="latin-1")
            
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
            
            
            fig, ax = plt.subplots(figsize=(10,10))
            plt.imshow(wordcloud)
            plt.axis("off")
            plt.tight_layout(pad = 0)
        
        if input.word_cloud() == 'Waldorf':
            return word_waldorf()
        elif input.word_cloud()=='Hilton Garden Inn':
            return word_Hilton_Garden_Inn()
        elif input.word_cloud()== 'Double Tree':
            return word_Double_Tree()
        else:
            return word_all()  
    
    
    
    

    
app = App(app_ui, server)