import uuid
import sqlite3
from datetime import datetime


# translate account 0, pay_category 2 and program 5 into those ids
def translate_three_paras(connection, text, column_name):
    try:
        sql = "SELECT name FROM tb_%s WHERE id = \"%s\";" % (column_name, text)
        c = connection.cursor()
        ans = c.execute(sql).fetchone()[0]
        if ans is not None:
            return text
    except TypeError:
        try:
            sql = "SELECT id FROM tb_%s WHERE name = \"%s\";" % (column_name, text)
            c = connection.cursor()
            ans = c.execute(sql).fetchone()[0]
        except TypeError:
            ans = "ERR_NOT_IN_LIST"
    return ans


def insert_tb_pay_line(db_file, data, table="tb_pay"):
    conn = sqlite3.connect(db_file)
    data = [str(uuid.uuid4())] + data
    formatted_data = [
        item.strftime("%Y-%m-%d %H:%M:%S") if isinstance(item, datetime) else str(item)
        for item in data
    ]

    for index, column_name in [[1, "account"], [3, "pay_category"], [6, "program"]]:
        formatted_data[index] = translate_three_paras(conn, formatted_data[index], column_name)

    sql = "INSERT INTO %s (guid, account_id, amount, category_id, paid_time, real_time, program_id, editor, memo) VALUES (" % table
    sql += (" ".join(["\"%s\","] * len(formatted_data)) % tuple(formatted_data))[:-1]
    sql += ");"

    c = conn.cursor()
    try:
        c.execute(sql)
    except sqlite3.IntegrityError:
        print("Duplicate uuid! WoW! Gonna generate a new one.")
        formatted_data[0] = str(uuid.uuid4())
        sql = "INSERT INTO %s (guid, account_id, amount, category_id, paid_time, real_time, program_id, editor, memo) VALUES (" % table
        sql += (" ".join(["\"%s\","] * len(formatted_data)) % tuple(formatted_data))[:-1]
        sql += ");"
        c.execute(sql)
    conn.commit()
    conn.close()
