from insta_scraper import main
from calculator import calculate_statistics
from industry_recognize import get_industries
from algorithm import scoring_algorithm
import json

if __name__ == '__main__':
    profile = {}
    target_account = 'jonasroeber'
    # main(target_account)
    #get values from calculator
    emoji_sentiment, word_sentiment, like_engagement_ratios, comm_engagement_ratios = calculate_statistics(f"profiles/{target_account}.json")
    top_industries = get_industries(target_account)
    final_scores_dict = scoring_algorithm(emoji_sentiment, word_sentiment,like_engagement_ratios,comm_engagement_ratios,top_industries)
    print(final_scores_dict)

    # export all data as json file
    profile["emoji_sentiment"] = emoji_sentiment
    profile["word_sentiment"] = word_sentiment
    profile["like_engagement_ratios"] = like_engagement_ratios
    profile["comm_engagement_ratios"] = comm_engagement_ratios
    profile["top_industries"] = top_industries
    profile["final_scores_dict"] = final_scores_dict

    with open(f"profiles/{target_account}_scoring.json", "w") as outfile:
        json.dump(profile, outfile)