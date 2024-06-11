import csv

def read_csv_as_dicts(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        data = [row for row in reader]
    return data

def wrangle_country(country):
    country_codes = read_csv_as_dicts('data/country-codes.csv')
    return {
        **country,
        "iso": next((code["ISO"] for code in country_codes if code["IOC"] == country["country_code"]), None),
        "gold": int(country["gold"]),
        "silver": int(country["silver"]),
        "bronze": int(country["bronze"]),
        "total": int(country["total"]),
    }

def get_country_data():
    # See https://www.olympedia.org/statistics/medal/country
    file_path = 'data/olympic_medal_counts.csv'
    data = read_csv_as_dicts(file_path)

    countries = [wrangle_country(d) for d in data]
    countries = [c for c in countries if c["iso"] is not None]

    return countries



