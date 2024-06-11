import pandas as pd
import requests
from io import StringIO

# get the cldf file
url = "https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/languages.csv"
response = requests.get(url)

#unicode should work
data = response.content.decode('utf-8')
df = pd.read_csv(StringIO(data))


#NB FOR YONGGOM: it is in WALS under Kati, there are TWO Kati languages
#have to pass the exact string "Kati (in West Papua, Indonesia)"


languages = ["English", "Chickasaw", "Kati (in West Papua, Indonesia)", "Norwegian", "Basque", "Blackfoot", "Luiseño", "Wambaya", "Dyirbal"]
language_codes = { #NB THESE ARE THE WALS LANGUAGE CODES NOT ISO-639!!
        "English": "eng",
        "Chickasaw": "cck", 
        "Kati (in West Papua, Indonesia)": "kti", #yonggom is in wals under Kati
        "Norwegian": 'nor',
        "Basque": 'bsq',
        "Blackfoot": 'bla',
        "Luiseño": 'lui',
        "Wambaya": 'wam',
        "Dyirbal": 'dyi',
        #MADAK DOES NOT HAVE A WALS DESIGNATION
        }

filtered_df = df[df['ID'].isin(language_codes.values())]

# get feature values 
features_url = "https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/values.csv"
features_response = requests.get(features_url)
features_data = features_response.content.decode('utf-8')
features_df = pd.read_csv(StringIO(features_data))
merged_df = pd.merge(filtered_df, features_df, left_on='ID', right_on='Language_ID')

#get features per  language
pivot_df = merged_df.pivot_table(index='Parameter_ID', columns='Name', values='Value')


# count diffs w/ english (just summing up the number of unequal entries?? sus but works??)
english_features = pivot_df['English']
diff_tracker = []

for language in languages:
    if language != "English":
        diffcount = (pivot_df[language] != english_features).sum()
        diff_tracker.append({"Language": language, "# of differing features": diffcount})

#chuck everything into a dataframe to check whether this stuff works 
comparison_df = pd.DataFrame(diff_tracker).sort_values(by="# of differing features")

pivot_df.to_csv('all_features.csv')
comparison_df.to_csv('diff_features_count.csv', index=False)


