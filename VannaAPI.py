import time

import vanna
import pandas as pd
import mysql.connector
from vanna.remote import VannaDefault
import sys
from io import StringIO
import json
import re


def VannaGetSql(words):
    api_key = '56651f10131246a6b634d7f5d5564f70'
    vanna_model_name = 'answhite'
    vn = VannaDefault(model=vanna_model_name, api_key=api_key)
    # vn.train(ddl="""
    # DROP TABLE IF EXISTS `student`;
    # CREATE TABLE `student_info`  (
    #   `id` int NULL DEFAULT NULL,
    #   `name` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
    #   `classId` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
    #   `chineseScore` int NULL DEFAULT NULL,
    #   `mathScore` int NULL DEFAULT NULL,
    #   `englishScore` int NULL DEFAULT NULL,
    #   `totalScore` int NULL DEFAULT NULL
    # ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
    #
    # DROP TABLE IF EXISTS `teacher_info`;
    # CREATE TABLE `teacher_info`  (
    #   `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
    #   `subject` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
    #   `classId` int NOT NULL
    # ) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;
    #
    #
    # """)

    # vn.train(question='查询id为1的学生的英语老师？',
    #          sql='SELECT * FROM teacher_info where subject="english" AND classId = (select classId from student_info where id =1);')
    # vn.train(question='查询id为1的学生的英语老师和数学老师和语文老师？',
    #          sql='SELECT * FROM teacher_info where subject in ("english", "math", "chinese" ) AND classId = (select classId from student_info where id =1);')


    # 保存原始的标准输出流
    old_stdout = sys.stdout

    # 创建一个新的字符串IO对象
    sys.stdout = StringIO()

    print(vn.generate_sql(question=words))

    # 获取打印台中的文本
    output = sys.stdout.getvalue().splitlines()

    # 恢复原始的标准输出流
    sys.stdout = old_stdout

    # 从第二行开始获取文本
    start_line = 1
    end_line = len(output)

    # 将指定行及其后面所有行的文本赋值给str_var变量
    str_var = "\n".join(output[start_line:end_line])

    # 使用正则表达式匹配出单独的 SQL 语句
    pattern = re.compile(r"(SELECT .*?;)", re.DOTALL)
    sql_statements = pattern.findall(str_var)

    # 取出第一个 SQL 语句
    first_sql_statement = sql_statements[0]

    return first_sql_statement

def executiveSql(sql):#执行已经转化出来的sql语句
    # 连接到MySQL数据库
    mydb = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456",
        database="data_co_pilot"
    )

    # 创建一个游标对象
    mycursor = mydb.cursor()

    # 执行SQL查询
    mycursor.execute(sql)

    # 获取查询结果的列名
    columns = [i[0] for i in mycursor.description]

    # 获取查询结果的数据,包括列名和数据
    result = []
    for row in mycursor.fetchall():
        row_data = dict(zip(columns, row))
        result.append(row_data)


    # 关闭游标和数据库连接
    mycursor.close()
    mydb.close()

    return json.dumps(result)

def getSql(text):
    sqlResult = VannaGetSql(text) #根据自然语言转化为sql语句
    print(sqlResult)
    result = executiveSql(sqlResult) #根据sql语句的执行，得到数据结果
    print(result)
    return result

# if __name__ == '__main__':
#     getSql('查询id为1的学生的英语老师')

#查询student_info表中id为1或2或3的学生
#查询所有学生和他对应的语文成绩和数学成绩
#'查询id为1的学生的英语老师语文老师数学老师
#查询语文成绩高于90的学生