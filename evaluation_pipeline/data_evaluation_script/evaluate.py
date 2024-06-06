# coding: utf-8

# Scoring program for the PuzzLing Machines shared task
# Written collaboratively by Gözde Gül Sahin, Liane Vogel, Marc-Simon Uecker and Philip Rust, April-2020

import json
import numpy as np
import os
import sys
import glob
from eval_submission_file import evaluate_file
from util import add_dict_to_dict


def check_format(data_folder):
    global_raise = False
    for puzzle_json in os.listdir(data_folder):

        filename = os.path.join(data_folder, puzzle_json)
        with open(filename, "r", encoding="utf8") as file:
            do_raise = False
            try:
                puzzle_data = json.load(file)
            except ValueError as e:
                do_raise = True
                global_raise = True
            if do_raise:
                print(f"ERROR: INVALID JSON FORMAT IN FILE:{filename}")
                continue

        for key in ["source_language", "target_language", "train", "test"]:
            try:
                puzzle_data[key]
            except KeyError as e:
                global_raise = True
                print(f"ERROR: MISSING FIELD '{key}' IN FILE: {filename}")
        for sent in puzzle_data["train"]:
            if len(sent) != 2:
                print(f"ERROR: WRONG TRAIN SENTENCE FORMAT IN FILE: {filename}")
                do_raise = True

        for sent in puzzle_data["test"]:
            if len(sent) != 2 and len(sent) != 3:
                print(f"ERROR: WRONG TEST SENTENCE FORMAT IN FILE: {filename}")
                do_raise = True

    if global_raise:
        raise ValueError("INVALID FORMATTING EXISTS.\nPLEASE CHECK THE SCORING OUTPUT LOG.")

def get_mean_scores(all_scores_dict):
    """
    Get the average for all keys in the dictionary
    :param all_scores_dict:
    :return: mean_s
    """
    mean_s = {"bleu": [], "chrf": [], "cter": [], "em": []}

    for k in all_scores_dict:
        mean_s[k] = np.mean(all_scores_dict[k])

    return mean_s

def get_scores(submission_path, solution_path):
    """
    Get the average of all scores
    :param submission_path:
    :param solution_path:
    :return:
    """
    target_files = glob.glob(f"{solution_path}/*.json")
    # source_files = [x.replace(solution_path, submission_path) for x in target_files]
    source_files = glob.glob(f"{submission_path}/*.json")

    # english -> foreign results from all submissions
    all_ef = {"bleu": [], "chrf": [], "cter": [], "em": []}

    # english -> foreign results from all submissions
    all_fe = {"bleu": [], "chrf": [], "cter": [], "em": []}

    # combined
    all = {"bleu": [], "chrf": [], "cter": [], "em": []}

    for f1, f2 in zip(target_files, source_files):
        (ef, fe) = evaluate_file(f1, f2)
        add_dict_to_dict(ef, all_ef)
        add_dict_to_dict(fe, all_fe)

    # get all in one
    add_dict_to_dict(all_ef, all)
    add_dict_to_dict(all_fe, all)

    print("Number of translations in total:", len(all["em"]))
    print("Number of English -> Foreign translations:", len(all_ef["em"]))
    print("Number of Foreign -> English translations:", len(all_fe["em"]))

    mean_ef = get_mean_scores(all_ef)
    mean_fe = get_mean_scores(all_fe)
    mean_all = get_mean_scores(all)

    return (mean_ef, mean_fe, mean_all)


submission_dir=sys.argv[1]+"/res"
ground_truth_dir=sys.argv[1]+"/ref"
output_path=sys.argv[2]

check_format(submission_dir)

submission_dirname = os.path.normpath(submission_dir)
ground_truth_dirname=os.path.normpath(ground_truth_dir)

# get scores
(mean_ef, mean_fe, mean_all) = get_scores(submission_dirname, ground_truth_dirname)

with open(output_path+"/scores.txt","w") as file:
    # e->f
    for k, v in mean_ef.items():
        m_name = "EF_"+k.upper()+"_SCORE"
        v *= 100
        file.write(f"{m_name}: {v:.2f}\n")
        print(m_name+" : "+str(v))


    # f->e
    for k, v in mean_fe.items():
        m_name = "FE_"+k.upper()+"_SCORE"
        v *= 100
        file.write(f"{m_name}: {v:.2f}\n")
        print(m_name + " : " + str(v))


    # total
    for k, v in mean_all.items():
        m_name = k.upper() + "_SCORE"
        v *= 100
        file.write(f"{m_name}: {v:.2f}\n")
        print(m_name + " : " + str(v))


print("Evaluation Completed")

