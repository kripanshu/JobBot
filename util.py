import datetime

class Util(object):

    def __init__(self):
        """utilities class"""

    @staticmethod
    def conver_to_date(gmailDate):
        s = gmailDate / 1000.0
        new_date = datetime.datetime.fromtimestamp(s).strftime('%Y-%m-%d %H:%M:%S.%f')
        return new_date
