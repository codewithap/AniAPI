from requests import get
from bs4 import BeautifulSoup
import json
import time

class gogoscrapper:
    def __init__(self):
        self.gogoUrls = ('https://www4.gogoanimes.fi',
                        'http://gogoanime3.net')
        self.apis = ('https://ajax.gogo-load.com',
                    'https://ajax.gogocdn.net',
                    'https://ajax.apimovie.xyz')

    def search(self, q):
        for url in self.apis:
            try:
                response = get(url+f"/site/loadAjaxSearch?keyword={q}")
                if response.status_code == 200:
                    return json.loads(response.content)["content"]
            except:
                pass
    
    def getEpis(self,q):
        anime = self.search(q)
        soup = BeautifulSoup(str(anime), "html.parser")
        link = soup.select("a")[0]["href"]
        gogoId = self.getId(link)
        for api in self.apis:
            epurl = f"{api}/ajax/load-list-episode?ep_start=0&ep_end=9999&id={gogoId}"
            response = get(epurl)
            if response.status_code == 200:
                epsoup = BeautifulSoup(response.content, "html.parser")
                epis = [x["href"] for x in epsoup.select("a")][::-1]
                return epis

    def getId(self, link):
        for url in self.gogoUrls:
            try:
                response = get(f"{url}/{link}")
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, "html.parser")
                    id = soup.select("input#movie_id")[0]["value"]
                    return id
            except:
                pass

