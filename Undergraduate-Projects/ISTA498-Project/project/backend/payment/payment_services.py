from snowflake_db.snowflake_engine import insert_user_deposited

def make_deposit(id, amount):
    insert_user_deposited(id, amount)