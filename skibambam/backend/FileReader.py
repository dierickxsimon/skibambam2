
#import mysql.connector as mysql
import pytz
import csv
import fitparse
from backend.DbController import DbController
import os


class FileReader:
    def __init__(self, fit):
        self.FIT = fit
        self.CSVpath = 'C:/MP/test/CSV'
        self.allowed_fields = ['timestamp', 'position_lat', 'position_long', 'distance',
                               'enhanced_altitude', 'altitude', 'enhanced_speed',
                               'speed', 'heart_rate', 'temperature', 'cadence', 'fractional_cadence']
        self.required_fields = ['timestamp']

        self.UTC = pytz.UTC
        self.CST = pytz.timezone('Europe/Brussels')
        self.dbcontroller = DbController()
        self.conn = self.dbcontroller.getConnection()
        self.c = self.conn.cursor()



    def writeCsv(self):
        fit_files = self.FIT
        for file in fit_files:
            new_filename = self.CSVpath + '/' + os.path.basename(file)[:-4] + '.csv'
            if os.path.exists(new_filename):
                print('%s already exists. skipping.' % new_filename)
                continue
            fitfile = fitparse.FitFile(file, data_processor=fitparse.StandardUnitsDataProcessor())

            print('converting %s' % file)
            self.writeFitFileToCsv(fitfile, new_filename)
        print('finished conversions')

    def writeFitFileToCsv(self, fitfile, output_file):
        messages = fitfile.messages
        self.output_file = self.CSVpath
        # raw data in messages in one line
        data = []
        for m in messages:
            skip = False
            if not hasattr(m, 'fields'):
                continue
            fields = m.fields
            # check for important data types
            mdata = {}
            for field in fields:

                if field.name in self.allowed_fields:
                    if field.name == 'timestamp':
                        mdata[field.name] = self.UTC.localize(field.value).astimezone(self.CST)
                    else:
                        mdata[field.name] = field.value
            for rf in self.required_fields:
                if rf not in mdata:
                    skip = True

            if not skip:
                data.append(mdata)
                # write to csv
        with open(output_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(self.allowed_fields)

            for entry in data:
                line_file = []
                for k in self.allowed_fields:
                    data_var = str(entry.get(k, ""))
                    # print(entry," ", k," " ,data_var)
                    line_file.append(data_var)

                writer.writerow(line_file)

    def saveIntoDb(self, athleteid):
        files = os.listdir(self.CSVpath)

        csv_files = [file for file in files if file.endswith('.csv')]

        for file in csv_files:
            with open(os.path.join(self.CSVpath, file)) as csv_file:
                csv_reader = csv.reader(csv_file, delimiter=',')

                # Skip header row
                next(csv_reader)

                # Get the name of the table from the file name
                table_name = file[:-4].lower()

                # Insert a row into the training table
                id_athlete = athleteid
                first_row = next(csv_reader)
                timestamp = first_row[0]

                training_columns = ['id_athlete', 'timestamp', 'name']
                training_values = [id_athlete, timestamp, table_name]

                training_id = self.dbcontroller.insertRow('training', training_columns, training_values)

                # Process the remaining rows and insert them into the trainingdata table
                training_data_columns = ['id_training', 'id_athlete', 'timestamp', 'position_lat', 'position_long',
                                         'distance', 'enhanced_altitude', 'enhanced_speed', 'speed', 'temperature',
                                         'heart_rate', 'cadence', 'fractional_cadance']
                all_values = []

                for row in csv_reader:
                    print(row[6])
                    if row[6] == 'None':
                        os.remove(os.path.join(self.CSVpath, file))
                        print(file + 'was not valide')

                    else:
                        row_values = [
                            training_id,
                            id_athlete,
                            row[0],
                            row[1],
                            row[2],
                            row[3],
                            row[4],
                            row[5],
                            row[6],
                            row[7],
                            row[8],
                            row[9],
                            row[10],
                        ]

                    # Replace empty strings with None
                    row_values = [None if val == '' else val for val in row_values]

                    all_values.append(row_values)

                self.dbcontroller.insert_many_rows('trainingdata', training_data_columns, all_values)
            #os.remove(os.path.join(self.CSVpath, file))



