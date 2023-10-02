from backend.DbController import DbController
from backend.Plots import Plots
from backend.FFM import CalculateFFM
import pandas as pd



class DataHandeling:
    def __init__(self):
        self.dbcontroller = DbController()
        self.conn = self.dbcontroller.getConnection()
        self.c = self.conn.cursor()
        self.plots = Plots()
        self.calculateFFM = CalculateFFM()


    def deleteMissing(self, table, column):
        dataCleaningQuery = f"DELETE FROM {table} WHERE {column} IS  NULL"
        self.dbcontroller.executeQuery(dataCleaningQuery)


    def tl_df_to_skibadf(self, tl_df):
        tl_df = tl_df.sort_values(by='timestamp')
        tl_df["timedelta"] = tl_df["timestamp"].diff()
        tl_df['days'] = tl_df['timedelta'] / pd.Timedelta(days=1)
        tl_df['days'] = tl_df['days'].fillna(0).astype(int)
        tl_df['cumsumdays'] = tl_df['days'].cumsum()


        totDays = tl_df['cumsumdays'].iloc[-1]
        days = range(0, totDays + 2)
        totDays +=2
        tl = [0] * totDays
        df = pd.DataFrame({'cumsumdays': days, 'tlvalue': tl})

        merged_df = pd.merge(df, tl_df, on='cumsumdays', how='left')
        merged_df['tlvalue'] = merged_df['tlvalue_y'].fillna(0)
        skibadf = merged_df[['cumsumdays', 'tlvalue']]
        skibadf = skibadf.rename(columns= {'cumsumdays':'days'} )
        print(skibadf)
        skibadf.loc[-1] = [0, 0]  # adding a row
        skibadf.index = skibadf.index + 1  # shifting index
        skibadf.sort_index(inplace=True)

        return skibadf


    def athlete_full_name(self):
        columns = "first_name, name"
        table = ('athlete')
        athletes = self.dbcontroller.getAllValuesincolumns(columns, table)
        athletes_full_name=[]
        for tup in athletes:
            full_name = tup[0] + ' ' + tup[1]
            athletes_full_name.append(full_name)
        return athletes_full_name

    def return_list_off_tl_types(self):
        columns = "name"
        table = 'trainingloadtypes'
        types = self.dbcontroller.getAllValuesincolumns(columns, table)
        tl_types = []
        for tup in types:
            type = tup[0]
            tl_types.append(type)

        return tl_types

    def returns_an_athlete_id_on_basis_of_first_second_name(self, name_tuple):
        columns = 'id_athlete'
        table = 'athlete'
        testvalue1 = 'first_name'
        parameter1 = name_tuple[0]
        testvalue2 = 'name'
        parameter2 = name_tuple[1]
        id_athelete = self.dbcontroller.getValuesBytwoParameters(columns,table,testvalue1,parameter1,testvalue2, parameter2)
        return id_athelete

    def get_id_tl(self, name):
        columns = 'id_trainingloadtypes'
        table = 'trainingloadtypes'
        testvalue = 'name'
        parameter = name

        id_tl = self.dbcontroller.getValueByParameter(columns, table, testvalue, parameter)

        return id_tl

    def plot_it(self, id_tl, id_athlete):
        df = self.dbcontroller.joinTables(id_athlete, id_tl)
        df = self.tl_df_to_skibadf(df)
        timestamp=df["days"]
        tlvalue =df["tlvalue"]
        self.plots.tlplot(tlvalue, timestamp)

        df = self.calculateFFM.StandardMethode(df)
        days = df['days']
        PTE = df['PTE']
        NTE = df['NTE']
        P = df['P(t)']
        self.plots.plot_ffm(PTE, NTE, P, days)