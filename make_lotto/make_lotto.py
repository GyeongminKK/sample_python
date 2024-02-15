import sys
import pyodbc
import random
import itertools
from collections import Counter

def conn_db():
    dsn = 'tibero_local'
    user = 'sscs'
    pwd = 'sscs'
    conn = pyodbc.connect(DSN=dsn, uid=user, pwd=pwd)
    return conn    

def get_count(conn) :
    sql = f'SELECT COUNT(*), MAX(nom), MIN(nom) from SAVE_NUMBER'
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()    
    count = result[0][0]
    max_nom = result[0][1]
    min_nom = result[0][2]    
    cursor.close()
    return count, max_nom, min_nom

def get_num(conn, where_num):
    sql = f'SELECT num1,num2,num3,num4,num5,num6 from SAVE_NUMBER where nom >= {where_num}'
    cursor = conn.cursor()    
    cursor.execute(sql)
    result = cursor.fetchall()
    cursor.close()
    conn.close()
    return result

def get_result(number_list):
    # number_list를 하나의 리스트로 펼치기
    flattened_list = list(itertools.chain.from_iterable(number_list))

    # 각 숫자의 등장 횟수 계산
    number_counts = Counter(flattened_list)

    # 총 숫자의 갯수
    total_count = len(number_list) * 6

    # 각 숫자의 등장 확률 계산하여 number_counts에 저장
    probability_dict = {}
    for num in range(1, 46):
        probability = number_counts[num] / total_count * 100
        probability_dict[num] = round(probability, 3)

    # 각 숫자의 등장 확률을 누적 확률로 변환
    cumulative_probabilities = {}
    cumulative_prob = 0
    for num, probability in probability_dict.items():
        cumulative_prob += probability
        cumulative_probabilities[num] = cumulative_prob
        
    combinations = []
    
    # 10번의 조합 생성
    for _ in range(10):
        selected_numbers = set()  # 중복을 허용하지 않는 세트 생성
        while len(selected_numbers) < 6:  # 6개의 숫자를 선택할 때까지 반복
            rand = random.uniform(0, 100)
            selected_num = next((num for num, prob in cumulative_probabilities.items() if prob >= rand), None)
            if selected_num is not None:
                selected_numbers.add(selected_num)  # 세트에 중복되지 않게 추가
        combinations.append(sorted(selected_numbers))  # 정렬된 숫자를 리스트에 추가

    # 결과 출력
    for idx, combination in enumerate(combinations, start=1):
        print(f"조합 {idx}: {combination}")
    
if __name__ == "__main__" : 
    # DB 연결
    conn = conn_db()
    # 현재 등록된 회차 정보 조회
    count, max, min = get_count(conn)
    print(f"총 회차 : {int(count)} ({max}회차 ~ {min}회차)")
    # 차수 입력
    user_num = input("몇 개 차수를 기준? ")
    print("")
    where_num = int(max) - int(user_num) + 1
    print(f"{max} ~ {where_num} 회차 분석 진행 ")
    number_list = get_num(conn, where_num)
    get_result(number_list)
  