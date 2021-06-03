import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

import json

### Setup database
with open('credentials.json', 'r') as json_file:
    credentials = json.load(json_file)

sql_engine = create_engine(f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['dbname']}")


def runQuery(sql):
    result = sql_engine.connect().execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())

### Querys
# Users subscribed
def get_users_subscribed_audiobook_plays(start, end):
    """ Query first_plays and last_plays of the users from the audiobook_plays

    Args:
        start (): 
        end (): 

    Returns:
        pandas.core.frame.DataFrame: DataFrame
    """

    df_users = runQuery(f"""
        WITH first_time_played(user_id, first_play, last_play, has_been_subscribed) AS (
            SELECT DISTINCT ap.user_id
            , DATE_TRUNC('day', FIRST_VALUE(ap.created_at) OVER (PARTITION BY ap.user_id ORDER BY ap.created_at))::date
            , DATE_TRUNC('day', FIRST_VALUE(ap.created_at) OVER (PARTITION BY ap.user_id ORDER BY ap.created_at DESC))::date
            , has_been_subscribed
            FROM audiobook_plays ap
            INNER JOIN users us
            ON ap.user_id = us.id
            WHERE ap.created_at BETWEEN '{start}'::TIMESTAMP AND '{end}'::TIMESTAMP
        )
        SELECT first_play,
            last_play,
            has_been_subscribed
        FROM first_time_played;
    """)

    return df_users

# Active Users
def get_users_active_audiobook_plays():
    """ Query active and total users per week from the audiobook_plays

    Args:
        start (): 
        end (): 

    Returns:
        pandas.core.frame.DataFrame: DataFrame
    """

    df_users = runQuery("""
        WITH user_week_date(user_id, 
            current_date_, prev_date) AS (
            SELECT DISTINCT
                abp.user_id,
                cw.current_week,
                (cw.current_week - INTERVAL '7 days')::date
            FROM audiobook_plays abp,
                LATERAL(SELECT DISTINCT abp.user_id, DATE_TRUNC('week',created_at)::date AS current_week) cw
            ORDER BY user_id, cw.current_week
        ),
        user_week_active AS (
            SELECT *,
                LAG(current_date_) OVER(PARTITION BY user_id ORDER BY current_date_) AS last_week
            FROM user_week_date uwa
        ),
        user_retention AS (
            SELECT *, 
                prev_date=last_week AS retained
            FROM user_week_active
        ),
        WAU AS (
            SELECT current_date_, 
            COUNT(1) AS total_users,
            COUNT(CASE WHEN retained THEN 1 END) AS active_users
            FROM user_retention
            GROUP BY current_date_
            ORDER BY current_date_
        )
        SELECT current_date_, 
            total_users,
            active_users,
            ROUND(active_users::numeric/total_users*100, 2) AS retention_rate
        FROM WAU;
    """)

    return df_users

### Data transformations with pandas
def cummulative(column, mask=pd.Series(dtype='float64')):
    """ Creates a dataframe with the counts and cummulative

    Args:
        column (pandas.core.series.Series): Could be a Series or column from pandas 
        mask (pandas.core.series.Series): Boolean mask to filter a DataFrame

    Returns:
        pandas.core.frame.DataFrame: A DataFrame with the counts and cummulatives
    """
    if mask.empty :
        count_series = column.value_counts()
    else:
        count_series = column[mask].value_counts()
        
    count_df = pd.DataFrame(count_series)
    count_df.reset_index(inplace=True)
    count_df.rename(columns={'index':'date', 'first_play':'users'}, inplace=True)
    count_df.sort_values(by='date', inplace=True)
    count_df['cumm_users'] = count_df['users'].cumsum()
    return count_df


### Transformations for users subscribed
### Pandas Dataframe
df = get_users_subscribed_audiobook_plays('2018-12-01', '2019-4-9')

# Change data types of the dates columns
df['first_play'] = pd.to_datetime(df['first_play'])
df['last_play'] = pd.to_datetime(df['last_play'])

# Boolean mask if users are subscribed
is_subscribed_mask = df['has_been_subscribed']==True

# Calcule cummulative dataframe
df_users_subscribed = cummulative(df['first_play'], is_subscribed_mask)
df_users = cummulative(df['first_play'])


### Transformations for active users
df_active_users = get_users_active_audiobook_plays()

# Change data types of the dates columns
df_active_users['current_date_'] = pd.to_datetime(df_active_users['current_date_'])