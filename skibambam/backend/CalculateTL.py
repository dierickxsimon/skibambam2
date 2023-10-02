import pandas as pd
from backend.DbController import DbController

class CalculateTL:
    def __init__(self):
        self._dflist = []
        self.dbc = DbController()


    def getdfofHR(self, athleteid):
        columns = ("timestamp, heart_rate")
        trainingid = [tup[0] for tup in
                      self.dbc.getValueByParameter("id_training", "training", "id_athlete", athleteid)]
        for id in trainingid:
            data = self.dbc.getValueByParameter(columns, "trainingdata", "id_training", id)

            df = pd.DataFrame(data, columns=["timestamp", "heart_rate"])
            df["timedelta"] = df["timestamp"].diff()
            df['seconds'] = df['timedelta'] / pd.Timedelta(seconds=1)
            df["id_training"] = id
            self._dflist.append(df)
        return self._dflist




