

def convert_to_decimal(sexagesimal_geo_cords: str):
    """
    coverts geo coordinates from sexagesimal format to decimal format
    """
    s = sexagesimal_geo_cords
    degree = float(s[s.find("'")+len("'"):s.rfind('°')])
    minute = float(s[s.find('°')+len('°'):s.rfind('′')])
    sec = float(s[s.find("′")+len("′"):s.rfind('″')])
    return degree + (minute / 60) + (sec / 3600)