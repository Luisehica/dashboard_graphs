import pandas as pd
import numpy as np
from sqlalchemy import create_engine, text

import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt


### Setup the database server
credentials = {
    'host':'35.227.110.100',
    'dbname':'postgres',
    'user':'postgres',
    'password':'n$EYUJRrmZ9jz2>7o',
    'port':'5432'
}

sql_engine = create_engine(f"postgresql://{credentials['user']}:{credentials['password']}@{credentials['host']}:{credentials['port']}/{credentials['dbname']}")

def runQuery(sql):
    result = sql_engine.connect().execution_options(isolation_level="AUTOCOMMIT").execute((text(sql)))
    return pd.DataFrame(result.fetchall(), columns=result.keys())

# query information needed for create the graph
df_all = runQuery(f"""
    SELECT u.id as user_id, u.gender as gender,
        ab.id as book_id, ab.actual_size, ab.grade_level, ab.language,
        abp.seconds as time_listened,
        bc.name as category
    FROM audiobook_plays abp
    INNER JOIN audiobook ab
    ON abp.audiobook_id = ab.id
    INNER JOIN users u
    ON abp.user_id = u.id
    INNER JOIN book_categories bc
    ON ab.book_category_codes[1] = bc.book_cateogory_code
    LIMIT 10;
    """)

### Initialize graph
bipartite_graph = nx.Graph()

# Add nodes with node attribute "bipartite"
bipartite_graph.add_nodes_from(list(pd.unique(df_all["user_id"])), bipartite=0)
bipartite_graph.add_nodes_from(list(pd.unique(df_all["book_id"])), bipartite=1)
bipartite_graph.add_nodes_from(list(pd.unique(df_all["category"])), bipartite=2)

# Add edges in a list of tuples of nodes
n = len(df_all.index)
bipartite_graph.add_edges_from([list(df_all[["user_id","book_id"]].iloc[i]) for i in range(n)]) # verify n+1 or just n

nx.draw(bipartite_graph, with_labels=True, font_weight='bold')
plt.show()