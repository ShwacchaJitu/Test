import pandas as pd

# Load the Excel file, starting from column 2 (B) and skipping the first row
file_path = 'login info.xlsx'
df = pd.read_excel(file_path)
url = df.iloc[0, 1]

org_userid = df.iloc[1, 1]
org_pass = df.iloc[1, 2]

facility_userid = df.iloc[2, 1]
facility_pass  = df.iloc[2, 2]

department_userid  = df.iloc[3, 1]
department_pass  = df.iloc[3, 2]

stm1_userid  =  df.iloc[4, 1]
stm1_pass =  df.iloc[4, 2]

stm2_userid  = df.iloc[5, 1]
stm2_pass  = df.iloc[5, 2]

ulink_userid  = df.iloc[6, 1]
ulink_pass  = df.iloc[6, 2]

otp  = df.iloc[3, 3]
browser = df.iloc[9, 1]
user = df.iloc[10, 1]



print(url)
print(org_userid , org_pass)
print(facility_userid ,facility_pass)
print(department_userid, department_pass)
print(stm1_userid, stm1_pass)
print(stm2_userid, stm2_pass)
print(ulink_userid, ulink_pass)
print(browser)
print(user)



