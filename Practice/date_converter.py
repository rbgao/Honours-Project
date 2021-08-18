from datetime import datetime

dates_SMP = []

def date_converter_SMP(date_list): 
    for date in date_list:
            sep = '– ' 
            date_only = date.split(sep, 1)[-1]
            converted_date = datetime.strptime(date_only, '%B %Y')
            dates_SMP.append(converted_date)
    return dates_SMP

dates_minutes = []

def date_converter_minutes(date_list):
    for date in date_list:
        location_date = date.replace(u'\xa0', ' ')
        sep = '– ' 
        sep1 = "- "
        date_only = location_date.split(sep, 1)[-1]
        date_only = date_only.split(sep1, 1)[-1]
        converted_date = datetime.strptime(date_only, '%d %B %Y')
        dates_minutes.append(converted_date)
    return dates_minutes