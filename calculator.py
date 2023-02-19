import json
import matplotlib.pyplot as plt
import regex as re

data = json.load(open('jonasroeber.json'))
post = data["posts"]
keys = post.keys()
print(post["22,3"])
# for key in keys:
#     number_of_likes = re.search(r"mit \d+ likes", post[key])
#     reach = re.sub(r"(?i)[a-z]", "", number_of_likes.group(0))
#     print(f"""{key}:{reach}""")
    