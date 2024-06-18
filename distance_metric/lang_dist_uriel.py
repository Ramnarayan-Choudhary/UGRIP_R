import lang2vec.lang2vec as l2v
import langcodes

import pandas as pd
import numpy as np



# # get the cldf file
# url = "https://raw.githubusercontent.com/cldf-datasets/wals/master/cldf/languages.csv"
# response = requests.get(url)

# #unicode should work
# data = response.content.decode('utf-8')
# df = pd.read_csv(StringIO(data))


#NB FOR YONGGOM: it is in WALS under Kati, there are TWO Kati languages
#have to pass the exact string "Kati (in West Papua, Indonesia)"


languages = ["English", "Chickasaw", "Kati (in West Papua, Indonesia)", "Norwegian", "Basque", "Blackfoot", "Luiseño", "Wambaya", "Dyirbal"]
language_codes_wals = { #NB THESE ARE THE WALS LANGUAGE CODES NOT ISO-639!!
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


#new code time

# print(l2v.available_feature_sets())

def euclidean_distance(vec1, vec2):
    vec1 = np.array([float(x) if x != '--' else np.nan for x in vec1], dtype=float)
    vec2 = np.array([float(x) if x != '--' else np.nan for x in vec2], dtype=float)
    #ignores nan dimensions
    mask = ~np.isnan(vec1) & ~np.isnan(vec2)
    if not np.any(mask): #yonggom causing problems
        return None
    #only non-nanned dims
    vec1_masked = vec1[mask]
    vec2_masked = vec2[mask]
    return np.linalg.norm(vec1_masked - vec2_masked)

#THIS IS JUST PUZZLING TRAIN
language_codes_iso = { 
        "English": "eng",
        "Chickasaw": "cic", 
        "Kati (in West Papua, Indonesia)": "kts", #yonggom is in wals/iso under Kati
        "Norwegian": 'nor',
        "Basque": 'eus',
        "Blackfoot": 'bla',
        "Luiseño": 'lui',
        "Wambaya": 'wmb',
        "Dyirbal": 'dbl',}


with open('puzzling_test_langs.txt', 'r') as file:
    languages = [line.strip() for line in file.readlines()]


def get_iso_codes(language_names):
    language_codes = {}
    for name in language_names:
        try:
            # Use langcodes to get the ISO-639 code
            language = langcodes.find(name)
            iso_code = language.language
            iso_3char = langcodes.Language.get(iso_code).to_alpha3()
            language_codes[name] = iso_3char
        except Exception as e:
            language_codes[name] = None
    
    return language_codes


def filter_valid_languages(language_codes):
    return {name: code for name, code in language_codes.items() if code is not None}

language_codes_iso_all = get_iso_codes(languages)

language_codes_iso_filtered = filter_valid_languages(language_codes_iso_all)

print(language_codes_iso_filtered)


dists_test = []

vector_eng = l2v.get_features('eng', 'syntax_average')
eng_features = vector_eng['eng']



for k, v in language_codes_iso_filtered.items():
    try:
        vector_lang = l2v.get_features(v, 'syntax_average')
    except Exception as e:
        continue
    lang_features = vector_lang[v]
    dist = euclidean_distance(eng_features, lang_features)
    dists_test.append({"Language": k, "# of differing features": dist})
    
comparison_df = pd.DataFrame(dists_test).sort_values(by="# of differing features")

print(comparison_df)

comparison_df.to_csv('uriel_dists_all.csv', index=False)





