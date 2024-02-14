import pyodbc

def insert_data_in_DB(nom_list, num1_list, num2_list, num3_list,num4_list,num5_list,num6_list) :
    dsn = 'tibero_local'
    user = 'sscs'
    password = 'sscs'    
    try:
   
        conn = pyodbc.connect(DSN=dsn, uid=user, pwd=password)
        print("Tibero에 성공적으로 연결되었습니다.")
        cursor = conn.cursor()
        cursor.execute('DELETE FROM SAVE_NUMBER')
        
        for nom,num1,num2,num3,num4,num5,num6 in zip(nom_list, num1_list, num2_list, num3_list,num4_list,num5_list,num6_list) :
            cursor.execute('INSERT INTO SAVE_NUMBER(nom, num1,num2,num3,num4,num5,num6) VALUES(?,?,?,?,?,?,?)',
                        (nom,num1,num2,num3,num4,num5,num6))   
        cursor.commit()
        print("작업 종료")
    except Exception as e:
        print("error " + str(e))
        
        
if __name__ == "__main__" : 
    file_path = 'E:\Test_Simple_Python\lotto_num.txt'
    
    nom_list = []
    num1_list = []
    num2_list = []
    num3_list = []
    num4_list = []
    num5_list = []
    num6_list = []
    bonus_list = []
    
    with open(file_path,'r',  encoding='utf-8') as fd :
        for line in fd :
            line = line.replace('\t', ' ')
            line = line.strip()  # 줄바꿈 문자 제거
            elements = line.split(' ')
            nom_list.append(int(elements[0]))
            num1_list.append(int(elements[2]))
            num2_list.append(int(elements[3]))
            num3_list.append(int(elements[4]))
            num4_list.append(int(elements[5]))
            num5_list.append(int(elements[6]))
            num6_list.append(int(elements[7]))
    insert_data_in_DB(nom_list, num1_list, num2_list, num3_list,num4_list,num5_list,num6_list)      
            
            