from datetime import datetime as dt


def assertIsDateTime(datetime):
    if isinstance(datetime, dt):
        return

    try:
        dt.strptime(datetime, "%Y-%m-%dT%H:%M:%S")
    except ValueError:
        assert False, 'Date is not parsable'
        raise
