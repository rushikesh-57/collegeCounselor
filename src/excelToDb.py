import sqlite3
import pandas as pd

# Step 1: Connect to SQLite database (creates file if not exists)
# conn = sqlite3.connect("data.db")
# cursor = conn.cursor()

# # Step 2: Create a Table
# cursor.execute("""DROP TABLE Cap1_cutoff_2021_Percentile;""")
# cursor.execute("""
# CREATE TABLE IF NOT EXISTS Cap1_cutoff_2024_Rank ("Branch Code" TEXT, "College Code" INTEGER, "College Name" TEXT, "Status" TEXT, "Home University" TEXT, 
#                "Branch Name" TEXT, "Admission Type" TEXT, "GOPENS" INTEGER, "GSCS" INTEGER, "GSTS" INTEGER, "GVJS" INTEGER, "GNT1S" INTEGER, "GNT2S" INTEGER, 
#                "GNT3S" INTEGER, "GOBCS" INTEGER, "GSEBCS" INTEGER, "LOPENS" INTEGER, "LSCS" INTEGER, "LSTS" INTEGER, "LVJS" INTEGER, "LNT2S" INTEGER, "LOBCS" INTEGER,
#                 "LSEBCS" INTEGER, "PWDOPENS" INTEGER, "PWDOBCS" INTEGER, "DEFOPENS" INTEGER, "DEFOBCS" INTEGER, "TFWS" INTEGER, "PWDROBCS" INTEGER,
#                 "DEFRSEBCS" INTEGER, "EWS" INTEGER, "LNT1S" INTEGER, "LNT3S" INTEGER, "PWDRSCS" INTEGER, "DEFROBCS" INTEGER, "ORPHAN" INTEGER, "DEFRNT1S" INTEGER,
#                 "GOPENH" INTEGER, "GSCH" INTEGER, "GSTH" INTEGER, "GNT2H" INTEGER, "GOBCH" INTEGER, "GSEBCH" INTEGER, "LOPENH" INTEGER, "LOBCH" INTEGER, "LSEBCH" INTEGER,
#                 "GSCO" INTEGER, "GVJO" INTEGER, "LOPENO" INTEGER, "GVJH" INTEGER, "LNT2H" INTEGER, "GOPENO" INTEGER, "GOBCO" INTEGER, "GSEBCO" INTEGER, "LOBCO" INTEGER,
#                 "LSCH" INTEGER, "GNT3H" INTEGER, "LSTH" INTEGER, "LVJH" INTEGER, "LNT1H" INTEGER, "PWDOPENH" INTEGER, "GNT1O" INTEGER, "GNT2O" INTEGER, "GNT3O" INTEGER,
#                 "LSTO" INTEGER, "GNT1H" INTEGER, "LNT3H" INTEGER, "PWDOBCH" INTEGER, "GSTO" INTEGER, "LSCO" INTEGER, "LVJO" INTEGER, "LNT2O" INTEGER, "LSEBCO" INTEGER,
#                 "LNT1O" INTEGER, "LNT3O" INTEGER, "PWDROBCH" INTEGER, "DEFSCS" INTEGER, "PWDRSTS" INTEGER, "MI" INTEGER, "PWDRSEBCS" INTEGER, "PWDRNT2S" INTEGER,
#                 "DEFRSCS" INTEGER, "DEFRNT2S" INTEGER, "PWDSCS" INTEGER, "DEFSEBCS" INTEGER, "DEFRVJS" INTEGER, "PWDSCH" INTEGER, "PWDSEBCS" INTEGER, "PWDRSCH" INTEGER,
#                 "PWDRSTH" INTEGER, "PWDRSEBCH" INTEGER, "DEFRNT3S" INTEGER, "PWDRVJS" INTEGER, "PWDRNT3S" INTEGER, "PWDRNT1S" INTEGER, "DEFSTS" INTEGER);
# """)


# # Step 3: Commit and close
# conn.commit()
# conn.close()

# print("Database and table created successfully!")


# Step 1: Read Excel file
file_path = 'C:/Work/College Counselor/Cutoff/csv files/Percentile/Group/Cap 1 cutoff 24-25 Percentile.xlsx'  # Change this to your Excel file path
df = pd.read_excel(file_path)

# Step 2: Connect to SQLite
conn = sqlite3.connect("data.db")
cursor = conn.cursor()

# Step 3: Create Table Dynamically
columns = df.columns
textCols = ['College Name', 'Status', 'Home University', 'Branch Name', 'Admission Type']
column_definitions = ", ".join([f'"{col}" TEXT' if col in textCols else f'"{col}" INTEGER' for col in columns])  # Assuming all columns as TEXT
create_table_query = f'CREATE TABLE IF NOT EXISTS Cap1_cutoff_2024_Percentile ({column_definitions});'

cursor.execute(create_table_query)

# Step 4: Insert Data Dynamically
for _, row in df.iterrows():
    placeholders = ", ".join(["?" for _ in columns])
    insert_query = f'INSERT INTO Cap1_cutoff_2024_Percentile VALUES {tuple(row)}'
    # insert_query = f'INSERT INTO Cap1_cutoff_2024_Rank ({", ".join(columns)}) VALUES ({placeholders})'
    cursor.execute(insert_query)

# Step 5: Commit and Close
conn.commit()
conn.close()

print("Table created and data inserted successfully!")