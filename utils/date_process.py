import pandas as pd
from datetime import timedelta, date, datetime
import logging

def _split_dates(dates: str):
    splits = dates.split('-')
    year = int(splits[0])
    month = int(splits[1])
    date = int(splits[2])
    sdate = datetime(year, month, date)
    return sdate


def _daterange(date1, date2):
    for n in range(int ((date2 - date1).days)):
        yield date1 + timedelta(n)


def _extract_points(county_first_occurance: pd.DataFrame):
    f_date = county_first_occurance['date'].to_list()[0]
    county = county_first_occurance['county'].to_list()[0]
    state = county_first_occurance['state'].to_list()[0]
    latitude = county_first_occurance['latitude'].to_list()[0]
    longitude = county_first_occurance['longitude'].to_list()[0]
    return f_date, county, state, latitude, longitude


def _add_missing_dates(start_dt, end_dt):
    dates = []
    for dt in _daterange(start_dt, end_dt):
        dates.append(dt.strftime("%Y-%m-%d"))
    return dates


def _get_existing_records(df: pd.DataFrame, county: str, state: str):
    df = df.query(f"state == '{state}'").query(f"county == '{county}'")
    neo_df_dict = {'date': [], 'county': [], 'state': [],
                   'cases': [], 'deaths': [],
                   'latitude': [], 'longitude': []}
    if not df.empty:
        df_dict = df.to_dict()
        zeroth_index = list(df_dict['date'].keys())[0]
        cols = ['date', 'county', 'state', 'cases', 'deaths', 'latitude', 'longitude']

        curr_ptr = -1
        for k, v in df_dict.items():
            for kk, vv in v.items():
                if kk == zeroth_index:
                    curr_ptr+=1
                neo_df_dict[cols[curr_ptr]].append(vv)
    else:
        logging.warning(f"Something wrong with {county}, {state}")
    return neo_df_dict


def process_missing_dates(df: pd.DataFrame, county_first_occurance: pd.DataFrame, lower_bound_date: str):
    f_date, county, state, latitude, longitude = _extract_points(county_first_occurance)
    record_dict = _get_existing_records(df, county, state)
    sdate_start = _split_dates(lower_bound_date)
    sdate_end = _split_dates(f_date)

    missing_dates = _add_missing_dates(sdate_start, sdate_end)
    county = [county for _ in range(len(missing_dates))]
    state = [state for _ in range(len(missing_dates))]
    cases = [0 for _ in range(len(missing_dates))]
    deaths = [0 for _ in range(len(missing_dates))]
    latitude = [latitude for _ in range(len(missing_dates))]
    longitude = [longitude for _ in range(len(missing_dates))]

    record_dict['date'] = missing_dates + record_dict['date']
    record_dict['county'] = county + record_dict['county']
    record_dict['state'] = state + record_dict['state']
    record_dict['cases'] = cases + record_dict['cases']
    record_dict['deaths'] = deaths + record_dict['deaths']
    record_dict['latitude'] = latitude + record_dict['latitude']
    record_dict['longitude'] = longitude + record_dict['longitude']

    return record_dict


