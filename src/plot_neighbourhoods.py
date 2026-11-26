import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/raw/General_Building_Permits_20261121.csv")

home = df[df["JOB_CATEGORY"] == "Home Improvement"]

renovations = home[
    home["JOB_DESCRIPTION"].str.contains(
        "renovat|alterat|remodel",
        case=False,
        na=False
    )
]

recent = renovations[renovations["YEAR"].between(2023, 2025)]

top10 = recent["NEIGHBOURHOOD"].value_counts().head(10)

top10 = top10.sort_values()

plt.figure(figsize=(12, 6))

plt.barh(top10.index, top10.values)

plt.title("Top 10 Edmonton Neighbourhoods (2023-2025)")
plt.xlabel("Number of Renovation-Related Permits")
plt.ylabel("Neighbourhood")

plt.tight_layout()
plt.savefig("figures/top10_neighbourhoods.png", dpi=300, bbox_inches="tight")
plt.show()
