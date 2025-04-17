from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS
import json
import sqlite3

# universityList = list(set(df['Home University']))
# collegeList = list(set(df['College Name']))

# df_filtered = df.applymap(extract_before_newline)
# print(df_filtered[df_filtered['Branch Code'] == '0101261210'])
dd = {'Rank': '99', 'Gender': 'Male', 'Caste': 'Open', 'EWS': 'No', 'PWD': 'No', 'DEF': 'No', 'TFWS': 'No', 'ORPHAN': 'No', 'MI': 'No',
      'HomeUniversity': 'Savitribai Phule Pune University', 
      'PrefferedUniversity': ['Sant Gadge Baba Amravati University'],
      'PrefferedBranch': ['Computer Science and Technology']
    }

def extract_before_newline(value):
    if isinstance(value, str):
        return value.split('\n')[0]
    return value

def getDefaultColumns():
    return ['College_Code', 'College_Name', 'Status', 'Home_University', 'Branch_Code', 'Branch_Name', 'Admission_Type']

def getAutonomousUniversity():
    return ["Autonomous Institute", "SNDT Women's University", 'Dr. Babasaheb Ambedkar Technological University,Lonere', 'Deemed to be University']

def addCutOffColumn(row):
    cutoff = 0
    if row['Admission_Type'] == 'State Level':
        pass
    if row["Home_University"] == dd['HomeUniversity']:
        pass
    return True

def getDataFromExcel(path):
    df = pd.read_excel(path)
    return df

def filterAsPerPreference(data, conn):
    #Need to add clg filter
    sqlQuery = """SELECT 
                        b.branch_code,
                        b.branch_name,
                        c.college_name,
                        u.university_name,
                        byd.*
                    FROM Cap1_Cutoff_Agg_2025 byd
                    JOIN Branch b ON byd.branch_code = b.branch_code
                    JOIN College c ON b.college_code = c.college_code
                    JOIN University u ON c.university_id = u.university_id
                    WHERE 1 = 1 """
    
    if data['PrefferedDistrict']:
        sqlQuery = sqlQuery + f""" AND c.District IN ({', '.join(f"'{item}'" for item in data['PrefferedDistrict'])}) """
    if data['PrefferedBranch']:
        sqlQuery = sqlQuery + f""" AND b.branch_name IN ({', '.join(f"'{item}'" for item in data['PrefferedBranch'])}) """
    # if data['PrefferedCollege']:
    #     sqlQuery = sqlQuery + f" AND c.college_name IN {tuple(data['PrefferedCollege'])} "
    sqlQuery = sqlQuery + "ORDER BY byd.[2024] DESC;"

    print(sqlQuery)
    df = pd.read_sql(sqlQuery, conn)
    
    # if data['PrefferedUniversity']:
    #     filtered_df_University = df[df['Home_University'].isin(data['PrefferedUniversity'])]
    #     if data['PrefferedBranch']:
    #         filtered_df_University_Branch = filtered_df_University[filtered_df_University['Branch_Name'].isin(data['PrefferedBranch'])]
    #         return filtered_df_University_Branch
    #     else:
    #         return filtered_df_University
    # else:
    #     if data['PrefferedBranch']:
    #         filtered_df_Branch = df[df['Branch_Name'].isin(data['PrefferedBranch'])]
    #         return filtered_df_Branch
    return df

def filterAsPerHomeOtherState(df, data):
    universityList = getAutonomousUniversity()
    filtered_df_State = df[df['university_name'].isin(universityList)]
    filtered_df_Not_State = df[~df['university_name'].isin(universityList)]
    filtered_df_Home = filtered_df_Not_State[filtered_df_Not_State['university_name'] == data['HomeUniversity']]
    filtered_df_Other = filtered_df_Not_State[filtered_df_Not_State['university_name'] != data['HomeUniversity']]
    return filtered_df_State, filtered_df_Home, filtered_df_Other

def filterColumnsAsPerCasteGender(allCols, data):
    if data['Gender'] == 'Male':
        genderCols = [x for x in allCols if x[0]=='G']
    else:
        genderCols = [x for x in allCols if x[0]=='L']
    casteGenderCols = [x for x in genderCols if x.startswith(data['Caste'], 1)]
    return casteGenderCols

def filterColumnsAsPerPwdDef(allCols, data):
    castePwdDefCols = []
    if data['PWD'] == 'Yes':
        pwdCols = [x for x in allCols if x.startswith("PWD")]
        castePwdCols = [x for x in pwdCols if data['Caste'] in x]
        castePwdDefCols = castePwdDefCols + castePwdCols
    if data['DEF'] == 'Yes':
        defCols = [x for x in allCols if x.startswith("DEF")]
        casteDefCols = [x for x in defCols if data['Caste'] in x]
        castePwdDefCols = castePwdDefCols + casteDefCols
    return castePwdDefCols

def filterOtherColumns(data):
    cols = []
    if data['EWS'] == 'Yes':
        cols = cols + ['EWS']
    if data['TFWS'] == 'Yes':
        cols = cols + ['TFWS']
    if data['ORPHAN'] == 'Yes':
        cols = cols + ['ORPHAN']
    if data['MI'] == 'Yes':
        cols = cols + ['MI']
    return cols

def collegeSuggest(data):
    path = 'C:/Work/collegeCounselor/src/Cap 1 cutoff 24-25.xlsx'
    path = 'C:/Work/College Counselor/Cutoff/Cap Cutoff Average.xlsx'
    defaultCols = getDefaultColumns()
    df = pd.read_excel(path)
    allCols = list(df.columns)
    filtered_df_University_Branch = filterAsPerPreference(df, data)

    
    casteGenderCols = filterColumnsAsPerCasteGender(allCols, data)
    castePwdDefCols = filterColumnsAsPerPwdDef(allCols, data)
    otherCols = filterOtherColumns(data)
    rankCols = casteGenderCols + castePwdDefCols + otherCols
    filteredCols = defaultCols + rankCols
    dfFiltered = filtered_df_University_Branch[filteredCols]
    # df_filtered_split = dfFiltered.applymap(extract_before_newline)
    # df_filtered_split = df_filtered_split.fillna('0')
    # df_filtered_split[rankCols] = df_filtered_split[rankCols].apply(pd.to_numeric)
    defaultCols.remove('Branch_Code')
    # agrs = {x: 'first' if x in defaultCols else 'max' for x in filteredCols}
    # grouped_df = df_filtered_split.groupby('Branch Code').agg(agrs)
    
    filtered_df_State, filtered_df_Home, filtered_df_Other = filterAsPerHomeOtherState(dfFiltered, data)
    filtered_df_State['CutOff'] = filtered_df_State[rankCols].max(axis=1)
    homeCols = [x for x in casteGenderCols if x.endswith("H")] + [x for x in castePwdDefCols if x.endswith("H")] + otherCols
    awayCols = [x for x in casteGenderCols if x.endswith("O")] + [x for x in castePwdDefCols if x.endswith("O")] + otherCols
    filtered_df_Home['CutOff'] = filtered_df_Home[homeCols].max(axis=1)
    filtered_df_Other['CutOff'] = filtered_df_Other[awayCols].max(axis=1)
    combined_df = pd.concat([filtered_df_State, filtered_df_Home, filtered_df_Other], ignore_index=True, sort=False)
    combined_df_final = combined_df[defaultCols + ['Branch_Code','CutOff']]
    combined_df_final_Rem = combined_df_final[combined_df_final['CutOff'] != 0]
    combined_df_final_Sorted = combined_df_final_Rem.sort_values(by='CutOff')

    combined_df_final_Not_Eligible = combined_df_final_Sorted[combined_df_final_Sorted['CutOff'] < int(data['Rank'])]
    combined_df_final_Eligible = combined_df_final_Sorted[combined_df_final_Sorted['CutOff'] > int(data['Rank'])]

    noEligibleRows = 20
    eligibleRows = 40
    if len(combined_df_final_Not_Eligible.index) < 20:
        noEligibleRows = len(combined_df_final_Not_Eligible.index)
        eligibleRows = 60 - noEligibleRows

    eligible_df = combined_df_final_Eligible.head(eligibleRows)
    not_eligible_df = combined_df_final_Not_Eligible.tail(noEligibleRows)
    final_df = pd.concat([not_eligible_df, eligible_df], ignore_index=True, sort=False)
    # combined_df_final['deviation'] = abs(combined_df_final['CutOff'] - int(data['Rank']))
    # closest_rows = combined_df_final.nsmallest(60, 'deviation')
    # closest_rows = closest_rows.drop(columns='deviation')

    # grouped_df['CutOff'] = grouped_df.apply(lambda row: addCutOffColumn(row), axis=1)
    
    #df['Final'] = df[['category 1', 'category 2', 'category 3']].max(axis=1)
    #filtered_df = df[df['branch'] != 'CS'] and filtered_df = df[df['branch'] == 'CS']
    #df['Final'] = df.apply(lambda row: custom_function(row), axis=1)

    # Group by 'branch' and get the max from each category, also keep the first 'college' name in each group
        # grouped_df = df.groupby('branch').agg({
        #     'college': 'first',  # Keep the first occurrence of 'college' for each branch
        #     'category 1': 'max',
        #     'category 2': 'max',
        #     'category 3': 'max'
        # }).reset_index()
        
    return final_df

def collegeSuggestNew(data):
    predictTable = 'Cap1_cutoff_2024_Rank'
    defaultCols = getDefaultColumns()
    conn = sqlite3.connect("data.db")
    # college_list_query = "SELECT * FROM Cap1_Cutoff_Agg_2025;"
    # df = pd.read_sql(college_list_query, conn)
    filtered_df_University_Branch = filterAsPerPreference(data, conn)
    allCols = list(set(filtered_df_University_Branch['Category']))
    casteGenderCols = filterColumnsAsPerCasteGender(allCols, data)
    castePwdDefCols = filterColumnsAsPerPwdDef(allCols, data)
    otherCols = filterOtherColumns(data)
    rankCols = casteGenderCols + castePwdDefCols + otherCols
    # filteredCols = defaultCols + rankCols
    # dfFiltered = filtered_df_University_Branch[filteredCols]
    defaultCols.remove('Branch_Code')
    filtered_df_State, filtered_df_Home, filtered_df_Other = filterAsPerHomeOtherState(filtered_df_University_Branch, data)
    # filtered_df_State['CutOff'] = filtered_df_State[rankCols].max(axis=1)
    filtered_df_State = filtered_df_State[filtered_df_State['Category'].isin(rankCols)]
    filtered_df_State_Grouped = filtered_df_State.loc[filtered_df_State.groupby('branch_code')['2024'].idxmax()]
    homeCols = [x for x in casteGenderCols if x.endswith("H")] + [x for x in castePwdDefCols if x.endswith("H")] + otherCols
    awayCols = [x for x in casteGenderCols if x.endswith("O")] + [x for x in castePwdDefCols if x.endswith("O")] + otherCols
    filtered_df_Home = filtered_df_Home[filtered_df_Home['Category'].isin(homeCols)]
    filtered_df_Other = filtered_df_Other[filtered_df_Other['Category'].isin(awayCols)]
    # filtered_df_Home['CutOff'] = filtered_df_Home[homeCols].max(axis=1)
    # filtered_df_Other['CutOff'] = filtered_df_Other[awayCols].max(axis=1)
    filtered_df_Home_Grouped = filtered_df_Home.loc[filtered_df_Home.groupby('branch_code')['2024'].idxmax()]
    filtered_df_Other_Grouped = filtered_df_Other.loc[filtered_df_Other.groupby('branch_code')['2024'].idxmax()]
    combined_df = pd.concat([filtered_df_State_Grouped, filtered_df_Home_Grouped, filtered_df_Other_Grouped], ignore_index=True, sort=False)
    # combined_df_final = combined_df[defaultCols + ['Branch_Code','CutOff']]
    # combined_df_final_Rem = combined_df_final[combined_df_final['CutOff'] != 0]
    combined_df_final_Sorted = combined_df.sort_values(by='2024')

    combined_df_final_Not_Eligible = combined_df_final_Sorted[combined_df_final_Sorted['2024'] < int(data['Rank'])]
    combined_df_final_Eligible = combined_df_final_Sorted[combined_df_final_Sorted['2024'] > int(data['Rank'])]

    noEligibleRows = 20
    eligibleRows = 40
    if len(combined_df_final_Not_Eligible.index) < 20:
        noEligibleRows = len(combined_df_final_Not_Eligible.index)
        eligibleRows = 60 - noEligibleRows

    eligible_df = combined_df_final_Eligible.head(eligibleRows)
    not_eligible_df = combined_df_final_Not_Eligible.tail(noEligibleRows)
    final_df = pd.concat([not_eligible_df, eligible_df], ignore_index=True, sort=False)

    # # Adding cutoff for the past years
    # tableList = ['Cap1_cutoff_2023_Rank','Cap1_cutoff_2022_Rank','Cap1_cutoff_2021_Rank','Cap1_cutoff_2020_Rank']
    # branch_code_list = final_df['Branch_Code'].values.tolist()
    # for tbl in tableList:
    #     tbl_query = f"SELECT {', '.join(filteredCols)} FROM {tbl};"
    #     df = pd.read_sql(tbl_query, conn)
    #     # df['Branch_Code'] = df['Branch_Code'].str.lstrip('0')
    #     filtered_df_BranchCode = df[df['Branch_Code'].isin(branch_code_list)]
    #     filtered_df_State, filtered_df_Home, filtered_df_Other = filterAsPerHomeOtherState(filtered_df_BranchCode, data)
    #     filtered_df_State[f'CutOff_{tbl[12:16]}'] = filtered_df_State[rankCols].max(axis=1)
    #     homeCols = [x for x in casteGenderCols if x.endswith("H")] + [x for x in castePwdDefCols if x.endswith("H")] + otherCols
    #     awayCols = [x for x in casteGenderCols if x.endswith("O")] + [x for x in castePwdDefCols if x.endswith("O")] + otherCols
    #     filtered_df_Home[f'CutOff_{tbl[12:16]}'] = filtered_df_Home[homeCols].max(axis=1)
    #     filtered_df_Other[f'CutOff_{tbl[12:16]}'] = filtered_df_Other[awayCols].max(axis=1)
    #     combined_df = pd.concat([filtered_df_State, filtered_df_Home, filtered_df_Other], ignore_index=True, sort=False)
    #     combined_df_final = combined_df[['Branch_Code', f'CutOff_{tbl[12:16]}']]
    #     final_df = pd.merge(
    #                 final_df,
    #                 combined_df_final,
    #                 on='Branch_Code',
    #                 how='left',
    #                 # suffixes=('', '_new'),
    #             )
        # combined_df_final = combined_df[defaultCols + ['Branch Code','CutOff']]
        # combined_df_final_Rem = combined_df_final[combined_df_final['CutOff'] != 0]
        # combined_df_final_Sorted = combined_df_final_Rem.sort_values(by='CutOff')

        # combined_df_final_Not_Eligible = combined_df_final_Sorted[combined_df_final_Sorted['CutOff'] < int(data['Rank'])]
        # combined_df_final_Eligible = combined_df_final_Sorted[combined_df_final_Sorted['CutOff'] > int(data['Rank'])]

        # noEligibleRows = 20
        # eligibleRows = 40
        # if len(combined_df_final_Not_Eligible.index) < 20:
        #     noEligibleRows = len(combined_df_final_Not_Eligible.index)
        #     eligibleRows = 60 - noEligibleRows

        # eligible_df = combined_df_final_Eligible.head(eligibleRows)
        # not_eligible_df = combined_df_final_Not_Eligible.tail(noEligibleRows)
        # old_df = pd.concat([not_eligible_df, eligible_df], ignore_index=True, sort=False)
    conn.close()
    return final_df