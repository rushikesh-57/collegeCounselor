import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
# from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
import sqlite3
# from statsmodels.tsa.arima.model import ARIMA
from sklearn.ensemble import RandomForestRegressor

def predict_wma(row):
    """Weighted Moving Average (WMA) ignoring zero values"""
    years = [col for col in row.index if str(col).startswith("20") and col != 2024 and row[col] > 0]
    if len(years) < 2:
        return row[years[0]] if len(years) == 1 else 0
    weights = np.linspace(0.1, 0.9, len(years))
    weights /= np.sum(weights)
    return np.sum(row[years].values * weights)

def predict_lr(row):
    """Linear Regression Model"""
    years = [col for col in row.index if str(col).startswith("20") and col != 2024 and row[col] > 0]
    if len(years) < 2:
        return row[years[0]] if len(years) == 1 else 0
    X = np.array([int(y) for y in years]).reshape(-1, 1)
    y = row[years].values
    model = LinearRegression().fit(X, y)
    return model.predict([[2024]])[0]

# def predict_ets(row):
#     """Exponential Smoothing (ETS)"""
#     years = [col for col in row.index if str(col).startswith("20") and col != 2024 and row[col] > 0]
#     if len(years) < 2:
#         return row[years[0]] if len(years) == 1 else 0
#     model = ExponentialSmoothing(row[years].values, trend="add").fit()
#     return model.forecast(1)[0]

# def predict_arima(row):
#     """AutoRegressive Integrated Moving Average (ARIMA)"""
#     years = [col for col in row.index if str(col).startswith("20") and col != 2024 and row[col] > 0]
#     if len(years) < 2:
#         return row[years[0]] if len(years) == 1 else 0
#     model = ARIMA(row[years].values, order=(2, 1, 2)).fit()
#     return model.forecast(1)[0]

def predict_rf(row):
    """Random Forest Regressor"""
    years = [col for col in row.index if str(col).startswith("20") and row[col] > 0]
    if len(years) < 2:
        return row[years[0]] if len(years) == 1 else 0
    X = np.array([int(y) for y in years]).reshape(-1, 1)
    y = row[years].values
    model = RandomForestRegressor(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model.predict([[2025]])[0]

tableList = ['Cap1_cutoff_2024_Rank','Cap1_cutoff_2023_Rank','Cap1_cutoff_2022_Rank','Cap1_cutoff_2021_Rank','Cap1_cutoff_2020_Rank']
dfs = {}
conn = sqlite3.connect("data.db")
c = 2024
l = ['College_Code', 'College_Name', 'Status', 'Home_University', 'Branch_Name', 'Admission_Type']
for tbl in tableList:
    tbl_query = f"SELECT * FROM {tbl};"
    df = pd.read_sql(tbl_query, conn)
    allCols = list(df.columns)
    # allCols.remove('Status')
    # allCols.remove('Home_University')
    finalCols = [x for x in allCols if x not in l]
    fil_df=df[finalCols]
    dfs[c] = fil_df.assign(Year=c)
    c -= 1

cols = ['Branch_Code']

# Merge all years into a single DataFrame
merged_df = pd.concat(dfs.values(), ignore_index=True).sort_values(by=cols + ['Year'])

# Convert from wide to long format for easier processing
melted_df = merged_df.melt(id_vars= cols + ['Year'], var_name='Category', value_name='Cutoff')
melted_df = melted_df[melted_df['Cutoff'] > 0]

# Pivot to reshape for ML models
pivot_df = melted_df.pivot(index= cols + ['Category'], columns='Year', values='Cutoff').reset_index()
# pivot_df = pivot_df.dropna(axis=1, how='all')
# pivot_df = pivot_df[pivot_df[2024] > 0]
# pivot_df["Predicted_2024_WMA"] = pivot_df.apply(predict_wma, axis=1)
# pivot_df = pivot_df[pivot_df["Predicted_2024_WMA"] > 0]
# pivot_df["Predicted_2024_LR"] = pivot_df.apply(predict_lr, axis=1)
# pivot_df = pivot_df[pivot_df["Predicted_2024_LR"] > 0]
# pivot_df["Predicted_2024_ARIMA"] = pivot_df.apply(predict_arima, axis=1)
# pivot_df = pivot_df[pivot_df["Predicted_2024_ARIMA"] > 0]
pivot_df["Predicted_2024_RF"] = pivot_df.apply(predict_rf, axis=1)
pivot_df = pivot_df[pivot_df["Predicted_2024_RF"] > 0]
# Convert back to wide format with 'Men' and 'Women' columns
predicted_df = pivot_df.pivot(index=cols, columns='Category', values='Predicted_2025_WMA').reset_index()

# Rename columns for clarity
predicted_df.columns.name = None  # Remove multi-level column index
predicted_df.to_csv('C:/Work/pivot_predicted_cutoffs_RF.csv', index=False)
pivot_df.to_csv('C:/Work/pivot_RF.csv', index=False)
# pivot_df["Predicted_2024_ETS"] = pivot_df.apply(predict_ets, axis=1)

# Calculate error for each model
# pivot_df["Error_WMA"] = abs(pivot_df[2024] - pivot_df["Predicted_2024_WMA"])
# pivot_df["Error_LR"] = abs(pivot_df[2024] - pivot_df["Predicted_2024_LR"])
# # pivot_df["Error_ARIMA"] = abs(pivot_df[2024] - pivot_df["Predicted_2024_ARIMA"])
# pivot_df["Error_RF"] = abs(pivot_df[2024] - pivot_df["Predicted_2024_RF"])
# # pivot_df["Error_ETS"] = abs(pivot_df["2024"] - pivot_df["Predicted_2024_ETS"])

# # Compute Mean Absolute Error (MAE) for each model
# mae_wma = mean_absolute_error(pivot_df[2024], pivot_df["Predicted_2024_WMA"])
# mae_lr = mean_absolute_error(pivot_df[2024], pivot_df["Predicted_2024_LR"])
# # mae_arima = mean_absolute_error(pivot_df[2024], pivot_df["Predicted_2024_ARIMA"])
# mae_rf = mean_absolute_error(pivot_df[2024], pivot_df["Predicted_2024_RF"])
# # mae_ets = mean_absolute_error(pivot_df["2024"], pivot_df["Predicted_2024_ETS"])

# # Choose the best model based on lowest MAE
# best_model = min([("WMA", mae_wma), ("LR", mae_lr), ("RF", mae_rf)], key=lambda x: x[1])

# print(f"MAE (WMA): {mae_wma}")
# print(f"MAE (LR): {mae_lr}")
# # print(f"MAE (ETS): {mae_ets}")
# # print(f"MAE (ARIMA): {mae_arima}")
# print(f"MAE (RF): {mae_rf}")
# print(f"Best Model: {best_model[0]}")
