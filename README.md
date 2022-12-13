# luxury_hotel_sentiment_analysis

## Background and Research Question:
Recently in the post pandemic era, lots of news and analysis has been reported about how the pandemic has impact the hotel industry. But they focus too much on how the pandemic has made too much small hotels to close. But how the pandemic impact the luxurious hotels? I decided to look into the impact of Covid-19 pandemic on customers' luxurious hotel experience. I guided our investigation with two sub-questions. Then I attempted to answer them respectively by making use of two sets of data available on travel websites, namely ratings and reviews. 

The first sub-question is: do hotel brands with different positioning show varying performance before, during, and after the pandemic, as measured by rating? My hypothesis is that the pandemic had a negative impact on customers' overall hotel experience, causing a downward pressure on average ratings as well as heightened negativity expressed in customer reviews. Still, I hypothesized that hotels with different positioning might display various reactions and adjustments to the pandemic, so part of the Covid impact might be hotel-specific. 

The second sub-question is: how can I predict the sentiment (i.e. 'Good', 'Neutral', 'Bad') based off the review context? I compared sklearn model(RandomForest, SVC,Ridge/Lasso Regression etc) and deep neural network DNN model(LSTM). The richness of information that can be retrieved from reviews is worth investigating.

I picked Chicago location wise and selected three hotels by Hilton that represent three tiers, Waldorf Astoria Chicago representing a luxury hotel, DoubleTree by Hilton Hotel Chicago as a mid-level hotel, and Hilton Garden Inn Chicago Downtown riverwalk that is the cheapest among the three. We defined Year 2020 as the Covid period that sets apart the pre-Covid period and post-Covid period.


## Approaches:
### 1. Data Wrangling

Method: I aim to scrape down the data from 3 different resources: expedia.com, tripadvisor.com and twitter. Based on the CSS HTML code on expedia.com and tripadvisor.com, I can scrape down the reviewerID, review date, review rating, review title, review content and the date of stay. 

For each component, I first used Selenium with Python. I started scraping through a Chrome Web Driver. Thankfully, the total number of reviews was shown on the webpage, so I scraped that element and used regular expressions to find the number and store it as an integer, so I could know when to stop looking for more reviews. So basically the steps are: 
(1) Scrape one page at a time, based on their CSS code unique class and text, we can scrape down the data that we want.
(2) Click on the next page button whenever each page is scraped
(3) Stop when the total review number reached the total review number that we scraped at the first point.
(4) Cleaning while scrape down the text

For twitter scraping, I applied for the Twitter development account and scrape down the tweet content by setting up the credentials. First, I set up my credentials to access the Twitter API. After some deliberation on what keywords to scrape for, I decided to go after 'Waldorf Astoria','Tru By Hilton','Hilton' because that is the name of the hotels. But there is a problem in here. After I checked the quality of the twitter, I found that the data quality is extremely poor: there are very limited data and 80% are retweet and the robots. Therefore I decided not to use this data source.

Files and coding: The 9 datasets that is scraped down from Expedia.com and trip advisor.com is saved under folder of "raw_data". The code for scraping down the data is under the jupyternotebook called "Retrieve_dataset.ipynb".

### 2. Preliminary Data Cleaning

Method: To combine data from two travel website sources into a master table, some preliminary data cleaning were required. For consistency, I (1) renamed some variable names, (2) limited review ratings to one digit (with no decimal places or word descriptions like "Excellent"), (3) added a column indicating the data source (i.e. Tripadvisor or Expedia), (4) added a column indicating the hotel name (i.e. Waldorf, DoubleTree, or Hilton Garden Inn), (5) added a column indicating the time period (i.e. pre-Covid, during-Covid, or post-Covid), and (6) rescaled rating from a 0-5 scale to a 0-1 scale.

Files and coding: The master table that combines data from two websites is saved under "master_table.csv." The code for performing data cleaning and combining is under the jupyternotebook called "Retrieve_dataset.ipynb".


### 3. Plotting

Method: I planned to plot out several diagrams: (1) linear diagram about how the average rating changes over the years within three different positionings of the hotels, (2) pie chart diagrams about how the customer share different positioning of the hotels, (3) pie chart diagrams about how the customer share of different years within each positioning hotel, (4) word cloud from three different positioning hotel review content which I can identify which is the most frequent value that the customers have mentioned. Attached is the word cloud from Waldorf Hotel for reference, (5) sentiment from customer’s review changes over years for three different positioning.

Files and coding: The static plots have been saved to the folder Images. The code that produced these images are saved under the Jupyter Notebook "Sentiment_Analysis.ipynb".


### 4. Prediction Analysis

Method: I used DNN and classic sk-learn models and build up my models and compared its performance based on its accuracy.

Files and coding: The code that produced these predictions and accuracy are saved under the Jupyter Notebook "Sentiment_Analysis.ipynb"

Findings: The regression result shows a statistically significant impact of time periods and hotel brands on rating. All else equal, hotels are about 0.07 point higher in rating during the pre-pandemic period but 0.29 point lower during the pandemic compared to post-pandemic performance. All else equal, Waldorf and Hilton Garden Inn are about 0.32 and 0.01 point higher in rating compared to DoubleTree. The R-squared is 0.034, which implies there are many uncontrolled factors that could have explained the rating in a better way. 

We can see that from the  prediction result that classic sklearn model, i.e.SVC classification model does well in the two subjectivity part, i.e.Good and Bad polars, but it doesn't do well in the neutral classifier detection.

On the other hand, DNN model does well in the classifier to the good side, i.e. the detection in Good and neutral, but it doesn't do well in the bad detection. 


## Weakness and Difficulties

First, the actual number of reviews is less than what appears on the websites. This may ran into the issue of running out of the length of the list and may raise the error of Timeout Error and Valur Error at the same time. So for now, since we can have a basic idea of how many actual reviews after the first trial, we can just delete approximately 250 reviews from the total review number from the number on the expedia website, this can help as to make sure that the for loop may not run out of length, but it may cause some data loss.

Second, the set of data available on the websites is limited and I needed to extract the same set of data variables for consistency. Were a richer set of data available, our regression model could have controlled for more variables. The R-squared value would have improved accordingly. Variables of interest include the price paid, ratings for sub-categories like cleanliness, location, and service, amenities, etc. 

Third, my project used customers' review dates to imply when they stayed at the hotels, while customers do not write reviews until after they leave hotels in reality. Tripadvisor provides information on each customer's date of stays, but Expedia only displays customers' review dates instead of their actual dates of stays. Someone that stayed in the hotel at the end of 2019 might not post their review until the beginning of 2020. However, I'm unable to distinguish such customers. As a result, I used review dates for consistency.

Finally, my best guess for the underperformance of my model is because of the imbalanced dataset for too much Good classifier and because I put the imbalanced dataset into nearly the same within the three different classifier, it made the whole dataset limited. Therefore to improve the performance of the model, I would choose a more accurate way to balance the dataset. 

Also since that I'm retrieving data from both the expedia.com and also tripadvisor.com for Waldorf, so the rating for Good is more likely. Therefore if we have more time, I would turn to make more rounded way to balance the dataset in a more scientific way.