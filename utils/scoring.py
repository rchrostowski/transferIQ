from models.contribution import year1_contribution

def total_score(row):
    return year1_contribution(
        row["expected_snaps"],
        row["scheme_match"],
        row["nil_bucket"]
    )

