import tweepy
from textblob import TextBlob
import statistics
from typing import List
import preprocessor as p

consumer_key = ""
consumer_secret = ""

auth = tweepy.AppAuthHandler(consumer_key, consumer_secret)
api = tweepy.API(auth)

def get_tweets(keyword: str) -> List[str]: # get tweets and -> returns all_tweets as a list & as a string
    all_tweets = []
    for tweet in tweepy.Cursor(api.search, q=keyword, tweet_mode='extended', lang='en').items(10):
        all_tweets.append(tweet.full_text) # Prints the full text of tweet
    return all_tweets

def clean_tweets(all_tweets: List[str]) -> List[str]: # once we get tweets we clean them since we have stuff like mentions, urls..etc. We want clean pure text. so we use preprocessor library
    tweets_clean = []
    for tweet in all_tweets:
        tweets_clean.append(p.clean(tweet))
    return tweets_clean

def get_sentiment(all_tweets: List[str]) -> List[float]: # then we pass tweets onto sentiment function
    sentiment_scores = []
    for tweet in all_tweets:
        blob = TextBlob(tweet)
        sentiment_scores.append(blob.sentiment.polarity)
    return sentiment_scores

def generate_average_sentiment_score(keyword: str) -> int:# generates average sentiment score from all the download tweets
    tweets = get_tweets(keyword)
    tweets_clean = clean_tweets(tweets)
    sentiment_scores = get_sentiment(tweets_clean)

    average_score = statistics.mean(sentiment_scores)

    return average_score

if __name__ == "__main__":
    print("Which football team do people feel more positive about right now:")
    first_thing = input()
    print("...or...")
    second_thing = input()
    print("")

    first_score = generate_average_sentiment_score(first_thing)
    second_score = generate_average_sentiment_score(second_thing)

    if (first_score > second_score):
        print(f"People are feeling more positive about {first_thing} over {second_thing}")
    else:
        print(f"People are feeling more positive about {second_thing} over {first_thing}")