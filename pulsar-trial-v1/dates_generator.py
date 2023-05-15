from datetime import date, timedelta

def generate_dates():
    start_date = date(2022, 1, 1)
    end_date = date(2022, 12, 31)

    # Calculate the total number of days
    total_days = (end_date - start_date).days + 1

    # Generate the array of dates
    return [start_date + timedelta(days=i) for i in range(total_days)]