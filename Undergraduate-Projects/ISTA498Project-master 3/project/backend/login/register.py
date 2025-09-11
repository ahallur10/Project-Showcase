import bcrypt
from snowflake_db.snowflake_engine import insert_user, get_user_password

def sign_up(id,password):
    hashed_password = bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())
    insert_user(id, hashed_password.decode("utf8"))
    return {200}

def id_login(id,password):
    print(id, password)
    if bcrypt.checkpw(password.encode('utf8'), get_user_password(id).encode('utf8')):
        return 200
    else:
        raise AssertionError
    
   