# Building a Travel Recommendation Engine

With around 200 countries in the world, how do I decide on the next one to visit?

This is a Case for a Recommender System to predict preferred travel destinations for a given user.

Business Cases
- Targeted Advertising on Social Media
- Personal Recommendations on Applications for Travel Agencies


## Data Sources

Travel Blogs:
- FathomAway.com
- TheBlondeAbroad.com
- AmateurTraveler.com
- BeMyTravelMuse.com
- NerdNomads.com
- OrdinaryTraveler.com

Travel Subreddits:
- Travel
- SoloTravel
- Backpacking
- DigitalNomad
- Shoestring
- CampingandHiking
- LongtermTravel
- Wanderlust
- Adventures
- RemotePlaces


## Exploratory Data Analysis

After gathering and cleaning the data, I compared the frequently used words across the travel blog articles and travel-related subreddit posts.

![Bar-Chart-of-Word-Frequencies](images/word-frequency-comparison.png)


## Model the Data

I used gensim's Doc2Vec to train a model on the text from these blogs and articles.

![Scatter plot of country similarities reduced to 2D](images/labeled_country_scatter.png)

As a result, I was able to provide recommendations of similar countries based on country name or a body of text.

![Chart of top country recommendations related to the United States](images/usa_recommendations_table.png)


## Conclusions
This is a proof of concept that can generally be applied as a travel recommendation engine, which can provide personalized recommendations to each user. However,  it would be preferred to utilize additional data resources in order to continuously evaluate and improve the model optimization.

### Limitations
- No free User input data -- clicks, likes, purchases -- to construct or evaluate the model
- A country is a very large scale

### Future Improvements
- Segment by region or city clusters
- Utilize data directly related to the desired application, including clicks, purchases, and ratings (if available)
- Add weights to more profitable items when providing recommendations
