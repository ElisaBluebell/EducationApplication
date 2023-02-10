from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel

a = QTableWidget()
a.currentRow()
a.currentColumn()
a.setItem(0, 0, QTableWidgetItem('11'))

b = QLabel

b.text

# xml_string = st.get_database_from_url('http://openapi.forest.go.kr/openapi/service/cultureInfoService/gdTrailInfoOpenAPI?serviceKey=yn8uwUR3eheqowtPnA9QRTQ9i8mYGhGEetp6HDG1hMhCeH9%2BNJFN6WlIM1AzfgrZB59syoKUT1rAVveE9J6Okg%3D%3D&searchMtNm=&searchArNm=&pageNo=1&numOfRows=100')
# raw_data = st.xml_to_json(xml_string)

# self.mntnm, self.aeatreason, self.overview, self.details = self.get_useful_data(raw_data)
# st.null_to_zero([self.mntnm, self.aeatreason, self.overview, self.details])


# for i in range(len(self.mntnm)):
#     print('length: ', len(self.mntnm))
#     print('i + 1: ', i + 1)
#     print('mntnm: ', self.mntnm[i])
#     print('aeatreason: ', self.aeatreason[i])
#     print('overview: ', self.overview[i])
#     print('details: ', self.details[i])
#     sql = f'''INSERT INTO education_data VALUES({i + 1}, "{self.mntnm[i]}", "{self.aeatreason[i]}", "{self.overview[i]}", "{self.details[i]}")'''
#     st.execute_db(sql)