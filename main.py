from insta_scraper import main
from calculator import calculate_statistics
from industry_recognize import get_industries
from algorithm import scoring_algorithm
from city_evaluator import evaluate_city
import json

if __name__ == '__main__':
    profile = {}
    # some data to test the algorithm
    target_account = 'timo.wacke'
    city = 'Hamburg'

    #get profile data
    # main(target_account)
    
    #get city value in reach points
    city_val = evaluate_city(city)

    #get values from calculator
    emoji_sentiment, word_sentiment, like_engagement_ratios, comm_engagement_ratios = calculate_statistics(f"profiles/{target_account}.json")

    #get top industries and their values
    top_industries = get_industries(target_account)

    #get final scores for each industry
    final_scores_dict = scoring_algorithm(emoji_sentiment, word_sentiment,like_engagement_ratios,comm_engagement_ratios,top_industries,city_val)
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