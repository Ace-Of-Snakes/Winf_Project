import numpy as np
def scoring_algorithm(sentiment1, sentiment2,values1,values2,top_industries):

    # get all variables and reformat them to be used in the algorithm
    emoji_sentiment = sentiment1[2]
    word_sentiment = sentiment2
    average_like_engagement = np.sum(values1)/len(values1)
    average_comm_engagement = np.sum(values2)/len(values2)
    scoring_seed = 0.99254

    # print all variables
    print(f"""emoji_sentiment: {emoji_sentiment} word_sentiment: {word_sentiment} average_like_engagement: {average_like_engagement} average_comm_engagement: {average_comm_engagement} top_industries: {top_industries}""")


    # calculate score after decided formula
    score1 = (average_like_engagement*3 + average_comm_engagement*50 +emoji_sentiment*2 + word_sentiment*2)/11*10 * scoring_seed

    # calculate score2

    # total_hash_vals = values of all top_industries hashtags added together
    total_hash_vals = [val[1] for val in top_industries]

    # industries = names of all top_industries
    industries = [val[0] for val in top_industries]
    
    # sum up all values in total_hash_vals
    total_hash_vals = np.sum(total_hash_vals)

    print(f"""total_hash_vals: {total_hash_vals}""")

    # score2 = is a list of all scores for each industry which is calculated by the formula
    # score2 = (value of industry hashtag/total_hash_vals)*10
    # in the final algorithm score 1 is added to this value and then divided by 2
    # this is done to make sure that the score is not too high

    score2 = []

    for val in top_industries:
        score2.append((((val[1]/total_hash_vals)*10)+score1)/2)

    # form a dict out of industries and score2
    final_scores_dict = {}

    for i in range(len(industries)):
        final_scores_dict[industries[i]] = score2[i]

    return final_scores_dict
