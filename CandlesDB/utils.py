import datetime as dt


def is_stale(date, threshold: int, ref_date: str = "") -> bool:
    _format = "%Y-%m-%d"
    if isinstance(date, str):
        date = dt.datetime.strptime(date, _format).date()

    if ref_date == "":
        ref_date = dt.datetime.now().date()
    else:
        if isinstance(ref_date, str):
            ref_date = dt.datetime.strptime(ref_date, _format).date()

    delta = ref_date - date
    delta = delta.days

    if delta > threshold:
        return True
    else:
        return False
