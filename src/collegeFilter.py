from flask import Flask, jsonify
import pandas as pd
from flask_cors import CORS
import json

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
    return ['College Code', 'College Name', 'Status', 'Home University', 'Branch Code', 'Branch Name', 'Admission Type']

def addCutOffColumn(row):
    cutoff = 0
    if row['Admission Type'] == 'State Level':
        pass
    if row["Home University"] == dd['HomeUniversity']:
        pass
    return True

def getDataFromExcel(path):
    df = pd.read_excel(path)
    return df

def filterAsPerPreference(df, data):
    #Need to add clg filter
    if data['PrefferedUniversity']:
        filtered_df_University = df[df['Home University'].isin(data['PrefferedUniversity'])]
        if data['PrefferedBranch']:
            filtered_df_University_Branch = filtered_df_University[filtered_df_University['Branch Name'].isin(data['PrefferedBranch'])]
            return filtered_df_University_Branch
        else:
            return filtered_df_University
    else:
        if data['PrefferedBranch']:
            filtered_df_Branch = df[df['Branch Name'].isin(data['PrefferedBranch'])]
            return filtered_df_Branch
    return df

def filterAsPerHomeOtherState(df, data):
    filtered_df_State = df[df['Admission Type'] == 'State Level']
    filtered_df_Not_State = df[df['Admission Type'] != 'State Level']
    filtered_df_Home = filtered_df_Not_State[filtered_df_Not_State['Home University'] == data['HomeUniversity']]
    filtered_df_Other = filtered_df_Not_State[filtered_df_Not_State['Home University'] != data['HomeUniversity']]
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

# def addColumn

def collegeSuggest(data):
    path = 'C:/Users/Santo/Downloads/compiled_colleges_data.xlsx'
    df = pd.read_excel(path)
    allCols = list(df.columns)
    filtered_df_University_Branch = filterAsPerPreference(df, data)

    defaultCols = getDefaultColumns()
    casteGenderCols = filterColumnsAsPerCasteGender(allCols, data)
    castePwdDefCols = filterColumnsAsPerPwdDef(allCols, data)
    otherCols = filterOtherColumns(data)
    rankCols = casteGenderCols + castePwdDefCols + otherCols
    filteredCols = defaultCols + rankCols
    dfFiltered = filtered_df_University_Branch[filteredCols]
    df_filtered_split = dfFiltered.applymap(extract_before_newline)
    df_filtered_split = df_filtered_split.fillna('0')
    df_filtered_split[rankCols] = df_filtered_split[rankCols].apply(pd.to_numeric)
    defaultCols.remove('Branch Code')
    agrs = {x: 'first' if x in defaultCols else 'max' for x in filteredCols}
    grouped_df = df_filtered_split.groupby('Branch Code').agg(agrs)
    
    filtered_df_State, filtered_df_Home, filtered_df_Other = filterAsPerHomeOtherState(grouped_df, data)
    filtered_df_State['CutOff'] = filtered_df_State[rankCols].max(axis=1)
    homeCols = [x for x in casteGenderCols if x.endswith("H")] + [x for x in castePwdDefCols if x.endswith("H")] + otherCols
    awayCols = [x for x in casteGenderCols if x.endswith("O")] + [x for x in castePwdDefCols if x.endswith("O")] + otherCols
    filtered_df_Home['CutOff'] = filtered_df_Home[homeCols].max(axis=1)
    filtered_df_Other['CutOff'] = filtered_df_Other[awayCols].max(axis=1)
    combined_df = pd.concat([filtered_df_State, filtered_df_Home, filtered_df_Other], ignore_index=True, sort=False)
    combined_df_final = combined_df[defaultCols + ['Branch Code','CutOff']]
    combined_df_final_Rem = combined_df_final[combined_df_final['CutOff'] != 0]
    combined_df_final_Sorted = combined_df_final_Rem.sort_values(by='CutOff')

    combined_df_final_Not_Eligible = combined_df_final_Sorted[combined_df_final_Sorted['CutOff'] < int(data['Rank'])]
    combined_df_final_Eligible = combined_df_final_Sorted[combined_df_final_Sorted['CutOff'] > int(data['Rank'])]

    eligible_df = combined_df_final_Eligible.head(40)
    not_eligible_df = combined_df_final_Not_Eligible.tail(20)
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