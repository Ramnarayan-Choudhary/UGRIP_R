#!/usr/bin/env python
# coding: utf-8

import json
import re

from metrics import bleu_score, chrfplus_score, cter_score, em_score
from util import split_bidirectional, is_directional


##############################
####### Preprocessing ########
##############################

def remove_punctuation(sent):
    """
    Remove fullstops (.), exclamation marks (!), question marks (?), and commas (,) from a sentence
    :param sent: ground truth or submission sentence that may include punctuation
    :return: ground truth or submission sentence without punctuation
    """
    return re.sub(r"[.!?,]","",sent)

def replace_brackets(sent):
    """
    Replace brackets "[word]" with "(word/ )" in the sentence
    :param sent: ground truth or submission sentence that may include brackets
    :return: ground truth or submission sentence without brackets
    """
    return re.sub("\[([^]]+)\]", '(\\1/ )', sent)

def get_alternatives(gt_sent, alternatives):
    """
    Get all valid alternative writings of a ground truth sentence (recursive function)
    :param gt_sent: ground truth sentence
    :param alternatives: empty list to start recursive loop
    :return: list of all valid alternative writings of gt_sent
    """
    alternatives.append(gt_sent)
    if (len(re.findall(r"\([^\)\r\n]+\/[^\)\r\n]+\)", gt_sent)) > 0):
        # get first parenthesis
        parenthesis = re.findall(r"\([^\)\r\n]+\/[^\)\r\n]+\)", gt_sent)[0]
        # get all options provided within the parenthesis
        options = [i.strip() for i in parenthesis[1:-1].split("/")]
        # recursively loop through each option
        for o in options:
            get_alternatives(gt_sent.replace(parenthesis, o), alternatives)
    #else:
    #    return alternatives
    return alternatives

def remove_pronoun_tags(sent):
    """
    Remove pronoun tags (i.e. .SG/.PL/.PL2/.PL3) from a sentence
    :param sent: ground truth or submission sentence that may include pronoun tags
    :return: ground truth or submission sentence without pronoun tags
    """
    # list of pronoun tags
    tags = [".SG", ".PL2-", ".PL2", ".PL3", ".PL"]

    # remove the tags
    for t in tags:
        sent = sent.replace(t, "")
    return sent

##########################
######  Evaluation   #####
##########################

def evaluate_puzzle(ground_truth, submission):
    """
    Preprocess the sentences, then calculate the scores
    :param ground_truth:
    :param submission:
    :return:
    """
    bleu_scores = []
    chrfpp_scores = []
    cter_scores = []
    em_scores = []

    # print(f'>>>> Working with language: {ground_truth["source_language"]}   >>>> ')
    # print(f'>>>> First problem is {ground_truth["train"][0]}   >>>> ')
    try:
        for i in range(len(ground_truth["test"])):


            # print(ground_truth["test"][i][0].strip())
            # print('-----------------------------------')
            # print(submission["test"][i][0].strip())
            # print(f'-------------Translation # {i} ----------------------')
                  
            assert (ground_truth["test"][i][0].strip() == submission["test"][i][0].strip()), "PLEASE KEEP THE ORDER OF SUBMISSION SENTENCES INTACT"

          
            gt_sent = ground_truth["test"][i][1]
            sub_sent = submission["test"][i][1]

            ref = gt_sent.strip()
            sub = sub_sent.strip()

            ref = remove_pronoun_tags(replace_brackets(ref))
            sub = remove_pronoun_tags(replace_brackets(sub))
            ref = ref.lower()
            sub = sub.lower()
            ref = remove_punctuation(ref)
            sub = remove_punctuation(sub)

            # create alternative translations from the reference text (he/she) -> (he/she), he or she
            gt_sent_lst = get_alternatives(ref, [])
            sub_sent_lst = get_alternatives(sub, [])

            max_bleu = 0.
            max_chrf = 0.
            max_cter = 0.
            max_em = 0.

            for sub in sub_sent_lst:
                bs = bleu_score(gt_sent_lst, sub)
                if bs > max_bleu:
                    max_bleu = bs
                chrf = chrfplus_score(gt_sent_lst, sub)
                if chrf > max_chrf:
                    max_chrf = chrf
                cter = cter_score(gt_sent_lst, sub)
                if cter > max_cter:
                    max_cter = cter
                em = em_score(gt_sent_lst, sub)
                if em > max_em:
                    max_em = em

            bleu_scores.append(max_bleu)
            chrfpp_scores.append(max_chrf)
            cter_scores.append(max_cter)
            em_scores.append(max_em)

    except Exception as e:
        raise ValueError(repr(e))

    return {
        "bleu": bleu_scores,
        "chrf": chrfpp_scores,
        "cter": cter_scores,
        "em": em_scores
    }

def evaluate_unidirectional(ground_truth, submission):
    return evaluate_puzzle(ground_truth, submission)

def evaluate_directional(ground_truth, submission):
    """
    Evaluates and returns the scores for one puzzle.
    Direction is fixed, ltr = always foreign -> English and vice versa
    :param ground_truth: reference puzzle
    :param submission: submitted puzzle
    :return: scores for english->foreign, foreign->english and all
    """
    # ltr: puzzle that contains source to target test questions; rtl: puzzle that contains target to source test pairs
    #                                                               : other info reversed too

    gt_ltr, gt_rtl = split_bidirectional(ground_truth)
    pred_ltr, pred_rtl = split_bidirectional(submission)
    assert (gt_ltr is None) == (pred_ltr is None), "PLEASE KEEP TRANSLATION DIRECTIONS INTACT!"
    assert (gt_rtl is None) == (pred_rtl is None), "PLEASE KEEP TRANSLATION DIRECTIONS INTACT!"

    have_ltr = (gt_ltr is not None)
    have_rtl = (gt_rtl is not None)

    if have_ltr:
        # Evaluate source -> target
        ltr_eval = evaluate_puzzle(gt_ltr, pred_ltr)
    else:
        ltr_eval = {"bleu": [], "chrf": [], "cter": [], "em": []}
    if have_rtl:
        # Evaluate target -> source
        rtl_eval = evaluate_puzzle(gt_rtl, pred_rtl)
    else:
        rtl_eval = {"bleu": [], "chrf": [], "cter": [], "em": []}

    return (rtl_eval, ltr_eval)

def evaluate_file(gt_file, submission_file):
    """
    Evaluate one file
    :param gt_file:
    :param submission_file:
    :return:
    """
    with open(gt_file, encoding='utf-8') as file:
        ground_truth = json.load(file)
    try:
        with open(submission_file, encoding='utf-8') as file:
            submission = json.load(file)

    except Exception:
        print(f"ERROR: {submission_file} missing.")
        raise ValueError(f"ERROR: {submission_file} missing.")

    gt_directional = is_directional(ground_truth)
    assert is_directional(submission) == gt_directional, "PLEASE KEEP TRANSLATION DIRECTIONS INTACT!"

    if gt_directional:
        return evaluate_directional(ground_truth, submission)
    else:
        return evaluate_unidirectional(ground_truth, submission)


