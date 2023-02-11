import server_tool as st

user_index = []
user_score_data = []

sql = 'SELECT user_index FROM user_account WHERE class="학생";'
user_number = st.execute_db(sql)

for i in range(len(user_number)):
    user_index.append(user_number[i][0])

for i in user_index:
    sql = f'SELECT user_name FROM user_account WHERE user_index={i};'
    user_name = st.execute_db(sql)[0][0]

    sql = f'''
    SELECT SUM(a.correct), 
    SUM(a.solve_datetime), 
    b.area_name 
    FROM score_board AS a 
    INNER JOIN quiz AS b 
    ON a.quiz_index=b.quiz_index 
    WHERE a.user_index={i} 
    GROUP BY b.area_name
    ;'''
    user_score = st.execute_db(sql)
    user_score = list(user_score)
    for j in range(len(user_score)):
        user_score[j] = list(user_score[j])

    st.null_to_zero(user_score)
    user_data = [user_name, user_score]

    user_score_data.append(user_data)
