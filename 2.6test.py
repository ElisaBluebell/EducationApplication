import requests
import json
import pandas as pd
URL = ('http://apis.data.go.kr/1262000/OverviewGnrlInfoService/'
        'getOverviewGnrlInfoList?'
        'serviceKey=i2bq%2BzI9klHXoNeB%2BfyUBC2r%2BbMQAQku1fh3TqFSm1CfWLf9KZ04pPvHKQwT6qiRhlZS1ivSQQHi7Rw0Gofetw%3D%3D'
        '&pageNo=1'
        '&numOfRows=10'
        '&returnType=json'
        '&cond[country_nm::EQ]=인도'
        ) # iso 2자리 코드

response = requests.get(URL)
print(response)
r = response.json()
print(r)
print(type(r))

items = r['data']
print(items)
print(items[0])

c_area = [item['area'] for item in items]
c_area_ranking = [item['area_desc'] for item in items]
c_capital = [item['capital'] for item in items]
c_eng_name = [item['country_eng_nm'] for item in items]
c_iso = [item['country_iso_alp2'] for item in items]
c_korea_name = [item['country_nm'] for item in items]
c_ethnic = [item['ethnic'] for item in items]
c_lang = [item['lang'] for item in items]
c_population = [item['population'] for item in items]
c_population_ranking = [item['population_desc'] for item in items]
c_relegion = [item['religion'] for item in items]

c_area = pd.Series(c_area)
c_area_ranking = pd.Series(c_area_ranking)
c_capital = pd.Series(c_capital)
c_eng_name = pd.Series(c_eng_name)
c_iso = pd.Series(c_iso)
c_korea_name = pd.Series(c_korea_name)
c_ethnic = pd.Series(c_ethnic)
c_lang = pd.Series(c_lang)
c_population = pd.Series(c_population)
c_population_ranking = pd.Series(c_population_ranking)
c_relegion = pd.Series(c_relegion)

data_frame = pd.DataFrame({'name_k': c_korea_name,
                    'name_e' : c_eng_name,
                    'iso' : c_iso,
                    'capital': c_capital,
                    'language': c_lang,
                    'ethnic': c_ethnic,
                    'relegion': c_relegion,
                    'population': c_population,
                    'population_rank' : c_population_ranking,
                    'area': c_area,
                    'area_rank': c_area_ranking})

print(data_frame)


def user_request(country):
    URL = ('http://apis.data.go.kr/1262000/OverviewGnrlInfoService/'
        'getOverviewGnrlInfoList?'
        'serviceKey=i2bq%2BzI9klHXoNeB%2BfyUBC2r%2BbMQAQku1fh3TqFSm1CfWLf9KZ04pPvHKQwT6qiRhlZS1ivSQQHi7Rw0Gofetw%3D%3D'
        '&pageNo=1'
        '&numOfRows=10'
        '&returnType=json'
        '&cond[country_nm::EQ]='+country+''
        ) # iso 2자리 코드

    response = requests.get(URL)
    # print(response)
    r = response.json()
    # print(r)
    # print(type(r))

    items = r['data']
    # print(items)
    # print(items[0])

    c_area = [item['area'] for item in items]
    c_area_ranking = [item['area_desc'] for item in items]
    c_capital = [item['capital'] for item in items]
    c_eng_name = [item['country_eng_nm'] for item in items]
    c_iso = [item['country_iso_alp2'] for item in items]
    c_korea_name = [item['country_nm'] for item in items]
    c_ethnic = [item['ethnic'] for item in items]
    c_lang = [item['lang'] for item in items]
    c_population = [item['population'] for item in items]
    c_population_ranking = [item['population_desc'] for item in items]
    c_relegion = [item['religion'] for item in items]

    c_area = pd.Series(c_area)
    c_area_ranking = pd.Series(c_area_ranking)
    c_capital = pd.Series(c_capital)
    c_eng_name = pd.Series(c_eng_name)
    c_iso = pd.Series(c_iso)
    c_korea_name = pd.Series(c_korea_name)
    c_ethnic = pd.Series(c_ethnic)
    c_lang = pd.Series(c_lang)
    c_population = pd.Series(c_population)
    c_population_ranking = pd.Series(c_population_ranking)
    c_relegion = pd.Series(c_relegion)

    data_frame = pd.DataFrame({'name_k': c_korea_name,
                        'name_e' : c_eng_name,
                        'iso' : c_iso,
                        'capital': c_capital,
                        'language': c_lang,
                        'ethnic': c_ethnic,
                        'relegion': c_relegion,
                        'population': c_population,
                        'population_rank' : c_population_ranking,
                        'area': c_area,
                        'area_rank': c_area_ranking})
    
    return data_frame

countryname = input("나라이름을 입력하세요: ")
print(user_request(countryname))