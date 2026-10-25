# Relationships between numbers.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])
sns.set_theme(style="darkgrid")

# %% Scatter with extra dimensions
sns.scatterplot(data=emp, x="age", y="salary")
plt.show()

sns.scatterplot(data=emp, x="age", y="salary", hue="department", size="performance_score", style="gender")
plt.show()

# %% Line plot (draws average and confidence band when x repeats)
long = monthly.melt(id_vars="month", value_vars=["electronics", "clothing", "furniture"],
                    var_name="category", value_name="sales")
sns.lineplot(data=long, x="month", y="sales", hue="category", marker="o")
plt.xticks(rotation=30)
plt.show()

emp["join_year"] = emp["join_date"].dt.year
sns.lineplot(data=emp, x="join_year", y="salary", errorbar="sd")
plt.show()

# %% Regression line
sns.regplot(data=emp, x="age", y="salary")
plt.show()

sns.regplot(data=emp, x="age", y="salary", order=2)                # curve
plt.show()

sns.lmplot(data=emp, x="age", y="salary", hue="gender")
plt.show()

sns.lmplot(data=emp, x="age", y="salary", col="department", col_wrap=3, height=3)
plt.show()

# %% Check regression errors
sns.residplot(data=emp, x="age", y="salary")
plt.show()

# %% relplot: scatter or line in panels
sns.relplot(data=emp, x="age", y="salary", col="department", col_wrap=3, hue="gender", height=3)
plt.show()
