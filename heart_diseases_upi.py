''' This code is using Heart disease Dataset'''
import sqlite3
from sqlalchemy import create_engine
import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('heart.csv')
df = df.sample(frac=1).reset_index(drop=True)

print(df.describe())
print(df.columns)

#Creating an engine that will enable SQL querying
engine = create_engine('sqlite://',echo = False)
sql = df.to_sql('heart_', con = engine)

print('Query options : ')
print('1. quit', '2. list', '3. graphs', '4. SQL')

# Infinite Querying loop
while True:
    try:
        query = input('Enter your query : ')
        #For quitting the qurying loop
        if re.search('quit', query):
            break
        elif re.search('list', query):
            print(df.columns)
        
        # For making Visualization 2D or 1D
        elif re.search('graphs', query):
            axis = int(input('Enter number of axes : '))
            if axis==2:
                print(df.columns)
                print('Chose from the above features : ')
                X_ax = input('Please enter X feature : ')
                Y_ax = input('Please enter Y feature : ')
                # To check if the feature is Categorical or Continuous
                if df[X_ax].nunique() > 6:
                    f = df.copy()
                    f = f.sort_values(X_ax)
                    sns.lmplot(x = X_ax, y = Y_ax, data = f, fit_reg = True)
                else:
                    sns.barplot(x = X_ax, y = Y_ax, data = df)
                #plt.legend()
                
            else:
                X_ax = input('Please enter X feature : ')
                if df[X_ax].nunique() > 6:
                    plt.plot(df[X_ax])
                    plt.legend()
                else:
                    sns.countplot(x = df[X_ax], data = df)
            plt.show()

        elif re.search('SQL', query):
            q = input('Enter your SQL Query : ')
            print(engine.execute(q).fetchall())

        
        query_split = query.split()
        query_len = len(query_split)
        
        for i in range(query_len):
            if re.search(query_split[0], 'avg') or re.search(query_split[0], 'average'):
                aggregate = 'avg'
            
                column = query_split[1]
                flag = 1
            else:
                column = query_split[0]
                flag = 0
        if flag == 1:
            for i in range(len(df.columns)):
                if re.search(df.columns[i], column):
                    print('Match found')
                    q = 'select ' + aggregate+'('+df.columns[i]+')'+' from heart_'
                    print(engine.execute(q).fetchall())
                    
        elif flag == 0:
            for i in range(len(df.columns)):
                if re.search(df.columns[i], column):
                    q = 'select ' +df.columns[i]+' from heart_'
                    print(engine.execute(q).fetchall())
        
        
    except Exception as e:
        print('Invalid query\n')
'''
Notes:
 To filter columns based on data types:
     Numeric:
         numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        dataframe = df.select_dtypes(exclude=numerics)
'''
        
