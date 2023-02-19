import json
import matplotlib.pyplot as plt
import regex as re
import numpy as np
import pandas as pd


df = pd.read_csv("Emoji_Sentiment_Data_v1.0.csv")
print(df["Emoji"].values)
reach_list,engagement_ratios = [],[]
hashtag_dict, word_dict, emoji_dict = {},{},{}
data = json.load(open('jonasroeber.json'))
followers = data["number_of_followers"]
post = data["posts"]
keys = post.keys()

def calculate_sentiment(emoji_dict):
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

def get_reach_engagement(post, followers):
    reach = post["likes"]
    engagement_ratio = reach/followers
    return reach, engagement_ratio

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

for key in keys:
    reach, engagement_ratio = get_reach_engagement(post[key], followers)
    hashtags = get_hashtags(post[key])

    for hashtag in hashtags:
        if hashtag in hashtag_dict:
            hashtag_dict[hashtag] += 1
        else:
            hashtag_dict[hashtag] = 1
    words, emojis= get_words(post[key])
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
    engagement_ratios.append(engagement_ratio)
    reach_list.append(reach)
    print(f"""{key}: {reach}""")

print(f"""{reach_list},{len(reach_list)}""")
sorted_hashtags = sorted(hashtag_dict.items(), key=lambda x: x[1], reverse=True)
sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
sorted_emojis = sorted(emoji_dict.items(), key=lambda x: x[1], reverse=True)
print(calculate_sentiment(emoji_dict))
# print(sorted_hashtags)
# print(sorted_words)
# print(sorted_emojis)
plt.plot(list(reversed(reach_list)))
plt.figure()
plt.plot(np.linspace(0,len(post), len(post)), np.ones(len(post))*(np.sum(engagement_ratios)/len(engagement_ratios)), label="average", color="red")
plt.stem(list(reversed(engagement_ratios)))
# pie chart of sentiment values
plt.figure()
plt.pie(calculate_sentiment(emoji_dict), labels=["negative", "neutral", "positive"], autopct='%1.1f%%')
plt.show()