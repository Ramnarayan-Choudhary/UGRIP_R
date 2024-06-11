import pandas as pd

def ranking(rankings, all_probs):
    """
    calculate the average ranking as (sum of ranks by everybody)/number of people.
    return sorted list by average ranking. 
    takes an input list of lists, where each list is someone's hardness ranking, sorted easy-hard. 

    """
    rank_sums = {prob: 0 for prob in all_probs}
    rank_counts = {prob: 0 for prob in all_probs}
    
    #get everyone's individual problem ranking
    for each_ranking in rankings:
        current = 1
        for prob in each_ranking:
            rank_sums[prob] += current
            rank_counts[prob] += 1
            current += 1

    avg_ranking = {prob: (rank_sums[prob] / rank_counts[prob]) if rank_counts[prob] > 0 else float('inf') for prob in rank_sums}

    #sort by overall rank (easy = rank 1, hard = rank 10)
    final_ranks = sorted(avg_ranking.keys(), key = lambda prob: avg_ranking[prob])
    return final_ranks


hanif_ranks = ['Euskara', 'Norwegian', 'Blackfoot', 'Madak', 'Yonggom']
joy_ranks = ['Luiseno', 'Blackfoot', 'Basque', 'Wambaya', 'Dyirbal']
khoa_ranks = []
rc_ranks = []

#NB I think Lakoff makes Dyirbal significantly easier.......
antara_ranks_all = ['Chickasaw', 'Norwegian', 'Blackfoot', 'Euskara', 'Luiseno', 'Basque', 'Madak', 'Wambaya', 'Dyirbal', 'Yonggom']

rankings = [antara_ranks_all, hanif_ranks, joy_ranks, khoa_ranks, rc_ranks]


all_probs = ['Wambaya','Blackfoot', 'Basque', 'Madak', 'Chickasaw',  'Euskara',  'Dyirbal', 'Norwegian','Yonggom',  'Luiseno']
global_ranking = ranking(rankings, all_probs)
print(global_ranking)
