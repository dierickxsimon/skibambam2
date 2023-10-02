import pandas  as pd
import numpy as np

class CalculateFFM:
    def __init__(self):
        pass

    def StandardMethode(self, df):
        tau1 = 12
        tau2 = 5
        k1 = 1
        k2 = 2
        df['PTE'] = 0
        df['NTE'] = 0
        for i in range(1, len(df)):
            df.loc[i, 'PTE'] = df.loc[i - 1, 'PTE'] * np.exp(-1 / tau1) + df.loc[i, 'tlvalue']
            df.loc[i, 'NTE'] = df.loc[i - 1, 'NTE'] * np.exp(-1 / tau2) + df.loc[i, 'tlvalue']

        df['PTE'] = df['PTE'] * k1
        df['NTE'] = df['NTE'] * k2

        df['P(t)'] = df['PTE'] - df['NTE']

        return df




        print(df)
