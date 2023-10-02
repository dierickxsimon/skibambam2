import pandas as pd
import datetime
from backend.CalculateTL import CalculateTL
from backend.DbController import DbController
from backend.CalculateTL import CalculateTL

class CalculateEdwardsTrimp:
    def EdwardsTRIMP(self, athleteid):
        dbc = DbController()
        calculatetl = CalculateTL()

        athletevalues = dbc.getAthletesValues(athleteid)
        maxhr = athletevalues["max_hr"]

        dflist = calculatetl.getdfofHR(athleteid)

        valuelist = []

        for df in dflist:
            EdwardTRIMP = []
            for Hr, td in zip(df["heart_rate"], df["timedelta"]):
                if td == None:
                    pass
                elif 0.01 * maxhr < Hr <= 0.6 * maxhr:
                    EdwardTRIMP.append(td * 1)
                elif 0.6 * maxhr < Hr <= 0.7 * maxhr:
                    EdwardTRIMP.append(td * 2)
                elif 0.7 * maxhr < Hr <= 0.8 * maxhr:
                    EdwardTRIMP.append(td * 3)
                elif 0.8 * maxhr < Hr <= 0.9 * maxhr:
                    EdwardTRIMP.append(td * 4)
                elif Hr > 0.9 * maxhr:
                    EdwardTRIMP.append(td * 5)
                else:
                    print('*' * 100, "er klop iets niet met de Edward Trimp")

            df["edwardtrimp"] = EdwardTRIMP
            sessionTRIMP = df["edwardtrimp"].sum()
            sessionTRIMP = sessionTRIMP.total_seconds()
            sessionTRIMP = float(sessionTRIMP)
            id_training = int(df["id_training"].iloc[0])
            nameTL = "eTRIMP"
            idtrainingloadtypes = [tup[0] for tup in
                                   dbc.getValueByParameter("id_trainingloadtypes", "trainingloadtypes", "name", nameTL)]

            idtrainingloadtypes = idtrainingloadtypes[0]

            values = [id_training, idtrainingloadtypes, sessionTRIMP]
            valuelist.append(values)

        columns = ["id_training", "id_trainingloadtypes", "tlvalue"]
        table = "trainingload"

        dbc.insert_many_rows(table, columns, valuelist)

