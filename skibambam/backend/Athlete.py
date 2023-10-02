from backend.DbController import DbController
class Athelete:
    dbc = DbController()
    def __init__(self, name, first_name, max_hr, rest_hr, vo2max, training_file_tuple):

        if name == '' or first_name == '':
            raise ValueError("please enter a name")
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not isinstance(first_name, str):
            raise TypeError("first_name must be a string")
        if not isinstance(max_hr, int):
            raise TypeError(f"max_hr must be an integer '{type(max_hr)}'")
        if not 0 < max_hr < 300:
            raise ValueError("max_hr must be between 0 and 300")
        if not isinstance(rest_hr, int):
            raise TypeError("rest_hr must be an integer")
        if not 0 < rest_hr < 300:
            raise ValueError("rest_hr must be between 0 and 300")
        if not 0 < rest_hr < max_hr:
            raise ValueError("rest_hr must be between 0 and max_hr")
        if not isinstance(vo2max, float):
            raise TypeError("vo2max must be a float")
        if not 0.0 < vo2max < 100.0:
            raise ValueError("vo2max must be between 0.0 and 100.0")


        self.name = name
        self.first_name = first_name
        self.max_hr = int(max_hr)
        self.rest_hr = int(rest_hr)
        self.vo2max = float(vo2max)

        self.athlete_tuple =(
                self.name,
                self.first_name,
                self.max_hr,
                self.rest_hr,
                self.vo2max
            )



    def full_name(self):
        full_name = f"{self.first_name} {self.name}"
        return full_name

    def save_athelte_to_db(self):
        self.dbc.saveAthelteInDataBase(self.athlete_tuple)


    def get_id_athlete_by_name(self):
        athleteid = self.dbc.getValueByParameter("id_athlete", "athlete", "name", self.name)
        athleteid = [tup[0] for tup in athleteid]
        athleteid = athleteid[0]
        return athleteid




