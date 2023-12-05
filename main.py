import pyautogui
import webbrowser
import time
import pyperclip
import pandas as pd
import psycopg2
from psycopg2 import sql
import os
import subprocess

dbname = 'original'
user = 'postgres'
password = 'root'
host = 'localhost'
port = '5432'

# Establish a connection to the PostgreSQL database
conn = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, port=port)

# Create a cursor object to execute SQL queries
cursor = conn.cursor()

# Example: Retrieve data from a table named 'credentials'
table_name = 'credentials'

# Execute a SELECT query
# query = sql.SQL('SELECT * FROM {}').format(sql.Identifier(table_name))
# query_str = query.as_string(conn)  # Convert the Composable object to a string

query_str = f'select * from {table_name}'
df = pd.read_sql(query_str, conn)
print(df)
# Initialize empty arrays to store usernames and passwords
usernames = []
passwords = []

# Populate the arrays
for index, row in df.iterrows():
    usernames.append(row['username'])
    passwords.append(row['password'])

# Now you have two separate arrays: usernames and passwords
print("Usernames:", usernames)
print("Passwords:", passwords)
for username, password in zip(usernames, passwords):
    print(username, password)
    

#result_data = {row['username']: row['password'] for index, row in df.iterrows()} 
#print(result_data)

#for username, password in result_data.items():
    #print(username, 'vvvvvvvvvvv', password)
    x = username
    y = password
    Hoppr = "https://app.hoppr.in/login"
    # login_path = " "
    webbrowser.open(Hoppr)
    time.sleep(2)
    pyautogui.typewrite(x)
    time.sleep(1)
    pyautogui.press('tab')
    pyautogui.typewrite(y)
    pyautogui.moveTo(829, 440, duration=1)
    pyautogui.click()
    time.sleep(2)
    pyautogui.moveTo(218, 412, duration=1)
    pyautogui.click()
    time.sleep(2)

    pyautogui.moveTo(288, 78, duration=1)
    pyautogui.click()
    pyautogui.hotkey('ctrl', 'c')
    # click
    # copy cntrl + v
    login_path = pyperclip.paste()
    time.sleep(1)

    if Hoppr == login_path:
        pyautogui.hotkey('ctrl', 'w')
        print("Error: Hoppr not found")
        continue
    pyautogui.moveTo(218, 412, duration=1)
    pyautogui.click()
    pyautogui.FAILSAFE = False

    # ____----------------------
    pyautogui.moveTo(544, 393, duration=1)
    try:
        pyautogui.dragRel(544, 123, duration=1)
    except pyautogui.FailSafeException as e:
        print(f"Fail-safe triggered: {e}")
    
    pyautogui.hotkey('ctrl', 'c')
    time.sleep(2)
    copied_data = pyperclip.paste()
    lines = copied_data.strip().split('\n')

    # create directory to store data
    data_dict = {}
    print(lines,'lineslines')
    current_key = None
    for line in lines:
        if ':' in line:
            print(line.split(':'))
            key, value =  line.split(':') #[part.strip() for part in line.split(': ', 1)]
            print(key, value)
            current_key = key
            data_dict[key.strip()] = value.strip()
        elif current_key is not None:
            data_dict[current_key] += f" {line.strip()}"
    print(data_dict,'AAAA')        
    pyautogui.hotkey('ctrl', 'w')
    df = pd.DataFrame(list(data_dict.items()), columns=['Field', 'value'])
    df_transposed = df.transpose()
    df_transposed.columns = df_transposed.iloc[0]
    df_transposed = df_transposed.drop(df_transposed.index[0])
    print(df_transposed, 'df_transposeddf_transposed', df_transposed.to_dict())
    csv_file_path = '/home/buzzadmin/Documents/dumped.csv'
    if os.path.isfile(csv_file_path):
        print('IMIM 222222222222')
        df_transposed.to_csv(csv_file_path, mode='a', header=False, index=False)
    else:
        print('gufrhgbjkiuhjn')
        df_transposed.to_csv(csv_file_path, index=False)
    time.sleep(1)
    #subprocess.run(['xdg-open', csv_file_path])
    #pyautogui.moveTo(920, 693, duration=1)
    #pyautogui.click()

    hoppr = "https://app.hoppr.in/logout"
    webbrowser.open(hoppr)
    time.sleep(1)
    pyautogui.hotkey('ctrl', 'w')
    time.sleep(2)

subprocess.run(['xdg-open', csv_file_path])
pyautogui.moveTo(920, 693, duration=1)
pyautogui.click()

