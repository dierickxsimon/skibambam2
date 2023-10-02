#import MySQLdb as mysql
import mysql.connector as mysql
import pandas as pd

class DbController:
    def __init__(self):
        self.conn = mysql.connect(
            host="localhost",
            user="root",
            database='learningffmdb',
            password="Masterproef2*",
            auth_plugin='mysql_native_password',
        )

    def getConnection(self):
        return self.conn


    def insert(self, table, values):
        cursor = self.conn.cursor()
        query = f"INSERT INTO {table} VALUES {values}"
        cursor.execute(query)
        self.conn.commit()

        last_row_id = cursor.lastrowid

        return last_row_id

    def insertRow(self, table, columns, values):
        cursor = self.conn.cursor()
        columns_str = "(" + ", ".join(columns) + ")"
        values_str = "(" + ", ".join(["%s"] * len(values)) + ")"
        query = f"INSERT INTO {table} {columns_str} VALUES {values_str}"


        cursor.execute(query, values)
        self.conn.commit()

        last_row_id = cursor.lastrowid
        return last_row_id

    def insert_many_rows(self, table_name, columns, rows):
        cursor = self.conn.cursor()
        placeholders = ','.join(['%s'] * len(columns))
        query = f"INSERT INTO {table_name} ({','.join(columns)}) VALUES ({placeholders})"
        try:
            cursor.executemany(query, rows)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Error inserting rows into {table_name}: {e}")



    def getValueByParameter(self, columns, table, testvalue, parameter):
        cursor = self.conn.cursor()
        query = f"SELECT {columns} FROM {table} WHERE {testvalue} = %s"
        params = (parameter,)
        cursor.execute(query, params)
        result = cursor.fetchall()
        if result is None:
            return None

        return result

    def getValuesBytwoParameters(self, columns, table, testvalue1, parameter1, testvalue2, parameter2):
        cursor = self.conn.cursor()
        query = f"SELECT {columns} FROM {table} WHERE {testvalue1} = %s AND {testvalue2} = %s"
        params = (parameter1, parameter2)
        cursor.execute(query, params)
        result = cursor.fetchall()
        if result is None:
            return None
        return result


    def getAllValuesincolumns(self, columns, table):
        cursor = self.conn.cursor()
        query = f'SELECT {columns} FROM {table}'
        cursor.execute(query)
        result = cursor.fetchall()

        return result



    def executeQuery(self, query):
        cursor = self.conn.cursor()
        cursor.execute(query)
        self.conn.commit()


    def getAthletesValues(self, id):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT first_name, name, max_hr, rest_hr, vo2max FROM athlete WHERE id_athlete = {id}")
        result = cursor.fetchone()

        return {
            'first_name': result[0],
            'name': result[1],
            'max_hr': result[2],
            'rest_hr': result[3],
            'vo2max': result[4],
        }


    def joinTables(self, id_athlete, id_trainingload):
        query = f'''
                    SELECT t.timestamp, v.tlvalue 
                    FROM trainingload v
                    JOIN training t
                    ON v.id_training = t.id_training
                    where t.id_athlete = {id_athlete} and v.id_trainingloadtypes = {id_trainingload}
                '''

        df = pd.read_sql_query(query, self.conn)
        return df

    def deletedb(self):
        cursor = self.conn.cursor()
        queries = [
            'DELETE FROM trainingload',
            'DELETE FROM trainingdata',
            'DELETE FROM training',
            'DELETE FROM athlete'
        ]
        for query in queries:
            cursor.execute(query)

        self.conn.commit()

    def saveAthelteInDataBase(self, athlete):
        c = self.conn.cursor()
        c.execute("INSERT INTO athlete (name, first_name, max_hr, rest_hr, vo2max) values (%s, %s, %s, %s, %s)", athlete)
        self.conn.commit()