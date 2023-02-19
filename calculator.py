import json
import matplotlib.pyplot as plt
import regex as re
import numpy as np

reach_list,engagement_ratios = [],[]
hashtag_dict, word_dict = {},{}
data = json.load(open('jonasroeber.json'))
followers = int(data["number_of_followers"])
post = data["posts"]
keys = post.keys()

def get_reach_engagement(post, followers):
    number_of_likes = int(post["likes"])
    reach = int((re.sub(r"(?i)[a-z]", "", number_of_likes.group(0))).strip())
    engagement_ratio = reach/followers
    return reach, engagement_ratio

def get_hashtags(post):
    hashtags = re.findall(r"#\w+", post)
    return hashtags

def get_words(post):
    post= re.sub(r"#\w+", "", post)
    post = re.sub(r"\d+", "", post)
    words = re.findall(r"\w+", post)
    return words

for key in keys:
    reach, engagement_ratio = get_reach_engagement(post[key], followers)
    hashtags = get_hashtags(post[key])

    for hashtag in hashtags:
        if hashtag in hashtag_dict:
            hashtag_dict[hashtag] += 1
        else:
            hashtag_dict[hashtag] = 1
    words = get_words(post[key])
    for word in words:
        if word in word_dict:
            word_dict[word] += 1
        else:
            word_dict[word] = 1
    
    engagement_ratios.append(engagement_ratio)
    reach_list.append(reach)
    print(f"""{key}: {reach}""")

# print(f"""{reach_list},{len(reach_list)}""")
sorted_hashtags = sorted(hashtag_dict.items(), key=lambda x: x[1], reverse=True)
sorted_words = sorted(word_dict.items(), key=lambda x: x[1], reverse=True)
print(sorted_hashtags)
print(sorted_words)
plt.plot(list(reversed(reach_list)))
plt.stem(list(reversed(engagement_ratios)))
plt.show()