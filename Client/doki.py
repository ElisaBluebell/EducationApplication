
list = ['["/login_success"', ' [[[1', ' "학생"', ' "박의용"', ' "yuiyong"', ' "1234"', ' 0]]', ' [[1', ' "국내에서 규모가 가장 작은 국립공원으로 남성적인 웅장함을 갖 춘 북쪽의 돌산이 특징이며 명칭은 월출산이다."', ' "O"', ' "전라남도"', ' 10]', ' [2', ' "꽃이 물에 잠긴 것 같다고 하여 수중매라는 별칭으로 불린다. 하늘금만 이쁜게 아니고 억새와 철쭉도 유명한 군립공원이다. 산이름은 황매산이다."', ' "O"', ' "경상남도"', ' 10]', ' [3', ' "북한산은 성채다. 걸출한 암봉들이 험준한 산세를 이 루고 여기 의지하여 사람들이 진짜 성을 쌓았으며 높은 산은 아니지만 주변에 어깨를 겨룰대상이 없어 눈 닿는 곳이면 어디서나 보인다. "', ' "O"', ' "서울/경기"', ' 10]', ' [4', ' "삼국통일의 도장과 대구의 진산이며 경관이 아름답고 도립공원으로 지 정 된 점등을 고려하여 천주교문화의 성지로 유명하며 산 이름은 팔공산이다."', ' "X"', ' "경상북도"', ' 10]', ' [5', ' "속세를 등진 이들의 회심처라고도 불리우며 봉우리들 사이엔 구암폭포', ' 오송폭포가 있고 산명은 속리산이다."', ' "X"', ' "충청북도"', ' 10]', ' [6', ' "용머리가 오종종하니 가운데가 높은 암탉 벼슬처럼 보인다하여 계암이라는 이름이 붙었다.이 산은 영험함 때문에 무속행사 장소로 각광받고있 고 산명은 계암산이다."', ' "X"', ' "충청남도"', ' 10]', ' [7', ' "우리나라 산 중에 제일 높은 산이며 유네스코 세계유산에 지정되어 있고 백록담이라는 유명한 호수가있고 명칭은 한라산이다."', ' "O"', ' "제주도"', ' 10]', ' [8', ' "우리나라에서 "단풍"하면 제일 떠오르는 산이 내장산이다. 아쉽게 호남5대 명산의 국립공원으로 지 정되지는 못했지만 산줄기가 말발굽처럼 둘러쳐져 마치 철옹성 같은 특이지형을 이룬 다."', ' "X"', ' "전라북도"', ' 10]', ' [9', ' "이 산은 섬세한 비경을 두루 갖춘 팔방미인이며 한마디로 한국의 알프스다. 동국여지승람에는 한가위가 내리기 시작한  눈이 하지에 이르러 사라지기 때문에 설악이라 한다는 기록이 있다. 이 산명은 설악산이다."', ' "O"', ' "강원도"', ' 10]]]]']
Jeonnam_quiz = []
Gyeongnam_quiz = []
Seoul_quiz = []
Gyeongbuk_quiz = []
Chungbuk_quiz = [] 
Chungnam_quiz = []
Jeju_quiz = []
Jeonbuk_quiz = []
Gangwon_quiz = []
# print(one)
# list[7]
# list[12]
# 1번문제

for i in range(len(list)):
    if list[i] == ' "전라남도"':
        for j in range(-1, 4):
            Jeonnam_quiz.append(list[i-j])
    if list[i] == ' "경상남도"':
        for j in range(-1, 4):
            Gyeongnam_quiz.append(list[i-j])
    if list[i] == ' "서울/경기"':
        for j in range(-1, 4):
            Seoul_quiz.append(list[i-j])
    if list[i] == ' "경상북도"':
        for j in range(-1, 4):
            Gyeongbuk_quiz.append(list[i-j])
    if list[i] == ' "충청북도"':
        for j in range(-1, 4):
            Chungbuk_quiz.append(list[i-j])
    if list[i] == ' "충청남도"':
        for j in range(-1, 4):
            Chungnam_quiz.append(list[i-j])
    if list[i] == ' "제주도"':
        for j in range(-1, 4):
            Jeju_quiz.append(list[i-j])
    if list[i] == ' "전라북도"':
        for j in range(-1, 4):
            Jeonbuk_quiz.append(list[i-j])
    if list[i] == ' "강원도"':
        for j in range(-1, 4):
            Gangwon_quiz.append(list[i-j])


print(Jeonnam_quiz) # 점수[0] / 지역[1] / 정답[2] / 문제[3] / 문제번호<인덱스>[4]


        # a = list[i-3], list[i-2], list[i-1], list[i], list[i+1]
        # print(a)
        

# for i in range(0, len(list)):
#     if list[i] == '전라남도':
#         print('hi')
    # print(list[10])
    # print(type(list[10]))
# for index, value in enumerate(list, start=1):
#     print(index, value)
#     # if value ==  ' "전라남도"':
#     #     print('hi')

# for index, value in enumerate(list, start=1):
#     # print(index, value)
#     if value ==  ' "전라남도"':
#         a += index
#         if index<12:
#             print(index, value)
    # if a-4<index<a+2:
    #     print(index,value)

        # index-3<=print(value) <=index+1
        
    # elif value ==  ' "경상남도"':
    
    # elif value ==  ' "서울/경기"':
    
    # elif value ==  ' "경상북도"':

    # elif value ==  ' "충청북도"':

    # elif value ==  ' "충청남도"':

    # elif value ==  ' "제주도"':
    
    # elif value ==  ' "전라북도"':

    # elif value ==  ' "강원도"':


#     for i in range(0, , 5):
#         print(index,value)
    # if value == '강원도':
    #     print(index, value)

#     # print(index, value)
#     if 7<index<13:
#         one.append(value)

#     elif 12<index<18:
#         two.append(value)

#     elif 17<index<23:
#         three.append(value)

#     elif 22<index<28:
#         four.append(value)

#     elif 27<index<33:
#         five.append(value)

#     elif 32<index<38:
#         six.append(value)

#     elif 37<index<43:
#         seven.append(value)

#     elif 42<index<48:
#         eight.append(value)

#     elif 47< index<53:
#         nine.append(value)


# print(one)
# print(two)
# print(three)
# print(four)
# print(five)
# print(six)
# print(seven)
# print(eight)
# print(nine)
    #     one.append()
    # elif 12<index<18:
    #     print(index, value)


# for i in list:
#     if 6<i<12:
#         one.append(list[i])

# print(one)

# print(list[3]) # 이름
# print(list[4]) # 아이디
# print(list[6][:-2]) # 포인트 점수

# print(list[7])
# print(list[7][3:]) # 문제번호
# print(list[8]) # 문제
# print(list[9]) # 정답
# print(list[10]) # 지역
# print(list[11][:-1]) # 점수

# print(list[12][2:]) # 문제번호
# print(list[13]) # 문제
# print(list[14]) # 정답
# print(list[15]) # 지역
# print(list[16][:-1]) # 점수

# print(list[17][2:])