# Relationships between numbers.
# Each line has a short comment saying WHAT the function is.
# Common arguments: data = the table, x / y = column names for the axes, hue = colour by this column.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

# Path("data").exists(): True if that folder exists; otherwise use ../data.
DATA = Path("data") if Path("data").exists() else Path("../data")
# pd.read_csv(file): loads a CSV into a table. parse_dates=[col]: reads that column as dates.
emp = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])
monthly = pd.read_csv(DATA / "04_monthly_sales.csv", parse_dates=["month"])
# sns.set_theme(style="darkgrid"): grey background with white grid lines for all charts.
sns.set_theme(style="darkgrid")

# ==============================================================
# SECTION 1: MUST KNOW  (use these every day, learn these well)
# ==============================================================

# %% Scatter with extra dimensions
# sns.scatterplot(data, x, y): one dot per row.
sns.scatterplot(data=emp, x="age", y="salary")
# plt.show(): displays the chart.
plt.show()

# hue = dot colour by department. size = dot size by performance. style = dot shape by gender.
sns.scatterplot(data=emp, x="age", y="salary", hue="department", size="performance_score", style="gender")
plt.show()

# %% Line plot (draws average and confidence band when x repeats)
# .melt(...): turns wide columns into long rows (month, category, sales).
# id_vars: column kept as is. value_vars: columns to stack. var_name / value_name: new column names.
long = monthly.melt(id_vars="month", value_vars=["electronics", "clothing", "furniture"],
                    var_name="category", value_name="sales")
# sns.lineplot(data, x, y): line chart; hue="category" = one line per category.
# marker="o": a circle on each point.
sns.lineplot(data=long, x="month", y="sales", hue="category", marker="o")
# plt.xticks(rotation=30): tilts the x labels by 30 degrees.
plt.xticks(rotation=30)
plt.show()

# .dt.year: year taken from a date column.
emp["join_year"] = emp["join_date"].dt.year
# errorbar="sd": the shaded band shows standard deviation (spread of salaries) for each year.
sns.lineplot(data=emp, x="join_year", y="salary", errorbar="sd")
plt.show()

# %% Regression line
# sns.regplot(data, x, y): dots plus a best-fit straight line with a light band for uncertainty.
sns.regplot(data=emp, x="age", y="salary")
plt.show()

# order=2: fits a curved (squared) line instead of a straight one.
sns.regplot(data=emp, x="age", y="salary", order=2)                # curve
plt.show()

# sns.lmplot: like regplot but can split by hue/col; makes its own figure. hue="gender": one line per gender.
sns.lmplot(data=emp, x="age", y="salary", hue="gender")
plt.show()

# col="department": one panel per department. col_wrap=3: 3 panels per row. height=3: panel height.
sns.lmplot(data=emp, x="age", y="salary", col="department", col_wrap=3, height=3)
plt.show()

# ==============================================================
# !SECTION 2: GOOD TO KNOW  (rarely used, just know they exist)
# ==============================================================

# %% Check regression errors
# sns.residplot: dots show how far each real value is from the trend line (good fit = random around 0).
sns.residplot(data=emp, x="age", y="salary")
plt.show()

# %% relplot: scatter or line in panels
# sns.relplot(...): scatter (default) or line chart that can split into panels.
sns.relplot(data=emp, x="age", y="salary", col="department", col_wrap=3, hue="gender", height=3)
plt.show()
