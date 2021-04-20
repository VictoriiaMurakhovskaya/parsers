from urllib import request
from bs4 import BeautifulSoup as BS
import re
import pandas as pd

given_url = 'https://www.otodom.pl/sprzedaz/mieszkanie/mazowieckie/?search%5Bregion_id%5D=7'
sample_apt = 'https://www.otodom.pl/pl/oferta/apartament-z-tarasem-i-widokiem-na-panorame-ID4b16n.html#21655ad6d5'


def get_list(url):
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')
    apt_list = bs.find_all('a', attrs={'data-featured-name': ["listing_no_promo", "promo_top_ads"]})
    return list(set([tag['href'] for tag in apt_list]))


def get_item(url):
    html = request.urlopen(url)
    bs = BS(html.read(), 'html.parser')
    names = bs.find_all('div', attrs={'class': 'css-o4i8bk ev4i3ak2'})
    values = bs.find_all('div', attrs={'class': 'css-1ytkscc ev4i3ak0'})
    res = {n['title']: v['title'] for n, v in zip(names, values)}

    for names, cond in zip(['title', 'address'], [{'class': 'css-46s0sq eu6swcv18'}, {'class': 'css-1qz7z11 e1nbpvi61'}]):
        res.update({names: bs.find(['a', 'h1', 'div', 'strong'], attrs=cond).string})
    for i in ['Cena', 'Cena za metr kwadratowy']:
        res.update({i: bs.find(['h1', 'div', 'strong'], attrs={'aria-label': i}).string})

    return res


if __name__ == '__main__':
    lst = get_list(given_url)
    res = [get_item(item) for item in lst]
    pd.DataFrame(res).to_excel('parsed.xlsx')






