class Fillable:

    def __init__(self, dictionary):
        for key in dictionary:
            setattr(self, "_" + key, dictionary[key])
