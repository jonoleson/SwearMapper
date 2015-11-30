import json
import pandas as pd
import re
import numpy as np 
import geocoder


def parse_tweets(data_path, test=False):
	'''
	Reads the data txt file and appends each tweet's data into a list
	if it contains the necessary geographic tags.
	'''
	count 			 = 0
	tweets_data_path = data_path
	tweets_data 	 = []
	tweets_file 	 = open(tweets_data_path, "r")
	for line in tweets_file:
	    try:
	        tweet = json.loads(line)
	        if 'text' in tweet:
        		if tweet['place'] is not None:
        			if tweet['place']['bounding_box'] is not None:
        				if tweet['place']['bounding_box']['coordinates'] is not None:
    						tweets_data.append(tweet)
    						if test==True:
    							count += 1
    							if count > 10:
    								break
	    except:
	        continue
	return tweets_data


def build_df(tweets_data):
	# Create an empty dataframe
	tweets = pd.DataFrame()

	# Fill the dataframe with the tweet text, place name, place type, and coordinates
	tweets['text']   = map(lambda tweet: tweet['text'].lower(), tweets_data)
	tweets['coords'] = map(lambda tweet: tweet['place']['bounding_box']['coordinates'], \
						   tweets_data) 
	return tweets


def clean_text(tweets):
	# Remove all punctuation and special characters from the text
	tweets.replace(to_replace = {'text': {"[^a-zA-Z]":" "}}, inplace=True, regex=True)
	return tweets


def get_state(coordinate):
	''' 
	Convert coordinate rectangles to coordinate centroids, then use geocoder to get the state.
	I'm using the Mapbox API to do the reverse geocoding, which involved getting an access token
	and setting it as an Environment Variable like so:
	$ export MAPBOX_ACCESS_TOKEN=<Secret Access Token>
	'''
	lng, lat = zip(*coordinate[0])
	g = geocoder.mapbox([np.mean(lat), np.mean(lng)], method='reverse')
	return g.state


def get_state_column(tweets):
	# Create a column for 'state', using the get_state function defined below
	# Note: This step can take > 2 hours on a normal machine
	tweets['state'] = tweets.coords.map(get_state)
	return tweets


def drop_na(tweets):
	# Drop NA's from the dataframe
	tweets = tweets.dropna()
	return tweets


def get_swear_column(tweets):
	'''
	The swear_set is derived from this scene in the canonical cinematic
	work on profanity, "South Park: Bigger, Longer, and Uncut":
	https://www.youtube.com/watch?v=5eT0nZUROQ8#t=47
	'''
	swear_set = set(['fuck', 'shit', 'cock', 'ass', 'titties', 'boner', 
					 'bitch', 'muff', 'pussy', 'cock', 'butthole', 
					 'barbara streisand']) #sorry

	'''
	Creates a column titled 'swears' that has a '1' if the tweet contains 
	a curse word and '0' otherwise
	'''
	tweets['has_swears'] = tweets.text.map(lambda x: 1 if \
						   len(set(str(x).split()).intersection(swear_set)) > 0 else 0)

	return tweets


def get_tweet_counts(tweets):
	# Returns a new dataframe with the tweet counts grouped by state
	count_df 		= tweets.groupby('state').count()
	count_df['tweet_count'] = count_df['text']
	return count_df


def get_swear_sums(tweets):
	'''
	Returns a new dataframe with the number of tweets containing swears 
	grouped by state
	'''
	sum_df = tweets.groupby('state').sum()
	return sum_df


def join_dataframes(tweets, count_df, sum_df):
	'''
	Joins the tweets dataframe with the count_df and the sum_df, 
	returning a dataframe with the total tweet counts and count
	of tweets containing swears included
	'''
	tweets.set_index('state', inplace=True)
	tweets = tweets.join(count_df[['tweet_count']])
	tweets = tweets.join(sum_df[['has_swears']], rsuffix='_sum')
	tweets.reset_index(inplace=True)
	return tweets


def get_percentage_column(tweets):
	# Adds a column for the percentage of each state's tweets containing swearing
	tweets['percent_swears'] = 100*tweets['has_swears_sum'] / \
						       tweets['tweet_count'].astype(float)
	return tweets

def filter_states(tweets):
	# Filters out the observations of non-US states that slipped in to the dataset
	cols = np.array(['Arizona', 'Arkansas', 'California', 
       'Colorado', 'Connecticut', 'District of Columbia', 'Florida',
       'Georgia', 'Illinois', 'Indiana', 'Kentucky', 'Maryland',
       'Massachusetts', 'Michigan', 'Mississippi', 'New Jersey',
       'New Mexico', 'New York', 'North Carolina',
       'Ohio', 'Oklahoma', 'Pennsylvania', 'South Carolina',
       'Tennessee', 'Texas', 'Virginia', 'Washington'])
	# Some US states did not appear in our dataset
	tweets = tweets[(tweets['state'].isin(cols))] # Removing all non-US states
	return tweets

def group_by_state(tweets):
	# Returns the final dataframe, grouped by state
	tweets = tweets.groupby('state').mean().sort('percent_swears', ascending=False)
	tweets.reset_index(inplace=True)
	# Subset our final dataframe for only the columns we want to keep
	tweets = tweets[['state', 'tweet_count', 'has_swears_sum', 'percent_swears']]
	return tweets

def add_state_codes(tweets, test=False):
	'''
	Add state codes to dataframe (To work with Plotly visualization)
	NOTE: This array will vary depending on the sample of tweets gathered 
	during the streaming period. The tweets I gathered happened to be from 
	these states, and the dataframe sorted by swear percentage happened
	to be in this order. Automating this stage is a subject for future
	development.
	'''
	if test == False:
		tweets['code'] = ['MI', 'NJ', 'NM', 'GA', 'DC', 'IL', 
	              		  'TX', 'PA', 'OH', 'OK', 'MS', 'NY', 
	              		  'NC', 'CA', 'MD', 'VA', 'AR', 'AZ', 
	              		  'CO', 'SC', 'TN', 'IN', 'WA', 'CT', 
	              		  'MA','KY', 'FL']
	return tweets

if __name__=='__main__':
	tweets_data = parse_tweets('data/data.txt', test=True)
	tweets      = build_df(tweets_data)
	tweets      = clean_text(tweets)
	tweets      = get_state_column(tweets) 
	tweets      = drop_na(tweets)
	tweets      = get_swear_column(tweets)
	count_df    = get_tweet_counts(tweets)
	sum_df      = get_swear_sums(tweets)
	tweets      = join_dataframes(tweets, count_df, sum_df)
	tweets      = get_percentage_column(tweets)
	tweets      = filter_states(tweets)
	tweets      = group_by_state(tweets)
	tweets      = add_state_codes(tweets, test=True)
	tweets.to_csv('data/tweet_test.csv', index=False, encoding='utf-8')



