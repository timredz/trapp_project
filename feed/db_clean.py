from utils.connect_psql import bdengine


q_clean_orders = """
        
    TRUNCATE TABLE marketdata_myorders
    
"""


q_clean_trades = """
        
    TRUNCATE TABLE marketdata_mytrades
    
"""


# -----> main thread
engine = bdengine()
with engine.begin() as conn:
    conn.execute(q_clean_orders)
    conn.execute(q_clean_trades)
