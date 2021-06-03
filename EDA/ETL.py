import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

import json
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

from neo4j import GraphDatabase

### Extract
# Setup the database server


def extract_save_csv(query, file_name):
    with open('credentials.json', 'r') as json_file:
        credentials = json.load(json_file)

    sql_engine = create_engine(f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['dbname']}")
    logger.info('Connection to database succesful')

    def runQuery(sql):
        result = sql_engine.connect().execute((text(sql)))
        return pd.DataFrame(result.fetchall(), columns=result.keys())
    df_all = runQuery(query)
    logger.info('Query run database succesful')

    df_all.to_csv(file_name)
    logger.info('Connection to database succesful')

### Load
class Load_to_Neo4j:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def load_data(self, csv):
        with self.driver.session() as session:
            result = session.write_transaction(self._create_and_load, csv)
            print(result)
            
    @staticmethod
    def _create_and_load(tx, csv):
        result = tx.run("""
        LOAD CSV WITH HEADERS FROM 'file:///beek_db.csv' AS db
        CREATE (u:Users {userId: db.user_id
            , created_at: db.user_created_at
            , last_sign_in: db.last_sign_in_at
            , gender: db.gender
            , has_seen_onboarding: db.has_seen_onboarding
            , has_been_subscribed: db.has_been_subscribed
            ,})
        """, file=csv)

if __name__ == "__main__":

    query_all_transactions ="""
        WITH books(book_id, category_name_1 ) AS (
            SELECT a.id
                , bc.name
                , a.actual_size
                , a.grade_level
                , a."language"
                --, a.book_category_codes[2]
                --, a.book_category_codes[3]	
            FROM audiobook a
            LEFT JOIN book_categories bc
            ON a.book_category_codes[1]=bc.book_cateogory_code
        )
        SELECT a.id AS transaction_id
            , a.created_at AS transaction_created_at
            , a.seconds AS seconds_played
            , a.user_id
            , u.created_at AS user_created_at
            , u.last_sign_in_at
            , u.gender
            , u.has_seen_onboarding 
            , u.has_been_subscribed 
            , b.book_id
            , b.category_name_1
            , b.actual_size
            , b.grade_level
            , b."language"
        FROM audiobook_plays a
        LEFT JOIN users u
        ON a.user_id = u.id
        LEFT JOIN books b
        ON a.audiobook_id = b.book_id;
    """
    #extract_save_csv(query_all_transactions, 'beek_db.csv')
    if True:
        extract_save_csv("""
            WITH books(book_id, category_name_1 ) AS (
                SELECT a.id
                    , bc.name
                    , a.actual_size
                    , a.grade_level
                    , a."language"
                    --, a.book_category_codes[2]
                    --, a.book_category_codes[3]	
                FROM audiobook a
                LEFT JOIN book_categories bc
                ON a.book_category_codes[1]=bc.book_cateogory_code
            ) SELECT *
            FROM books
        """, 'audiobook.csv')

        extract_save_csv("""
            SELECT *
            FROM audiobook_plays
        """, 'audiobook_plays.csv')

        extract_save_csv("""
            SELECT *
            FROM users
        """, 'users.csv')

    beek_db = Load_to_Neo4j("bolt://localhost:7687", "neo4j", "test")
    beek_db.load_data("beak_db.csv")
    #greeter.close()