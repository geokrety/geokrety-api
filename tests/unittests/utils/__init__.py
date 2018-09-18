from datetime import datetime


def assertIsDateTime(date_time):
    if isinstance(date_time, datetime):
        return

    try:
        datetime.strptime(date_time, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        assert False, 'Date is not parsable'
        raise
