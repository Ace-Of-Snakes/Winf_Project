import instaloader

def get_industries(username):
    # define the categories and their corresponding hashtags
    categories = {
        "art": ["art", "painting", "drawing", "sketching"],
        "beauty": ["beauty", "skincare", "makeup", "cosmetics"],
        "books": ["books", "reading", "bookstagram", "booklover"],
        "business": ["business", "entrepreneur", "startup", "marketing"],
        "cooking": ["cooking", "food", "recipe", "baking"],
        "fashion": ["fashion", "style", "outfit", "clothing"],
        "fitness": ["fitness", "workout", "exercise", "training"],
        "gaming": ["gaming", "gamers", "videogames", "esports"],
        "health": ["health", "wellness", "mentalhealth", "selfcare"],
        "music": ["music", "guitar", "piano", "singing"],
        "photography": ["photography", "photooftheday", "landscape", "portrait"],
        "sports": ["sports", "football", "basketball", "soccer"],
        "travel": ["travel", "wanderlust", "adventure", "vacation"],
    }

    # create a dictionary to store the hashtags for each category
    hashtags = {category: [] for category in categories}

    # initialize instaloader
    L = instaloader.Instaloader()

    # load the user's profile
    profile = instaloader.Profile.from_username(L.context, username)

    # loop through the user's posts and extract hashtags
    for post in profile.get_posts():
        for hashtag in post.caption_hashtags:
            # check which category the hashtag belongs to
            for category, category_hashtags in categories.items():
                if any(keyword in hashtag.lower() for keyword in category_hashtags):
                    hashtags[category].append(hashtag)

    # sort the hashtags in each category by frequency count
    for category, category_hashtags in hashtags.items():
        hashtag_counts = {}
        for hashtag in category_hashtags:
            if hashtag in hashtag_counts:
                hashtag_counts[hashtag] += 1
            else:
                hashtag_counts[hashtag] = 1
        hashtags[category] = sorted(hashtag_counts.items(), key=lambda x: x[1], reverse=True)

    # print the top 5 most common hashtags in each category
    for category, category_hashtags in hashtags.items():
        print(f"Top 5 most common hashtags in {category}:")
        for hashtag, count in category_hashtags[:5]:
            print(f"{hashtag}: {count}")
        print()

    # determine the most common industries based on the hashtags
    industries = []
    for category, category_hashtags in hashtags.items():
        for hashtag, count in category_hashtags[:3]:
            industries.append(category)
    print(f"Most common industries: {', '.join(set(industries))}")

    # determine the most common industries based on the hashtags
    industry_counts = {}
    for category, category_hashtags in hashtags.items():
        for hashtag, count in category_hashtags[:3]:
            if category not in industry_counts:
                industry_counts[category] = count
            else:
                industry_counts[category] += count

    # sort the industries by frequency count
    top_industries = sorted(industry_counts.items(), key=lambda x: x[1], reverse=True)
    return top_industries

if __name__ == "__main__":
    industries = get_industries("jonasroeber")
    print(list(set(industries)))