import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Employee Dashboard", layout="wide")
st.title("📊 Employee Data Dashboard")
st.write("Upload your Excel or CSV file to explore and visualize employee data!")

uploaded_file = st.file_uploader("Choose a file", type=["csv", "xlsx"])

if uploaded_file is not None:
    try:
        # --------- Load file ---------
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
        st.success("✅ File loaded successfully!")
        
        # --------- Detect columns dynamically ---------
        col_lower = [c.lower() for c in df.columns]
        col_map = {}
        for c in df.columns:
            c_l = c.lower()
            if "salary" in c_l:
                col_map['Salary'] = c
            elif "department" in c_l:
                col_map['Department'] = c
            elif "age" in c_l:
                col_map['Age'] = c
            elif "experience" in c_l:
                col_map['Experience'] = c
            elif "performance" in c_l:
                col_map['Performance'] = c
        
        # --------- Data Cleaning ---------
        if 'Salary' in col_map:
            df[col_map['Salary']] = df[col_map['Salary']].fillna(df[col_map['Salary']].mean())
        if 'Department' in col_map:
            df[col_map['Department']] = df[col_map['Department']].fillna("Unknown")
        df = df.drop_duplicates()
        
        # Add Bonus
        if 'Salary' in col_map:
            df['Bonus'] = df[col_map['Salary']] * 0.10
        
        # Experience Level
        if 'Experience' in col_map:
            def exp_level(years):
                if years < 2:
                    return 'Junior'
                elif years <= 4:
                    return 'Mid'
                else:
                    return 'Senior'
            df['Experience_Level'] = df[col_map['Experience']].apply(exp_level)
        
        # --------- Data Overview ---------
        st.subheader("🔍 Data Overview")
        st.write(f"**Rows:** {df.shape[0]}, **Columns:** {df.shape[1]}")
        st.write("**Columns:**", list(df.columns))
        st.write("### Missing Values Check")
        st.write(df.isnull().sum())
        if df.isnull().sum().sum() == 0:
            st.success("✅ No missing values!")
        else:
            st.warning("⚠️ Some missing values detected.")
        dup_count = df.duplicated().sum()
        if dup_count > 0:
            st.warning(f"⚠️ {dup_count} duplicate rows detected!")
        else:
            st.success("✅ No duplicate rows!")
        
        # --------- Unusual Patterns Check ---------
        st.subheader("🚨 Unusual Patterns")
        if 'Salary' in col_map:
            Q1 = df[col_map['Salary']].quantile(0.25)
            Q3 = df[col_map['Salary']].quantile(0.75)
            IQR = Q3 - Q1
            outliers = df[(df[col_map['Salary']] < Q1 - 1.5*IQR) | (df[col_map['Salary']] > Q3 + 1.5*IQR)]
            st.write(f"Salary outliers: {outliers.shape[0]} rows")
            if not outliers.empty:
                st.dataframe(outliers)
        
        # --------- Sidebar Filters ---------
        st.sidebar.header("Filter Options")
        if 'Department' in col_map:
            departments = df[col_map['Department']].unique().tolist()
            selected_departments = st.sidebar.multiselect("Select Departments", departments, default=departments)
        else:
            selected_departments = df.index
        if 'Experience_Level' in df.columns:
            exp_levels = df['Experience_Level'].unique().tolist()
            selected_exp = st.sidebar.multiselect("Select Experience Levels", exp_levels, default=exp_levels)
        else:
            selected_exp = df.index
        
        df_filtered = df
        if 'Department' in col_map:
            df_filtered = df_filtered[df_filtered[col_map['Department']].isin(selected_departments)]
        if 'Experience_Level' in df.columns:
            df_filtered = df_filtered[df_filtered['Experience_Level'].isin(selected_exp)]
        
        # --------- Visualizations ---------
        st.subheader("📊 Visualizations")
        
        # Bar Chart: Avg Salary per Dept
        if 'Salary' in col_map and 'Department' in col_map:
            st.write("### 💰 Average Salary per Department")
            salary_dept = df_filtered.groupby(col_map['Department'])[col_map['Salary']].mean().sort_values(ascending=False)
            fig, ax = plt.subplots(figsize=(8,5))
            bars = salary_dept.plot(kind='bar', ax=ax, color='#4CAF50', edgecolor='black')
            # Add value labels
            for i, value in enumerate(salary_dept.values):
                ax.text(i, value + 0.5, f'{value:.2f}', ha='center', va='bottom', fontsize=10)
            # Styling
            ax.set_ylabel("Average Salary", fontsize=12, fontweight='bold')
            ax.set_xlabel("Department", fontsize=12, fontweight='bold')
            ax.set_title("Average Salary by Department", fontsize=14, fontweight='bold', pad=15)
            ax.grid(axis='y', linestyle='--', alpha=0.7)
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            st.pyplot(fig)
        
        # Pie Chart: Experience Level
        if 'Experience_Level' in df_filtered.columns:
            st.write("### 🎯 Experience Level Distribution")
            exp_counts = df_filtered['Experience_Level'].value_counts()
            fig2, ax2 = plt.subplots(figsize=(5,5))
            exp_counts.plot(kind='pie', autopct='%1.1f%%', colors=['#FF9999','#66B2FF','#99FF99'], startangle=90, ax=ax2)
            ax2.set_ylabel("")
            ax2.set_title("Experience Level Distribution", fontsize=14)
            st.pyplot(fig2)
        
        # Histogram: Age Distribution
        if 'Age' in col_map:
            st.write("### 👤 Age Distribution")
            fig3, ax3 = plt.subplots(figsize=(8,4))
            df_filtered[col_map['Age']].plot(kind='hist', bins=6, color='#FFA500', edgecolor='black', ax=ax3)
            ax3.set_xlabel("Age", fontsize=12)
            ax3.set_ylabel("Count", fontsize=12)
            ax3.set_title("Age Distribution of Employees", fontsize=14)
            ax3.grid(axis='y', linestyle='--', alpha=0.7)
            st.pyplot(fig3)
        
        # Scatter: Salary vs Performance
        if 'Salary' in col_map and 'Performance' in col_map:
            st.write("### 📈 Salary vs Performance Rating")
            fig4, ax4 = plt.subplots(figsize=(8,5))
            ax4.scatter(df_filtered[col_map['Salary']], df_filtered[col_map['Performance']], color='#8A2BE2')
            ax4.set_xlabel("Salary", fontsize=12)
            ax4.set_ylabel("Performance Rating", fontsize=12)
            ax4.set_title("Salary vs Performance Rating", fontsize=14)
            ax4.grid(True, linestyle='--', alpha=0.5)
            st.pyplot(fig4)
        
    except Exception as e:
        st.error(f"❌ Error processing file: {e}")

else:
    st.info("👆 Please upload a file to get started.")
