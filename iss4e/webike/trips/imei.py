class IMEI(object):
    def __init__(self, series_selector:str):
        self.series_selector = series_selector

    def __str__(self):
        return self.series_selector.split("'")[1]
