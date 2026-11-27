import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(
    "data/raw/General_Building_Permits_20261121.csv",
    low_memory=False
)

home = df[df["JOB_CATEGORY"] == "Home Improvement"]

renovations = home[
    home["JOB_DESCRIPTION"].str.contains(
        "renovat|alterat|remodel",
        case=False,
        na=False
    )
]

recent = renovations[renovations["YEAR"].between(2023, 2025)]

selected = recent[
    recent["NEIGHBOURHOOD"].isin(["LAUREL", "CHAPPELLE"])
]

yearly = selected.groupby(
    ["YEAR", "NEIGHBOURHOOD"]
).size().unstack(fill_value=0)

print(yearly)
percentage_change = yearly.pct_change() * 100

print("\nYear-over-Year Percentage Change (%):")
print(percentage_change.round(1))


percentage_change.round(1).to_csv("data/yearly_percentage_change.csv")

plt.figure(figsize=(10, 6))

plt.plot(
    yearly.index,
    yearly["LAUREL"],
    marker="o",
    label="Laurel"
)

plt.plot(
    yearly.index,
    yearly["CHAPPELLE"],
    marker="o",
    label="Chappelle"
)

plt.title("Renovation-Related Permit Trends (2023-2025)")
plt.xlabel("Year")
plt.ylabel("Number of Permit Records")

plt.xticks(yearly.index)
plt.legend()
plt.grid(axis="y", alpha=0.3)
plt.ylim(bottom=0)

plt.tight_layout()

plt.savefig(
    "figures/laurel_chappelle_yearly_trends.png",
    dpi=300,
    bbox_inches="tight"
)

plt.show()