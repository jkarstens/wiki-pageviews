from collections import Counter
import urllib.request
import re
import json
import csv
import sys

def write_page_views(article_name, start_year, stop_year, language_codes=[]):
    """Write 'page_views.csv' with daily page views on `article_name` from
    `start_year` (inclusive) to `stop_year` (exclusive). Optionally, specify
    a set of language codes (['en'] for example). If no language codes are
    specified, data will be summed over all existing language codes for
    `article_name`"""

    months = []
    for year in range(start_year, stop_year):
        for month in range(1, 13):
            month_string = str(month)
            if len(month_string) < 2:
                month_string = '0' + month_string
            months.append(str(year) + month_string)

    if language_codes == []:
        with urllib.request.urlopen('http://www.w3schools.com/tags/ref_language_codes.asp') as response:
            page = response.read().decode('utf-8')
            matches = re.findall(r"(<td>[a-z]{2}</td>)", page)
            language_codes = [match[4:6] for match in matches]

    table = Counter()
    for month in months:
        print('grabbing data for ' + month + '...')
        for language_code in language_codes:
            with urllib.request.urlopen('http://stats.grok.se/json/' + language_code + '/' + month + '/' + article_name) as response:
               data = json.loads(response.read().decode('utf-8'))
               for day, views in data['daily_views'].items():
                   table[day] += views

    with open('page_views.csv', 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=['day', 'page views'])
        writer.writeheader()
        for day, views in table.items():
            writer.writerow({'day': day, 'page views': views})

if __name__ == "__main__":
    article_name = sys.argv[1]
    start_year = sys.argv[2]
    stop_year = sys.argv[3]
    language_codes = sys.argv[4] if len(sys.argv) > 4 else []
    write_page_views(article_name, start_year, stop_year, language_codes)
