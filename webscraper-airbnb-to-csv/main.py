from bs4 import BeautifulSoup
import requests
import pandas as pd

"""
Webscraping project: Getting all listing (with Requests) from Airbnb in India
Results include: Name of listing, description, old price, original price and star reviews
Saving results to a CSV file
"""

# Airbnb URL to get
url = 'https://www.airbnb.com/s/India/homes?adults=1&tab_id=home_tab&refinement_paths%5B%5D=%2Fhomes&query=India' \
      '&place_id=ChIJkbeSa_BfYzARphNChaFPjNc&flexible_trip_lengths%5B%5D=one_week&price_filter_input_type=0' \
      '&price_filter_num_nights=5&channel=EXPLORE&search_type=user_map_move&ne_lat=59.139778890987905&ne_lng=93' \
      '.6332587156628&sw_lat=4.84557715667748&sw_lng=52.15767331460464&zoom=4&zoom_level=4&search_by_map=true'

r = (requests.get(url)).content

soup = BeautifulSoup(r, 'html.parser')

# Results are written to empty list Houses
houses = []

# Loop from page 1 to page 15 of Airbnb
for i in range(1, 16):

    # Webscraping html
    div = soup.find('div', class_='gh7uyir giajdwt g14v8520 dir dir-ltr')
    div_card = div.find_all('div', class_='g1qv1ctd cb4nyux dir dir-ltr')

    for item in div_card:

        # Every loop sabes the item result to a dictionary
        dict_house = {}

        name = item.find('div', class_='t1jojoys dir dir-ltr').string
        description = item.find('span', class_='t6mzqp7 dir dir-ltr').string
        list_price = item.find('span', class_='a8jt5op dir dir-ltr').string
        price = list_price.split()
        original_price = ''
        if len(price) == 7:
            old_price = float(price[1])
            original_price = float(price[6])
        else:
            old_price = float(price[1])
            original_price = old_price

        stars = item.find('span', class_='t5eq1io r4a59j5 dir dir-ltr')

        if stars is not None:
            stars = ((stars['aria-label']).split())[0]
        else:
            stars = 'No Review'

        # Dictionary
        dict_house = {'page': i, 'name': name, 'description': description, 'old_price': old_price,
                      'original_price': original_price, 'stars': stars}

        # Adding the dictionary to a list
        houses.append(dict_house)

    # Getting the link for the next page
    before_np = soup.find('a', class_='l1j9v1wn c1ytbx3a dir dir-ltr')
    np = before_np.find('href')

    # If to verify if next page exists. If not, stop running
    if np is not None:
        cnp = 'https://www.airbnb.com' + np.get('href')

        url = str(cnp)

        r = (requests.get(url)).content

        soup = BeautifulSoup(r, 'html.parser')
    else:
        print('stop')

# Using Pandas to save results to a CSV
data_frame = pd.DataFrame.from_dict(houses)
data_frame.to_csv('airbnb_stays.csv')
