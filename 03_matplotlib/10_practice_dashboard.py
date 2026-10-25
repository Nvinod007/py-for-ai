# Practice: one dashboard from the employee data.
# Try building each chart yourself first, then compare.

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

DATA = Path("data") if Path("data").exists() else Path("../data")
emp = pd.read_csv(DATA / "03_employees.csv", parse_dates=["join_date"])

# %% Dashboard
fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle("Company overview", fontsize=16, fontweight="bold")

# 1. headcount per department
counts = emp["department"].value_counts()
axes[0, 0].bar(counts.index, counts.values, color="tab:blue")
axes[0, 0].set_title("Headcount")
axes[0, 0].tick_params(axis="x", rotation=30)

# 2. salary distribution
axes[0, 1].hist(emp["salary"], bins=8, color="tab:green", edgecolor="white")
axes[0, 1].set_title("Salary distribution")

# 3. age vs salary
axes[0, 2].scatter(emp["age"], emp["salary"], c=emp["performance_score"], cmap="viridis")
axes[0, 2].set_title("Age vs salary (colour = performance)")

# 4. hires per year
hires = emp.groupby(emp["join_date"].dt.year).size()
axes[1, 0].plot(hires.index, hires.values, marker="o")
axes[1, 0].set_title("Hires per year")

# 5. salary spread per department
groups = [g["salary"] for _, g in emp.groupby("department")]
axes[1, 1].boxplot(groups, tick_labels=sorted(emp["department"].unique()))
axes[1, 1].set_title("Salary by department")
axes[1, 1].tick_params(axis="x", rotation=30)

# 6. remote share
remote = emp["remote"].value_counts()
axes[1, 2].pie(remote, labels=["Remote" if k else "Office" for k in remote.index], autopct="%1.0f%%")
axes[1, 2].set_title("Remote vs office")

fig.tight_layout()
plt.show()

# %% Your turn
# 1. Add a bar chart: average performance per department.
# 2. Draw a line chart of cumulative hires by year.
# 3. Show male vs female average salary per department as grouped bars.
