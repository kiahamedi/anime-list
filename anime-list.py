#!/usr/bin/python3

from os import system
import requests
from bs4 import BeautifulSoup


def script_info():
    asci_name = """
    _          _                  _     _     _
   / \   _ __ (_)_ __ ___   ___  | |   (_)___| |_
  / _ \ | '_ \| | '_ ` _ \ / _ \ | |   | / __| __|
 / ___ \| | | | | | | | | |  __/ | |___| \__ \ |_
/_/   \_\_| |_|_|_| |_| |_|\___| |_____|_|___/\__|

                                        v 1.0 - beta
"""

    print(asci_name)

# get anime from page
def get_page(page):
    lists = 50 * page
    list_url = "https://myanimelist.net/topanime.php?type=movie&limit=%s" % (lists)
    list_page = requests.get(list_url)
    soup = BeautifulSoup(list_page.content,'html5lib')
    titles = soup.find_all('h3',{"class":"hoverinfo_trigger fl-l fs14 fw-b anime_ranking_h3"})
    title_list = []
    url_list = []

    for t in titles:
        title = t.find('a').text
        href = t.find('a')['href']
        title_list.append(title)
        url_list.append(href)

    return title_list, url_list

# get details page with url
def get_page_details(url):
    page_content = requests.get(url)
    soup = BeautifulSoup(page_content.content,'html5lib')

    # get score
    td = soup.find('td',{"valign":"top"})
    all_div_td = td.find_all('div')
    div_score = soup.find('div', {"data-title": "score"})
    div_score_label = div_score.find('div')
    score = div_score_label.text

    # get trailer
    iframe = soup.find('a',{"class": "iframe js-fancybox-video video-unit promotion"})
    trailer = iframe['href']

    # get description
    description = soup.find('p',{"itemprop": "description"}).text

    # get image
    image_td = soup.find('td',{"class": "borderClass"})
    img = image_td.find('img')['data-src']

    return score, description, trailer, img


def main():
    print('\033[H\033[J', end='')
    # show asci name
    script_info()
    user_page = int(input("Enter page: "))
    print('\033[H\033[J', end='')
    print("================ Page %s ================" % (user_page))
    anime = []
    url = []
    anime, url = get_page(user_page)
    cnt = 1
    for anim in anime:
        print(cnt, anim)
        cnt += 1
    print("================ Selecte Anime ================")
    selected_anime = int(input("Number of anime: "))
    print('\033[H\033[J', end='')
    print("================ %s Details ================" % (anime[selected_anime-1]))
    user_anime_title = anime[selected_anime-1]
    user_anime_score, user_anime_description, user_anime_trailer, user_anime_img = get_page_details(url[selected_anime-1])
    print("Score -> " + user_anime_score)
    print("Description:", user_anime_description)

    return user_anime_img, user_anime_trailer

user_anime_img, user_anime_trailer = main()

while True:
    print("\n")
    print("================ Control ================")
    print("[1] : view cover")
    print("[2] : view trailer")
    print("[3] : back to home")
    print("[4] : exit")
    selected_control = int(input("Select control: "))
    if selected_control == 1:
        system("feh %s" % (user_anime_img))
    elif selected_control == 2:
        system("mpv %s" % (user_anime_trailer))
    elif selected_control == 3:
        user_anime_img, user_anime_trailer = main()
    elif selected_control == 4:
        break
