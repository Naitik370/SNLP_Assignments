import re
import pandas as pd

# Define regex patterns for different date formats
patterns = {
    'us_format': r'\b(\d{1,2})[/-](\d{1,2})[/-](\d{2,4})\b',
    'iso_format': r'\b(\d{4})[-/](\d{2})[-/](\d{2})\b',
    'dot_format': r'\b(\d{2})[.](\d{2})[.](\d{2,4})\b',
    'yyyy_mm_dd': r'\b(\d{4})\.(\d{2})\.(\d{2})\b',
    'day': r'\b(\d{1,2})(?:st|nd|rd|th)?\b',
    'month': r'\b(January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\b',
    'year': r'\b(\d{4})\b'
}

month_map = {
    'January': '01', 'February': '02', 'March': '03', 'April': '04', 'May': '05', 'June': '06',
    'July': '07', 'August': '08', 'September': '09', 'October': '10', 'November': '11', 'December': '12',
    'Jan': '01', 'Feb': '02', 'Mar': '03', 'Apr': '04', 'Jun': '06', 'Jul': '07', 'Aug': '08', 'Sep': '09',
    'Oct': '10', 'Nov': '11', 'Dec': '12'
}

data = pd.read_csv('date_parser_testcases.csv')

data = data.drop(50).reset_index(drop=True)
c = 0
for text in data.Input:
    us_match = re.search(patterns['us_format'], text)
    if us_match:
        month, day, year = us_match.groups()
        year = f"20{year.zfill(2)}" if len(year) == 2 else year
        print(f"{day.zfill(2)}/{month.zfill(2)}/{year}")
        continue

    iso_match = re.search(patterns['iso_format'], text)
    if iso_match:
        year, month, day = iso_match.groups()
        print(f"{day}/{month}/{year}")
        continue

    dot_match = re.search(patterns['dot_format'], text)
    if dot_match:
        day, month, year = dot_match.groups()
        year = f"20{year.zfill(2)}" if len(year) == 2 else year
        print(f"{day}/{month}/{year}")
        continue

    yyyy_mm_dd_match = re.search(patterns['yyyy_mm_dd'], text)
    if yyyy_mm_dd_match:
        year, month, day = yyyy_mm_dd_match.groups()
        print(f"{day}/{month}/{year}")
        continue

    day_match = re.search(patterns['day'], text)
    day = day_match.group(1) if day_match else None

    month_match = re.search(patterns['month'], text)
    month = month_map.get(month_match.group(0), None) if month_match else None

    year_match = re.search(patterns['year'], text)
    year = year_match.group(1) if year_match else None

    if day and month and year:
        print(f"{day.zfill(2)}/{month}/{year}")
    else:
        print("Date not found")
