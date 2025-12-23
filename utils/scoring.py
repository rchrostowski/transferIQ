import numpy as np

def fit_score(scheme_match):
    return scheme_match * 100

def cost_efficiency(expected_snaps, nil_bucket):
    cost_map = {"Low": 1, "Mid": 2, "High": 3}
    return expected_snaps / cost_map[nil_bucket]

