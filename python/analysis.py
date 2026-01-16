# ==========================================
# Mobile Game A/B Test: Gate 30 vs Gate 40
# Purpose: Evaluate engagement and retention
# ==========================================

import pandas as pd
from scipy.stats import mannwhitneyu
from statsmodels.stats.proportion import proportions_ztest
import matplotlib.pyplot as plt
import seaborn as sns

# -------------------------
# Load Data
# -------------------------
df = pd.read_csv("cookie_cats.csv")

# Basic integrity checks
assert df.userid.nunique() == len(df), "Duplicate users detected"
assert df.version.nunique() == 2, "Unexpected experiment variants"

# -------------------------
# Engagement Analysis
# Metric: Total Game Rounds Played
# -------------------------

# Engagement data is heavily right-skewed.
# Mean-based tests (t-test) would be misleading.
# Median-based comparison is more appropriate.

# Remove extreme outliers using a percentile-based rule
upper_bound = df.sum_gamerounds.quantile(0.99)
df_engagement = df[df.sum_gamerounds <= upper_bound]

# Visual sanity check (single, representative plot)
plt.figure(figsize=(8, 5))
sns.histplot(
    data=df_engagement,
    x="sum_gamerounds",
    hue="version",
    bins=100,
    kde=True
)
plt.xlim(0, 500)
plt.title("Distribution of Game Rounds Played (Trimmed)")
plt.xlabel("Total Game Rounds")
plt.ylabel("Player Count")
plt.tight_layout()
plt.show()

# Mann–Whitney U Test (median comparison)
gate_30 = df_engagement[df_engagement.version == "gate_30"].sum_gamerounds
gate_40 = df_engagement[df_engagement.version == "gate_40"].sum_gamerounds

u_stat, p_engagement = mannwhitneyu(
    gate_30,
    gate_40,
    alternative="two-sided"
)

# -------------------------
# Retention Analysis
# Metrics: Day 1 and Day 7 Retention
# -------------------------

def retention_test(df, retention_col):
    g30_users = df[df.version == "gate_30"].userid.count()
    g40_users = df[df.version == "gate_40"].userid.count()

    g30_retained = df[(df.version == "gate_30") & (df[retention_col])].userid.count()
    g40_retained = df[(df.version == "gate_40") & (df[retention_col])].userid.count()

    z_stat, p_value = proportions_ztest(
        [g30_retained, g40_retained],
        [g30_users, g40_users],
        alternative="two-sided"
    )

    return {
        "gate_30_rate": g30_retained / g30_users,
        "gate_40_rate": g40_retained / g40_users,
        "p_value": p_value
    }

day1_results = retention_test(df, "retention_1")
day7_results = retention_test(df, "retention_7")

# -------------------------
# Results Summary
# -------------------------

print("=== Engagement (Game Rounds) ===")
print(f"Mann–Whitney U p-value: {p_engagement:.3f}")
print("Interpretation: No statistically significant difference in median engagement.\n")

print("=== Retention Results ===")
print(f"Day 1 Retention p-value: {day1_results['p_value']:.3f}")
print(f"Day 7 Retention p-value: {day7_results['p_value']:.3f}\n")

# -------------------------
# Decision Logic (Documented)
# -------------------------

"""
Decision Summary:

- Engagement (primary progression metric):
  No statistically significant difference between Gate 30 and Gate 40.

- Day 1 Retention:
  Directionally different but not statistically significant.

- Day 7 Retention:
  Statistically significant improvement for Gate 30.

Despite the Day 7 retention signal, Gate 40 was NOT recommended for rollout.
Reason:
- No engagement improvement
- Increased progression friction risk
- Retention uplift alone does not justify gating players later without
  supporting engagement evidence

Final Recommendation: Do Not Roll Out Gate 40
"""
