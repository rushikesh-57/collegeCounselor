import pandas as pd
import os

output_excel_path = 'C:/Work/College Counselor/Cutoff/Cap Cutoff Average.xlsx'

def extract_before_newline(value):
    if isinstance(value, str):
        return value.split('\n')[0]
    return value

def read_and_join_excels(folder_path, join_column):
    # Initialize the base DataFrame as None
    combined_df = None
    defaultCols = ['College Code', 'College Name', 'Status', 'Home University', 'Branch Name', 'Admission Type']

    # Loop through each file in the folder
    fileList = os.listdir(folder_path)
    fileList.reverse()

    for filename in fileList:
        print(filename)
        if filename.endswith('.xlsx') or filename.endswith('.xls'):
            file_path = os.path.join(folder_path, filename)
            # Read the Excel file into a DataFrame
            df = pd.read_excel(file_path)
            allCols = list(df.columns)
            allCols.remove('Branch Code')
            rankCols = [x for x in allCols if x not in defaultCols]
            df_filtered_split = df.map(extract_before_newline)
            df_filtered_split = df_filtered_split.fillna('0')
            # defaultCols.remove('Branch Code')
            df_filtered_split[rankCols] = df_filtered_split[rankCols].apply(pd.to_numeric)
            agrs = {x: 'first' if x in defaultCols else 'max' for x in allCols}
            grouped_df = df_filtered_split.groupby('Branch Code').agg(agrs)
            grouped_df = grouped_df.reset_index()
            grouped_df['Branch Code'] = grouped_df['Branch Code'].str.lstrip('0')
            # If it's the first file, initialize combined_df
            if combined_df is None:
                combined_df = grouped_df
            else:
                # Join the current DataFrame with the combined DataFrame on the join_column
                combined_df = pd.merge(
                    combined_df,
                    grouped_df,
                    on=join_column,
                    how='left',
                    suffixes=('', '_new'),
                )

                # Merge overlapping numeric columns by averaging
                for column in combined_df.columns:
                    if column.endswith('_new'):
                        original_col = column.replace('_new', '')
                        if original_col in combined_df.columns and original_col in rankCols:
                            # Average the original and new column
                            combined_df[original_col] = combined_df[[original_col, column]].mean(axis=1)
                            # Drop the "_new" column after averaging
                            combined_df.drop(columns=[column], inplace=True)
                        else:
                            combined_df.drop(columns=[column], inplace=True)
    
    return combined_df

# Example usage
folder_path = 'C:/Work/College Counselor/CutoffToExcel'  # Replace with the path to your folder
join_column = 'Branch Code'
# combined_data = read_and_join_excels(folder_path, join_column)
# combined_data.to_excel(output_excel_path, index=False)
# print(combined_data)

import sqlite3
folder_path = 'C:/Work/College Counselor/Cutoff'
tableList = ['Cap1_cutoff_2024_Rank','Cap1_cutoff_2023_Rank','Cap1_cutoff_2022_Rank','Cap1_cutoff_2021_Rank','Cap1_cutoff_2020_Rank']
dfs = {}
conn = sqlite3.connect("data.db")
c = 2024
for tbl in tableList:
    tbl_query = f"SELECT College_Code, College_Name, Branch_Code, Branch_Name FROM {tbl};"
    df = pd.read_sql(tbl_query, conn)
    dfs[c] = df
    c -= 1

# Convert into a single DataFrame with a Year column
for year, df in dfs.items():
    df['Year'] = year

merged_df = pd.concat(dfs.values(), ignore_index=True)

# Find unique combinations of College_Code, Branch_Code over the years
grouped = merged_df.groupby(['College_Code', 'College_Name', 'Branch_Code', 'Branch_Name'])['Year'].agg(['min', 'max']).reset_index()
grouped.to_csv('C:/Work/College Counselor/Cutoff/combined.csv', index=False)

# **1️⃣ Identify New Colleges and Branches added**
new_entries = grouped[grouped['min'] == grouped['max'].max()]
new_entries.to_csv('C:/Work/College Counselor/Cutoff/new_entries.csv', index=False)

# **2️⃣ Identify College Code or Branch Code changes**
college_changes = merged_df.groupby('College_Name')['College_Code'].nunique().reset_index()
college_changes = college_changes[college_changes['College_Code'] > 1]  # College codes changed over years
college_changes.to_csv('C:/Work/College Counselor/Cutoff/college_changes.csv', index=False)

branch_changes = merged_df.groupby(['College_Name', 'Branch_Name'])['Branch_Code'].nunique().reset_index()
branch_changes = branch_changes[branch_changes['Branch_Code'] > 1]  # Branch codes changed over years
branch_changes.to_csv('C:/Work/College Counselor/Cutoff/branch_changes.csv', index=False)

# **Print Results**
print("🔹 New Colleges/Branches Added in Recent Years:")
print(new_entries)

print("\n🔹 College Code Changes Over Years:")
print(college_changes)

print("\n🔹 Branch Code Changes Over Years:")
print(branch_changes)
conn.close()
