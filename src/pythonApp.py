from flask import Flask,request, jsonify
import pandas as pd
from flask_cors import CORS
import json
from collegeFilter import collegeSuggest, getDataFromExcel, extract_before_newline, filterAsPerPreference
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

# Endpoint to fetch data from Excel
@app.route('/api/get-data', methods=['GET'])
def get_data():
    # Read data from Excel file (ensure the file is in the same directory as this script)
    try:
        path = 'C:/Users/Santo/Downloads/compiled_colleges_data.xlsx'  # Specify your Excel file name
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
    df = pd.read_excel('C:/Users/Santo/Downloads/collegeData.xlsx')
    data = df.to_dict(orient='records')
    # Convert the DataFrame to a list of dicts
    return json.dumps(data)


@app.route('/api/getCollegeList', methods=['POST'])
def collegeListPerUni():
    data = request.get_json()
    universityList = data['universityList']
    path = 'C:/Users/Santo/Downloads/compiled_colleges_data.xlsx'  # Specify your Excel file name
    df = getDataFromExcel(path)
    filtered_df_University = df[df['Home University'].isin(universityList)]
    branchList = list(set(filtered_df_University['Branch Name'])).sort()
    return json.dumps(branchList)

@app.route('/api/formSubmit', methods=['POST'])
def submit():
    data = request.get_json()  # Read JSON data from the request
    # print('Received data:', data)
    df = collegeSuggest(data)
    # df_filtered = df.applymap(extract_before_newline)
    # df_filtered = df_filtered.fillna('0')
    dataDf = df.to_dict(orient='records')
    # For now, just return the data back as a response
    return json.dumps(dataDf)
if __name__ == '__main__':
    app.run(debug=True)
