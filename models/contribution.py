def year1_contribution(snaps, scheme_fit, nil_bucket):
    cost_map = {"Low": 1, "Mid": 2, "High": 3}
    return (snaps * 0.6 + scheme_fit * 200) / cost_map[nil_bucket]

