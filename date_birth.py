def get_date_of_birth():
    get_month = input("Enter your birth month(January): ")
    # get_month = 'January'
    get_day = input("Enter your birth day(1): ")
    # get_day = '5'
    get_year = input("Enter your birth year(2000): ")
    # get_year = '2003'
    date_of_birth = f"{get_month} {get_day}, {get_year}"
    return date_of_birth