from datetime import datetime

def format_datetime(date_str):
        if date_str and date_str != "N/A":
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
                return dt.strftime("%d-%m-%Y %H:%M")
            except ValueError:
                return date_str
        return "N/A"