import psycopg2
from config import load_config



def user_exist(user_name_x, user_name_0):
    checking_existence = """SELECT count(*) from users where user_name IN (%s, %s);"""
    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(checking_existence, (user_name_x,user_name_0))
                ans = cur.fetchone()[0]
                if ans == 2:
                    return True
                else:
                    return False
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def current_data(user_name):
    sql = """select score from users WHERE user_name = %s;"""
    config = load_config()
    try:
            with psycopg2.connect(**config) as conn:
                with conn.cursor() as cur:
                    cur.execute(sql, (user_name, ))
                    res = cur.fetchone()
                    if res:
                        return res[0]
                    else:
                        return 0
    except(Exception, psycopg2.DatabaseError) as error:
        print(error)

def insert_user_data(user_name):
    sql = """INSERT INTO users (user_name, score) VALUES (%s, 0)"""

    config = load_config()

    try:
        with psycopg2.connect(**config) as conn:
            with conn.cursor() as cur:
                cur.execute(sql, (user_name, ))
                conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    
def update_score(user_name):
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("UPDATE users set score = score + 1 where user_name = %s;", (user_name,))
            conn.commit()
def insert_game(user_x, user_o, result):
    config = load_config()
    with psycopg2.connect(**config) as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO tic_tac_toe (user_name_x, user_name_0, result) VALUES (%s, %s, %s);",
                        (user_x, user_o, result))
            conn.commit()