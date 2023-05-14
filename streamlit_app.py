# First, let's install the necessary Python libraries
!pip install streamlit
!pip install pandas
!pip install tweepy
!pip install newspaper3k

# Import necessary libraries
import streamlit as st
import pandas as pd
import tweepy
from newspaper import Article

# Set up Twitter API credentials and authentication    
consumer_key = st.secrets['consumer_key']
consumer_secret = st.secrets['consumer_secret']
access_token = st.secrets['access_token']
access_token_secret = st.secrets['access_token_secret']

#check if the credentials are correct
try:
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth)
    api.verify_credentials()
    st.sidebar.success("Twitter Authentication Success")
except tweepy.TweepError as e:
    st.sidebar.error("Invalid or Expired Twitter Credentials, please check again!")
    st.write("Error:", e)


# Set up function to retrieve tweets
def get_tweets(keyword, count):
    tweets_data = {'user': [],'text': [],'date': []}
    try:
        tweets = tweepy.Cursor(api.search_tweets,q=keyword, lang='en', tweet_mode='extended').items(count)
        for tweet in tweets:
            if 'retweeted_status' in dir(tweet):
                tweets_data['user'].append(tweet.retweeted_status.user.screen_name)
                tweets_data['text'].append(tweet.retweeted_status.full_text)
                tweets_data['date'].append(tweet.retweeted_status.created_at)

            else:
                tweets_data['user'].append(tweet.user.screen_name)
                tweets_data['text'].append(tweet.full_text)
                tweets_data['date'].append(tweet.created_at)
        return pd.DataFrame(tweets_data)
    except tweepy.TweepError as e:
        st.write("Error:", e)


# Set up function to retrieve news articles
def get_articles(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        st.write("Error:", e)


# Set up Streamlit app interface
st.title('News and Twitter Analysis')
option = st.sidebar.selectbox('Select an option', ['Twitter Analysis', 'News Analysis'])

# Twitter Analysis
if option == 'Twitter Analysis':
    st.header('Twitter Analysis')
    keyword = st.text_input('Enter a keyword')
    count = st.slider('Select the number of tweets to retrieve', 1, 100, 10)
    if st.button('Get Tweets'):
        if keyword and count:
          tweets = get_tweets(keyword, count)
          if tweets.empty:
              st.write("No tweets found for the given keyword!")
          else:
              st.write(tweets)
        else:
          st.write("Please fill in both the keyword and count fields")

# News Analysis
if option == 'News Analysis':
    st.header('News Analysis')
    url = st.text_input('Enter a news article URL')
    if st.button('Get Article'):
        if url:
          article_text = get_articles(url)
          if not article_text:
              st.write("Could not fetch article for the given URL, please check if the URL is valid")
          else:
              st.write(article_text)
        else:
          st.write("Please fill in the URL field")


# End of code

# Import necessary libraries
import streamlit as st
import pandas as pd
import tweepy
from newspaper import Article
from typing import List, Dict, Union

#authenticating Twitter API
def authenticate_twitter(credentials: Dict[str,str]):
    try:
        auth = tweepy.OAuthHandler(credentials['consumer_key'], credentials['consumer_secret'])
        auth.set_access_token(credentials['access_token'], credentials['access_token_secret'])
        api = tweepy.API(auth)
        api.verify_credentials()
        st.sidebar.success("Twitter Authentication Success")
        return api
    except tweepy.TweepError as e:
        st.sidebar.error("Invalid or Expired Twitter Credentials, please check again!")
        st.write("Error:", e)
        return None

# Set up function to retrieve tweets
def get_tweets(api, keyword: str, count: int) -> pd.DataFrame:
    tweets_data = {'user': [],'text': [],'date': []}
    try:
        tweets = tweepy.Cursor(api.search_tweets,q=keyword, lang='en', tweet_mode='extended').items(count)
        for tweet in tweets:
            if 'retweeted_status' in dir(tweet):
                tweets_data['user'].append(tweet.retweeted_status.user.screen_name)
                tweets_data['text'].append(tweet.retweeted_status.full_text)
                tweets_data['date'].append(tweet.retweeted_status.created_at)

            else:
                tweets_data['user'].append(tweet.user.screen_name)
                tweets_data['text'].append(tweet.full_text)
                tweets_data['date'].append(tweet.created_at)
        return pd.DataFrame(tweets_data)
    except tweepy.TweepError as e:
        st.write("Error:", e)

# Set up function to retrieve news articles
def get_articles(url: str) -> Union[None,str]:
    try:
        article = Article(url)
        article.download()
        article.parse()
        return article.text
    except Exception as e:
        st.write("Error:", e)
        return None

# Set up Streamlit app interface
def app_ui():
    st.title('News and Twitter Analysis')

    # Sidebar for Twitter and News Analysis
    option = st.sidebar.selectbox('Select an option', ['Twitter Analysis', 'News Analysis'])

    if option == 'Twitter Analysis':
        st.header('Twitter Analysis')
        keywords = st.text_input('Enter a comma-separated keyword list')
        count = st.number_input('Select the number of tweets to retrieve', min_value=1, max_value=100, value=10)

        # Twitter Authentication and Authorization
        if not st.secrets:
            st.write("No Twitter access credentials found.")
            st.stop()
        else:
            api = authenticate_twitter(st.secrets)

        # Retrieve tweets
        if st.button('Get Tweets'):
            if keywords and api:
                # Retrieving tweets using the given keywords
                keywords = [keyword.strip() for keyword in keywords.split(',')]
                tweets_df = pd.DataFrame()
                for keyword in keywords:
                    tweets = get_tweets(api, keyword, count)
                    if tweets is not None:
                        tweets_df = pd.concat([tweets_df, tweets])

                # Display tweets dataframe
                if not tweets_df.empty:
                    st.write(tweets_df)
                else:
                    st.write("No tweets found for the given keyword(s)!")
            else:
                st.write("Please enter keyword(s) and make sure Twitter access credentials are valid") 

    elif option == 'News Analysis':
        st.header('News Analysis')
        url = st.text_input('Enter a news article URL')

        # Retrieve news article
        if st.button('Get Article'):
            if url:
                article_text = get_articles(url)
                if article_text is not None:
                    st.write(article_text)
                else:
                    st.write("Could not fetch article for the given URL, please check if the URL is valid")
            else:
                st.write("Please enter a news article URL")

# Initialize the application
if __name__ == '__main__':
    app_ui()

# End of code 
# changes - Added comments, encapsulated the functions, added twitter authentication and modified the ui flow. Made sure that all the errors are handled
