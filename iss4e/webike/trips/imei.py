class IMEI(object):
    def __init__(self, series_selector: str):
        self.series_selector = "" if series_selector == "" else series_selector.split("'")[1]

    def __str__(self):
        return self.series_selector

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.series_selector == other.series_selector
        return NotImplemented

    def __ne__(self, other):
        if isinstance(other, self.__class__):
            return not self == other
        return NotImplemented
