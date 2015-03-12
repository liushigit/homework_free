def year_day(day):
    return day.timetuple().tm_yday
    
def date_format(day, splitter):
    return splitter.join(day.isoformat().split('-'))
    
# 
if __name__ == "__main__":
    import datetime
    print date_format(datetime.date.today(), '.')
