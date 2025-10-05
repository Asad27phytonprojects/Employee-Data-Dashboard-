# Employee Data Dashboard 📊

A dynamic and interactive dashboard built with **Streamlit**, **Pandas**, and **Matplotlib** to visualize and explore employee data.  
Upload your Excel or CSV file and get insights such as average salary per department, experience level distribution, age histogram, and salary vs performance analysis.

---

## Features

- Upload CSV or Excel files for employee data.
- Automatic detection of key columns: Salary, Department, Age, Experience, Performance.
- Data cleaning:
  - Fills missing salaries with the average
  - Fills missing departments with "Unknown"
  - Removes duplicate rows
- Bonus calculation (10% of salary)
- Experience level classification: Junior, Mid, Senior
- Interactive sidebar filters:
  - Filter by Department
  - Filter by Experience Level
- Visualizations:
  - **Bar Chart:** Average Salary per Department
  - **Pie Chart:** Experience Level Distribution
  - **Histogram:** Age Distribution
  - **Scatter Plot:** Salary vs Performance

---

## Requirements

### Python
- Python 3.8+
- Pip (Python package installer)
- Required Python libraries:

```bash
pip install streamlit pandas matplotlib openpyxl
