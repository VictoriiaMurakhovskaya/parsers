from selenium import webdriver
import pandas as pd

given_url = 'https://www.otodom.pl/sprzedaz/mieszkanie/mazowieckie/?search%5Bregion_id%5D=7'

chromedriver = r'chromedriver.exe'
options = webdriver.ChromeOptions()
options.add_argument('headless')  # для открытия headless-браузера
driver = webdriver.Chrome(executable_path=chromedriver, options=options)


def get_list(url):
    driver.get(url)
    content = driver.find_elements_by_xpath("//a[@data-featured-name='listing_no_promo']") + \
              driver.find_elements_by_xpath("//a[@data-featured-name='promo_top_ads']")

    return list(set([item.get_attribute('href') for item in content]))


def get_item(url):
    driver.get(url)

    names  = [item.get_attribute('title')
              for item in driver.find_elements_by_xpath("//div[@class='css-o4i8bk ev4i3ak2']")]
    values = [item.get_attribute('title')
              for item in driver.find_elements_by_xpath("//div[@class='css-1ytkscc ev4i3ak0']")]
    res = {n: v for n, v in zip(names, values)}
    for name, xpath in zip(['title', 'address', 'Cena', 'Cena za metr kwadratowy'],
                           ["//h1[@data-cy='adPageAdTitle']", "//a[@class='css-1qz7z11 e1nbpvi61']",
                            "//strong[@aria-label='Cena']", "//div[@aria-label='Cena za metr kwadratowy']", ]):
        content = driver.find_elements_by_xpath(xpath)
        if content:
            res.update({name: content[0].text})

    return res


if __name__ == '__main__':
    lst = get_list(given_url)
    res = [get_item(item) for item in lst]
    pd.DataFrame(res).to_excel('parsed_sl.xlsx')



