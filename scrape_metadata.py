"""
scrape_metadata.py

@author: wronk

Get metadata for list of thesis
"""
from bs4 import BeautifulSoup as BS
import requests
import time
import warnings

html_head = 'https://digital.lib.washington.edu'
theses_page = html_head + '/researchworks/handle/1773/4894/browse'

#
# Get all paper links
#

result = requests.get(theses_page)
result.raise_for_status()  # Error check

soup = BS(result.text, 'lxml')
contents = soup.select("h4 > a")  # get all <a> links in <h4>
thesis_urls = [html_head + child['href'] + '?show=full' for child in contents]

#
# Obtain and store  metadata
#
thesis_list = []
for ui, url in enumerate(thesis_urls):
    res_thesis = requests.get(url)
    res_thesis.raise_for_status()

    soup_thesis = BS(res_thesis.text, 'lxml')
    thesis_rows = soup_thesis.find_all(class_="ds-table-row")

    # TODO: get .pdf link

    # Get extended metadata
    entry_dict = {}
    for row in thesis_rows:
        key = row.find(class_='label-cell').string
        if 'dc.' not in key:
            warnings.warn('key: %s doesn\'t contain `dc`, check scraper' % key)
        entry_dict[key] = row.find(class_='word-break').string

    # Store in list of theses
    thesis_list.append(entry_dict)
    print 'Scraped %i/%i; %s' % (ui + 1, len(thesis_urls),
                                 entry_dict['dc.contributor.author'])

    time.sleep(3)  # Try not to piss off server
