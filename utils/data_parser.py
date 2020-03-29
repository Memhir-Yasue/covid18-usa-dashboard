from data.us_state_abbrev import us_state_abbrev
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
import logging


def get_node_info(node: pd.Series):
    return 0


def not_empty(df_query_result: pd.DataFrame):
    if not df_query_result.empty:
        return True
    return False


def correct_nulls(county: str):
    if county == "new york city":
        return 'new york'
    else:
        return county

def format(county: str):
    county = correct_nulls(county)
    county = county.replace("'", "")
    return county

def get_county_geo(df_geo: pd.DataFrame, df_cvd19: pd.DataFrame):
    """
    Extract county geo-coordinates based on the city with largest population
    :param df_geo:
    :param df_cvd19:
    :return:
    """
    state_to_county = list(zip(df_cvd19['state'],df_cvd19['county']))
    data = {'latitude': [], 'longitude': []}
    data_null = {}
    for k, v in state_to_county:
        state = us_state_abbrev[k]
        v = format(v)
        county_info = (df_geo.query(f"state == '{state}' ")).query(f"county == '{v}' ")
        if not_empty(county_info):
            # select the city with the largest population as a geo-spatial node
            populations = county_info['estimated_population']
            index = county_info.index[populations == populations.max()][0]
            node = county_info.loc[index]
            data['latitude'].append(node.latitude)
            data['longitude'].append(node.latitude)
        else:
            logging.warning(f"Problem with {v}, {k}\nAppending to null island")
            data['latitude'].append(0)
            data['longitude'].append(0)
            if k not in data_null:
                data_null[k] = {}
                data_null[k][v] = 1
            elif k in data_null:
                if v not in data_null[k]:
                    data_null[k][v] = 1
                else:
                    data_null[k][v] += 1

    return data, data_null


def get_county_seat(county: str, state: str):
    """
    Extract county info (such as population from wikipedia
    :param county:
    :param state:
    :return:
    """
    url = f'https://en.wikipedia.org/wiki/{county}_county,_{state}'
    data = urlopen(url)
    soup = BeautifulSoup(data, 'html.parser')
    return 0


def get_geo_cords(county: str, state: str):
    """
    Extract geo cords of county
    :param county:
    :param state:
    :return:
    """
    try:
        url = f'https://en.wikipedia.org/wiki/{county}_county,_{state}'
        data = urlopen(url)
        soup = BeautifulSoup(data, 'html.parser')
        lat = soup.find('span', {'class': 'latitude'})
        long = soup.find('span', {'class': 'longitude'})
        return lat.get_text(), long.get_text()
    except Exception as e:
        raise Warning (f"Geo coordinates could not be extracted due to Exception {e}")



