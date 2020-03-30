from utils.geo_parser import get_county_geo
from utils.date_process import process_missing_dates
from collections import defaultdict
from typing import List, Dict
import pandas as pd


def make_lower_case(df_geo: pd.DataFrame, df_covid: pd.DataFrame):
    df_geo['county'] = df_geo['county'].str.lower()
    df_covid['county'] = df_covid['county'].str.lower()
    return df_geo, df_covid


def get_earliest_event(df: pd.DataFrame, county: str, state: str):
    grouped_df = df.query(f"county == '{county}'").query(f"state == '{state}'")
    return grouped_df


def _merge_dicts(records: List[Dict]):
    merged_dict = defaultdict(list)
    for county_record in records:
        for k, values in county_record.items():
            for value in values:
                merged_dict[k].append(value)
    return merged_dict


def create_df(df_raw: pd.DataFrame):
    df = df_raw
    df_set = df.drop_duplicates(subset=['state', 'county'], keep='first')
    county_state_set = list(zip(df_set.county.to_list(), df_set.state.to_list()))
    all_county_records = []
    for county, state in county_state_set:
        county = county.replace("'", "")
        df_county = get_earliest_event(df_set, county, state)
        if not df_county.empty:
            county_record_dict = process_missing_dates(df, df_county, "2020-01-21")
            all_county_records.append(county_record_dict)
    all_records = _merge_dicts(all_county_records)
    return pd.DataFrame(all_records)


def load_data():
    df_0 = pd.read_csv('data/Geocodes_USA_with_Counties.csv')
    df_1 = pd.read_csv('data/us-counties.csv')
    df_0, df_1 = make_lower_case(df_0, df_1)
    return df_0, df_1


def process_data():
    df_geo_info, df_covid19 = load_data()
    geo_inf, nulls = get_county_geo(df_geo_info, df_covid19)
    df_geo = pd.DataFrame(geo_inf)
    return df_geo, df_covid19, nulls


def data_pipeline():
    df_geo, df_covid19, nulls = process_data()
    # concat the geo-cords columns with covid stats
    df = pd.concat([df_covid19, df_geo], axis=1)
    df = df.drop('fips', axis=1)
    df = create_df(df)
    df.to_csv('output/usa_covid19.csv', index=False)


if __name__ == "__main__":
    data_pipeline()
