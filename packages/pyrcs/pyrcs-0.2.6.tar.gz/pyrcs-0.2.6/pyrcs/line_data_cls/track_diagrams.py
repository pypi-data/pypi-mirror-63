"""

Data source: http://www.railwaycodes.org.uk

Railway track diagrams (http://www.railwaycodes.org.uk/track/diagrams0.shtm)

"""

import copy
import os
import urllib.parse

import bs4
import pandas as pd
import requests
from pyhelpers.dir import regulate_input_data_dir

from pyrcs.utils import cd_dat, get_last_updated_date


class TrackDiagrams:
    def __init__(self, data_dir=None):
        self.HomeURL = 'http://www.railwaycodes.org.uk'
        self.Name = 'Railway track diagrams'
        self.URL = self.HomeURL + '/track/diagrams0.shtm'

        # Get contents
        source = requests.get(self.URL)
        soup, items = bs4.BeautifulSoup(source.text, 'lxml'), {}
        h3 = soup.find('h3', text=True, attrs={'class': None})
        while h3:
            # Description
            if h3.text == 'Miscellaneous':
                desc = [x.text for x in h3.find_next_siblings('p')]
            else:
                desc = h3.find_next_sibling('p').text.replace('\xa0', '')
            # Extract details
            cold_soup = h3.find_next('div', attrs={'class': 'columns'})
            if cold_soup:
                info = [x.text for x in cold_soup.find_all('p') if x.string != '\xa0']
                urls = [urllib.parse.urljoin(os.path.dirname(self.URL), x['href']) for x in cold_soup.find_all('a')]
            else:
                cold_soup = h3.find_next('a', attrs={'target': '_blank'})
                info, urls = [], []
                while cold_soup:
                    info.append(cold_soup.text)
                    urls.append(urllib.parse.urljoin(os.path.dirname(self.URL), cold_soup['href']))
                    cold_soup = cold_soup.find_next('a') if h3.text == 'Miscellaneous' \
                        else cold_soup.find_next_sibling('a')
            meta = pd.DataFrame(zip(info, urls), columns=['Description', 'FileURL'])
            items.update({h3.text: (desc, meta)})  # Update
            h3 = h3.find_next_sibling('h3')  # Move on
        self.Catalogue = items
        self.Date = get_last_updated_date(self.URL, parsed=True, date_type=False)
        self.DataDir = regulate_input_data_dir(data_dir) if data_dir else cd_dat("line-data", "track_diagrams")
        self.CurrentDataDir = copy.copy(self.DataDir)

    # Change directory to "...dat\\line-data\\track_diagrams\\" and sub-directories
    def cd_td(self, *sub_dir):
        path = self.DataDir
        for x in sub_dir:
            path = os.path.join(path, x)
        return path

    # Change directory to "dat\\line-data\\track_diagrams\\dat" and sub-directories
    def cdd_td(self, *sub_dir):
        path = self.cd_td("dat")
        for x in sub_dir:
            path = os.path.join(path, x)
        return path
