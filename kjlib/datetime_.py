from datetime import datetime
import re
import time

def sql_date_to_datetime(sql_date):
	if not re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}", sql_date):
		raise ValueError("%r is not a valid sql_date" % sql_date)
	date = time.strptime(sql_date, "%Y-%m-%d %H:%M")
	date = datetime.fromtimestamp(time.mktime(date))
	return date

def datetime_to_sql_date(date_):
	return date_.strftime("%Y-%m-%d %H:%M")