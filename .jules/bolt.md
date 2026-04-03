## 2024-05-20 - datetime.timedelta vs dateutil.relativedelta
**Learning:** `dateutil.relativedelta.relativedelta` is significantly slower (up to 5x) than the built-in `datetime.timedelta` for simple time offsets like days, hours, and minutes.
**Action:** Always prefer `datetime.timedelta` for offsets unless calculating differences in months or years, which `timedelta` does not support natively.
