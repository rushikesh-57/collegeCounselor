from flask import Flask,request, jsonify
import pandas as pd
from flask_cors import CORS
import json
from collegeFilter import collegeSuggest, getDataFromExcel, extract_before_newline, filterAsPerPreference, collegeSuggestNew
import sqlite3
app = Flask(__name__)
# CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})
CORS(app)

# Endpoint to fetch data from Excel
@app.route('/api/get-data', methods=['GET'])
def get_data():
    # Read data from Excel file (ensure the file is in the same directory as this script)
    try:
        path = 'C:/Work/collegeCounselor/src/compiled_colleges_data.xlsx'  # Specify your Excel file name
        df = getDataFromExcel(path)
        df_filtered = df.applymap(extract_before_newline)
        df_filtered = df_filtered.fillna('0')
        data = df_filtered.to_dict(orient='records')
        # Convert the DataFrame to a list of dicts
        return json.dumps(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/getCollegeData', methods=['GET'])
def collegeData():
    # df = pd.read_excel('C:/Work/collegeCounselor/src/collegeData.xlsx')
    # data = df.to_dict(orient='records')
    conn = sqlite3.connect("data.db")
    college_list_query = "SELECT `College Name`, `Branch Name` FROM Cap1_cutoff_2024_Rank;"
    df = pd.read_sql(college_list_query, conn)
    data = df.to_dict(orient='records')
    conn.close()
    # Convert the DataFrame to a list of dicts
    return json.dumps(data)


@app.route('/api/getCollegeList', methods=['POST'])
def collegeListPerUni():
    data = request.get_json()
    districtList = data['districtList']
    print(districtList)
    conn = sqlite3.connect("data.db")
    sqlQuery = """ SELECT DISTINCT(b.branch_name) from Branch b join College c ON b.college_code = c.college_code WHERE 1 = 1 """
    if districtList:
        sqlQuery = sqlQuery + f""" AND c.District IN ({', '.join(f"'{item}'" for item in districtList)}) ;"""
    print(sqlQuery)
    df = pd.read_sql(sqlQuery, conn)
    conn.close()
    branchList = list(set(df['branch_name'].to_list()))
    # print(branchList)
    return json.dumps(branchList)

@app.route('/api/formSubmit', methods=['POST'])
def submit():
    data = request.get_json()  # Read JSON data from the request
    # print('Received data:', data)
    # df = collegeSuggest(data)
    df = collegeSuggestNew(data)
    # df_filtered = df.applymap(extract_before_newline)
    # df_filtered = df_filtered.fillna('0')
    df.fillna(0, inplace=True)
    dataDf = df.to_dict(orient='records')
    # For now, just return the data back as a response
    return json.dumps(dataDf)

if __name__ == '__main__':
    app.run(debug=True)