# SwearMapper
***
### The most important Twitter analysis ever done: Mapping how much each state curses on Twitter.

## Overview

The goal of the project was to measure how much each US state curses on Twitter, as a proportion of their total tweet output. To accomplish this, I used the [Tweepy library](http://www.tweepy.org/) to interface with Twitter's streaming API, Python's [Geocoder library](https://pypi.python.org/pypi/geocoder) (in conjunction with [Mapbox's geocoding API](http://geocoder.readthedocs.org/providers/Mapbox.html#reverse-geocoding)), and [Plotly's Pandas API](https://plot.ly/pandas/choropleth-maps/#) to build an interactive [Chloropleth map](https://plot.ly/~jonoleson/15/swearmapper-cursing-on-twitter-by-state-hover-for-breakdown/). 

## Getting the Data

In building the listener, I mostly followed [this tutorial](http://adilmoujahid.com/posts/2014/07/twitter-analytics/) written by Adil Moujahid. I modified the listener filter parameters to capture only Tweets that included location tags from within the continental US. 

I ran the listener for roughly 2 hours, piping the output into a txt file with the following command in the terminal: `$ python listener.py > data.txt`

The code for this can be found in [listener.py](/blob/master/listener.py).


## Parsing the Data

Parsing the data involved loading the JSON of each Tweet's data from the data.txt file, then feeding the data into a Pandas dataframe. Each tweet had coordinate data, which I reverse-geocoded to extract the state each tweet was sent from. To use the Mapbox API I used during this step, you have to set a Mapbox Access Token as an environment variable in the directory where you're running the parser, like so: `$ export MAPBOX_ACCESS_TOKEN=<Secret Access Token>`. On ordinary hardware, the reverse geocoding step can take up to 2 hours with a dataset of roughly 50k tweets. 

The code for this can be found in [parse.py](/blob/master/parse.py).

### What is a Swear?

Easy. The swear_set is derived from this scene in the canonical cinematic work on profanity,
 ["South Park: Bigger, Longer, and Uncut":](https://www.youtube.com/watch?v=5eT0nZUROQ8) (specifically starting at the 00:47 mark).
=======
Easy. The swear_set is derived from this scene in the canonical cinematic work on profanity, ["South Park: Bigger, Longer, and Uncut"](https://www.youtube.com/watch?v=5eT0nZUROQ8) (specifically starting at the 00:47 mark).


## Results 

The top 5 swear-iest states on Twitter were:

| State        | % Tweets Containing Profanity | 
| ------------- |:-------------:| 
| Michigan | 7.75 | 
| New Jersey | 6.11 |   
| New Mexico | 5.71 |    
| Georgia | 5.37 |
| Washington DC | 5.08 |

My graphed results can be found [here](https://plot.ly/~jonoleson/15/swearmapper-cursing-on-twitter-by-state-hover-for-breakdown/), I used Plotly's Pandas API. The map must be generated from within an iPython Notebook. For instructions on getting set up with Plotly's API, see [here](https://plot.ly/python/getting-started/).  

Find the graphing code in [swearmap.ipynb](/blob/master/swearmap.ipynb).

## Caveats

My process as outlined here has several potential issues:
* If the listener receives data faster than it can store it, it will fall behind the stream and disconnect. I ran into this issue several times before getting a volume of data I was satisfied with. The listener as currently built has no control for this and it is a subject for future development. 
* Limited sample size. The dataset contained over 50k tweets but there were still a large number of states for which no data was collected. On the positive side, the proportions of tweets containing profanity was fairly consistent among the states with decent samples, typically in the 2-5% range. 
* Limited definition of profanity. I limited my definition of profanity to this clip from ["South Park: Bigger, Longer, and Uncut"](https://www.youtube.com/watch?v=5eT0nZUROQ8). Furthermore, I assumed all instances of profanity were correctly spelled and properly spaced, by far the most naive assumption ever made about Twitter.

## Conclusion

This was just an exercise, and an admittedly silly one at that. I make no claims about the results here being meaningful in any way, but I hope there at least some useful technical points in API utilization and dataframe manipulation. Cheers!

### Libraries and APIs Used:

* Numpy
* Pandas
* Geocoders/Mapbox
* Tweepy/Twitter Streaming API
* Plotly

	
