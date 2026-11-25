import pandas as pd

file_path = "data/raw/General_Building_Permits_20261121.csv"

df = pd.read_csv(file_path, low_memory=False)

print("Total permits:", len(df))

home = df[df["JOB_CATEGORY"] == "Home Improvement"]

print("Home Improvement permits:", len(home))

matches = home["JOB_DESCRIPTION"].str.contains(
    "renovat|alterat|remodel",
    case=False,
    na=False
)

renovations = home[matches]

print("Possible renovations:", len(renovations))

percentage = len(renovations) / len(home) * 100

print(f"Possible renovation percentage: {percentage:.1f}%")

interior = renovations["JOB_DESCRIPTION"].str.contains(
    "interior alterat", case=False, na=False
)

print("Possible interior alterations:", interior.sum())

exterior = renovations["JOB_DESCRIPTION"].str.contains("exterior alterat", case=False, na=False)

print("Possible exterior alterations:", exterior.sum())

print("Both interior and exterior:", (interior & exterior).sum())

print("Interior or exterior:", (interior | exterior).sum())

other = renovations[~(interior | exterior)]

print("Other renovation keywords:", len(other))

print("Renovation:", other["JOB_DESCRIPTION"].str.contains("renovat", case=False, na=False).sum())

print("Alteration:", other["JOB_DESCRIPTION"].str.contains("alterat", case=False, na=False).sum())

print("Remodeling:", other["JOB_DESCRIPTION"].str.contains("remodel", case=False, na=False).sum())

renovation_keyword = other["JOB_DESCRIPTION"].str.contains(
    "renovat", case=False, na=False
)

alteration_keyword = other["JOB_DESCRIPTION"].str.contains(
    "alterat", case=False, na=False
)

both_keywords = renovation_keyword & alteration_keyword

print("Both renovation and alteration keywords:", both_keywords.sum())

print("Interior mentions:", other["JOB_DESCRIPTION"].str.contains("interior", case=False, na=False).sum())

print("Exterior mentions:", other["JOB_DESCRIPTION"].str.contains("exterior", case=False, na=False).sum())


other_interior = other["JOB_DESCRIPTION"].str.contains(
    "interior", case=False, na=False
)

other_exterior = other["JOB_DESCRIPTION"].str.contains(
    "exterior", case=False, na=False
)

print("Interior or exterior mentions:",
      (other_interior | other_exterior).sum())

print("Neither interior nor exterior:",
      (~(other_interior | other_exterior)).sum())

remaining = other[~(other_interior | other_exterior)]

print("Remaining records:", len(remaining))

print(remaining["JOB_DESCRIPTION"].head(5).to_string(index=False))

print("Addition:", remaining["JOB_DESCRIPTION"].str.contains(
    "addition", case=False, na=False
).sum())

print("Deck:", remaining["JOB_DESCRIPTION"].str.contains(
    "deck", case=False, na=False
).sum())

print("Secondary Suite:", remaining["JOB_DESCRIPTION"].str.contains(
    "secondary suite", case=False, na=False
).sum())

print("Top 10 neighbourhoods:")

print(
    renovations["NEIGHBOURHOOD"]
    .value_counts()
    .head(10)
    .to_string()
)

print(
    "Missing neighbourhoods:",
    renovations["NEIGHBOURHOOD"].isna().sum()
)

print("Renovations by year:")

print(
    renovations["YEAR"]
    .value_counts()
    .sort_index()
    .to_string()
)


recent = renovations[renovations["YEAR"].between(2023, 2025)]

print("Recent renovation permits:", len(recent))

print("Top 10 neighbourhoods (2023-2025):")

print(
    recent["NEIGHBOURHOOD"]
    .value_counts()
    .head(10)
    .to_string()
)

chappelle = recent[recent["NEIGHBOURHOOD"] == "CHAPPELLE"]

print("Chappelle permits by year:")

print(chappelle.groupby("YEAR").size().to_string())

comparison = recent[
    recent["NEIGHBOURHOOD"].isin(["LAUREL", "CHAPPELLE"])
]

print("Combined permits:", len(comparison))

yearly_comparison = comparison.groupby(
    ["NEIGHBOURHOOD", "YEAR"]
).size().unstack(fill_value=0)

print("Neighbourhood comparison by year:")
print(yearly_comparison.to_string())

yearly_change = yearly_comparison.pct_change(axis=1) * 100

print("Yearly percentage change:")

print(yearly_change.round(1).to_string())
