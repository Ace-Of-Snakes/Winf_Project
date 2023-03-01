import json
import matplotlib.pyplot as plt
import regex as re
import numpy as np
import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

# Load the German version of the VADER sentiment analyzer
analyzer = SentimentIntensityAnalyzer(lexicon_file="GERVaderLexicon.txt")

def get_sentiment(word, analyzer):
    """Returns the sentiment of a word as a float between -1 and 1"""
    try:
        return analyzer.polarity_scores(word).get('compound', 0.0)
    except Exception as e:
        # print(e)
        return 0.0


def calculate_emoji_sentiment(emoji_dict)->list:
    """Returns the sentiment of a word as a percentage between 0 and 1 split into negative, neutral and positive"""

    sentiment= [0,0,0] #negative, neutral, positive
    for emoji in emoji_dict.keys():
        for i in range(len(df)):
            if emoji == df["Emoji"][i]:
                sentiment[0] += df["Negative"][i] * emoji_dict[emoji]
                sentiment[1] += df["Neutral"][i] * emoji_dict[emoji]
                sentiment[2] += df["Positive"][i] * emoji_dict[emoji]
    overall_sentiment = np.sum(sentiment)
    sentiment = [x/overall_sentiment for x in sentiment]
    return sentiment

def get_reach_engagement(post, followers)->tuple:
    """Returns the reach and the engagement ratio of a post based on the number of likes and the number of followers"""
    reach = post["likes"]
    engagement_ratio = reach/followers
    return reach, engagement_ratio

def get_number_of_comments(post,followers)->float:
    """Returns the number of comments per follower"""
    return len(post["text"]["comments"].keys())/followers

def get_hashtags(post):
    hashtags = re.findall(r"#\w+", post["text"]["description"])
    return hashtags

def get_words(post):
    word_keys = post["text"]["comments"].keys()
    words = ""
    for key in word_keys:
        words += post["text"]["comments"][key]
    emojis = re.findall(r"\p{Emoji}", words)
    words = re.findall(r"\w+", words)
    return words, emojis

def calculate_statistics(filepath: str, plot:bool=False):
    global df
    # Load the emoji sentiment data
    df = pd.read_csv("ressources/Emoji_Sentiment_Data_v1.0.csv")

    # create empty lists and dictionaries for fututre data
    reach_list,like_engagement_ratios, comm_engagement_ratios = [],[],[]
    hashtag_dict, word_dict, emoji_dict = {},{},{}

    # load the json file
    data = json.load(open(filepath, "r"))
    
    followers = data["number_of_followers"]
    posts = data["posts"]
    # if last post in posts in none then remove it
    if posts[list(posts.keys())[-1]] == None:
        del posts[list(posts.keys())[-1]]
    keys = posts.keys()

    for key in keys:
        reach, engagement_ratio = get_reach_engagement(posts[key], followers)
        hashtags = get_hashtags(posts[key])
        comm_engagement = get_number_of_comments(posts[key], followers)

        for hashtag in hashtags:
            if hashtag in hashtag_dict:
                hashtag_dict[hashtag] += 1
            else:
                hashtag_dict[hashtag] = 1
        words, emojis= get_words(posts[key])
        for word in words:
            if word in word_dict:
                word_dict[word] += 1
            else:
                word_dict[word] = 1

        for emoji in emojis:
            if emoji in emoji_dict:
                emoji_dict[emoji] += 1
            else:
                emoji_dict[emoji] = 1
        like_engagement_ratios.append(engagement_ratio)
        reach_list.append(reach)
        comm_engagement_ratios.append(comm_engagement)
        print(f"""{key}: {reach}""")

    print(f"""{reach_list},{len(reach_list)}""")

    sorted_hashtags = sorted(hashtag_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
    sorted_emojis = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)

    # print(sorted_hashtags)
    # print(sorted_words)
    # print(sorted_emojis)

    emoji_sentiment = calculate_emoji_sentiment(emoji_dict)
    word_sentiment_values = [get_sentiment(word, analyzer) for word in word_dict.keys()]
    # remove all zeros from word_sentiment
    word_sentiment_values = [x for x in word_sentiment_values if x != 0]
    word_sentiment = np.sum(word_sentiment_values)/len(word_sentiment_values)

    # print(emoji_sentiment)
    # print(word_sentiment)
    if plot:
        plt.plot(list(reversed(reach_list)))

        plt.figure()
        plt.plot(np.linspace(0,len(posts), len(posts)), np.ones(len(posts))*(np.sum(like_engagement_ratios)/len(like_engagement_ratios)), label="average", color="red")
        plt.stem(list(reversed(like_engagement_ratios)))

        plt.figure()
        plt.plot(np.linspace(0,len(posts), len(posts)), np.ones(len(posts))*(np.sum(comm_engagement_ratios)/len(comm_engagement_ratios)), label="average", color="red")
        plt.stem(list(reversed(comm_engagement_ratios)))

        # pie chart of sentiment values
        plt.figure()
        explode = (0,0.1,0.2)
        colors = ["#bc5090","#ffa600","#003f5c"]
        plt.pie(emoji_sentiment, labels=["negative", "neutral", "positive"], autopct='%1.1f%%', explode=explode, startangle=90, colors=colors)
        plt.show()

    return emoji_sentiment, word_sentiment, list(reversed(like_engagement_ratios)), list(reversed(comm_engagement_ratios))
if __name__ == "__main__":
    calculate_statistics("profiles/jonasroeber.json", plot=True)