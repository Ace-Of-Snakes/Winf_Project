import pandas as pd
import regex as re
def evaluate_city(city):
    df = pd.read_csv("ressources/List_of_cities_in_Germany_by_population_1.csv")
    for i in range(len(df)):
        if city in df["City"][i]:
            if int(re.sub(",","", df["2021 estimate"][i])) > 500000:
                return 0.3
    return 0.0