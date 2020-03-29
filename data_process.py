from utils.data_parser import get_county_geo
import pandas as pd


def make_lower_Case(df_geo, df_covid):
    df_geo['county'] = df_geo['county'].str.lower()
    df_covid['county'] = df_covid['county'].str.lower()
    return df_geo, df_covid


def load_data():
    df_0 = pd.read_csv('data/Geocodes_USA_with_Counties.csv')
    df_1 = pd.read_csv('data/us-counties.csv')
    df_0, df_1 = make_lower_Case(df_0, df_1)
    return df_0, df_1


def process_data():
    df_geo_info, df_covid19 = load_data()
    geo_inf, nulls = get_county_geo(df_geo_info, df_covid19)
    df_geo = pd.DataFrame(geo_inf)
    return df_geo, df_covid19

def data_pipeline():
    df_geo, df_covid19 = process_data()
    df = pd.concat([df_covid19, df_geo], axis=1)
    df = df.drop('fips', axis=1)
    df.to_csv('output/usa_covid19.csv',index=False)

if __name__ == "__main__":
    data_pipeline()