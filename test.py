from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QLabel, QWidget, QPushButton, QApplication
import sys

# a = QTableWidget()
# a.currentRow()
# a.currentColumn()
# a.setItem(0, 0, QTableWidgetItem('11'))
#
# b = QLabel
#
# b.text

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

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.o_btn = QPushButton(self)
        self.x_btn = QPushButton(self)
        self.o_btn.setText('o')
        self.x_btn.setText('x')
        self.o_btn.setGeometry(20, 20, 20, 20)
        self.x_btn.setGeometry(40, 40, 20, 20)
        self.setGeometry(0, 0, 400, 400)
        self.o_btn.clicked.connect(self.change_to_o)
        self.x_btn.clicked.connect(self.change_to_x)
        self.a = ''

    def change_to_o(self):
        self.a = 'o'
        print('self.a: ', self.a)

    def change_to_x(self):
        self.a = 'x'
        print('self.a: ', self.a)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Window()
    window.show()
    app.exec_()
