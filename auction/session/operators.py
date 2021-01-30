import pandas as pd
import urllib

from auction.session.client import Client


class Interencheres:
    BASE_URL = 'https://www.interencheres.com'
    SEARCH_URL = '/recherche/lots?search='

    def __init__(self, item: str):
        """Get results for a searches

        Args:
            item (str): Item to search
        """
        self.client = Client()
        self.url = self.BASE_URL + self.SEARCH_URL + urllib.parse.quote(item)
        self.soup = self.client.run(self.url, True, True)

    def transform(self) -> pd.DataFrame:
        """Transform the soup response into a panda dataframe

        Returns:
            pd.DataFrame: Pandas dataframe containing :
                - item description
                - item date
                - item number
                - item price estimation
                - link to the item
        """
        items = self.soup.find('div', class_='results') \
            .find('div', class_='row--dense') \
            .find_all('div', class_='col-sm-6')
        lst = []
        for div in items:
            dt = div.find_all('div', class_='estimates')[1]
            if dt:
                dt = dt.text.replace('  ', '')
            link = self.BASE_URL + div.find('a')['href']
            description = div.find(
                'div',
                class_='description').text.replace('  ', '').replace('\n', '')
            estimation = div.find('div', class_='estimates')
            if estimation:
                estimation = estimation.text.replace('  ', '')
            lst += [(description, dt, estimation, link)]
        return pd.DataFrame(
            lst,
            columns=[
                'item',
                'date',
                'estimation',
                'link'])


class Drouot:
    BASE_URL = 'https://www.drouotonline.com'
    SEARCH_URL = '/recherche/lots?query='

    def __init__(self, item: str):
        """Get results for a searches

        Args:
            item (str): Item to search
        """
        self.client = Client()
        self.url = self.BASE_URL + self.SEARCH_URL
        self.url += urllib.parse.quote_plus(item)
        self.soup = self.client.run(self.url, False, False)

        # They have pages and not infinite scroll down
        self.nb_items = self.soup.find('div', class_='toolbar') \
            .find('h4').text.replace('\n', '').replace('  ', '')
        self.nb_items = int(self.nb_items[:self.nb_items.find('résultats')])

        # Iterate trought pages
        self.soups = []
        for i in range(0, self.nb_items, 50):
            url = self.url + f"&max=50&offset={i}"
            if i == max(range(0, self.nb_items, 50)):
                self.soups.append(self.client.run(url, False, True))
            else:
                self.soups.append(self.client.run(url, False, False))

    def transform(self) -> pd.DataFrame:
        """Transform the soup response into a panda dataframe

        Returns:
            pd.DataFrame: Pandas dataframe containing :
                - item description
                - item date
                - item number
                - item price estimation
                - link to the item
        """
        dfs = []
        for soup in self.soups:
            items = soup.find('div', id='list-lots') \
                .find_all('div', class_='lot vsListe')
            lst = []
            for div in items:
                link = str(
                    div.find(
                        'div',
                        class_='blog-page').find_all('a')[1])
                link = link[6 + link.find('href="'):link.find('?')]
                link = self.BASE_URL + link
                dt = div.find(
                    'div',
                    class_='infoDateListe').text.replace(
                        "\n",
                        "").replace('  ', '')
                description = div.find(
                    'div',
                    class_='product-cell').find('h5').text.replace(
                        "\n",
                        "").replace('  ', '')
                estimation = div.find('h5', class_='Estimation')
                if estimation:
                    estimation = estimation.text.replace(
                        "\n",
                        "").replace('  ', '')
                lst += [(description, dt, estimation, link)]
            dfs.append(
                pd.DataFrame(
                    lst,
                    columns=[
                        'item',
                        'date',
                        'estimation',
                        'link']))
        return pd.concat(dfs)
