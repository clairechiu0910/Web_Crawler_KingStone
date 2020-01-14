import collect_data_week as cdw
from datetime import date

start_date = date(2018, 1, 5)
end_date = date(2018, 3, 10)
print(type(start_date))
cdw.collect_data_week("TTTT", "month", start_date, end_date)