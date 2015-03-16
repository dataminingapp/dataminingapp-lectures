#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
import time
import argparse
import logging
import requests
from BeautifulSoup import BeautifulSoup


log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
loghandler = logging.StreamHandler(sys.stderr)
loghandler.setFormatter(logging.Formatter("[%(asctime)s] %(message)s"))
log.addHandler(loghandler)

base_url = "http://www.tripadvisor.com/"
user_agent = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.76 Safari/537.36"


parser = argparse.ArgumentParser(description='Scrape tripadvisor')
parser.add_argument('-datadir', type=str,
                    help='Directory to store raw html files',
                    default="data/")
parser.add_argument('-state', type=str,
                    help='State for which the hotel data is required.',
                    required=True)
parser.add_argument('-city', type=str,
                    help='City for which the hotel data is required.',
                    required=True)
args = parser.parse_args()


def get_city_page(city, state):
    """ Returns the URL of the list of the hotels in a city. Corresponds to
    STEP 1 & 2 of the slides.

    Parameters
    ----------
    city : str

    state : str


    Returns
    -------
    url : str
        The relative link to the website with the hotels list.

    """
    # Build the request URL
    url = base_url + "city=" + city + "&state=" + state
    # Request the HTML page
    headers = {'User-Agent': user_agent}
    response = requests.get(url, headers=headers)
    html = response.text.encode('utf-8')
    with open(os.path.join(args.datadir, city + '-tourism-page.html'), "w") as h:
        h.write(html)

    # Use BeautifulSoup to extract the url for the list of hotels in
    # the city and state we are interested in.

    # For example in this case we need to get the following href
    # <li class="hotels twoLines">
    # <a href="/Hotels-g60745-Boston_Massachusetts-Hotels.html" data-trk="hotels_nav">...</a>
    soup = BeautifulSoup(html)
    li = soup.find("li", {"class": "hotels twoLines"})
    city_url = li.find('a', href=True)
    return city_url['href']


def get_hotellist_page(city_url, page_count):
    """ Returns the hotel list HTML. The URL of the list is the result of
    get_city_page(). Also, saves a copy of the HTML to the disk. Corresponds to
    STEP 3 of the slides.

    Parameters
    ----------
    city_url : str
        The relative URL of the hotels in the city we are interested in.
    page_count : int
        The page that we want to fetch.

    Returns
    -------
    html : str
        The HTML of the page with the list of the hotels.
    """
    return ""


def parse_hotellist_page(html):
    """Parses the website with the hotel list and prints the hotel name, the
    number of stars and the number of reviews it has. If there is a next page
    in the hotel list, it returns a list to that page. Otherwise, it exits the
    script. Corresponds to STEP 4 of the slides.

    Parameters
    ----------
    html : str
        The HTML of the website with the hotel list.

    Returns
    -------
    URL : str
        If there is a next page, return a relative link to this page.
        Otherwise, exit the script.
    """
    return ""


if __name__ == "__main__":
    # Get current directory
    current_dir = os.getcwd()
    # Create datadir if does not exist
    if not os.path.exists(os.path.join(current_dir, args.datadir)):
        os.makedirs(os.path.join(current_dir, args.datadir))

    # Get URL to obtaint the list of hotels in a specific city
    city_url = get_city_page(args.city, args.state)
