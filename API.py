from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine
from sqlalchemy import text
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
from typing import List, Optional
import os
import clips
print("Available clips methods:", [method for method in dir(clips) if not method.startswith('_')])
import io
import sys
from pydantic import BaseModel

app = FastAPI(title="Crypto Market API", description="API test 1")

# Database connection
DATABASE_URL = os.environ.get('DATABASE_URL')
print(f"Database URL: {DATABASE_URL}")
if DATABASE_URL and DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    


engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Pydantic models for response
class MarketData(BaseModel):
    coins_count: int
    active_markets: int
    total_mcap: float
    total_volume: float
    btc_dominance: float
    eth_dominance: float
    mcap_change: float
    volume_change: float
    avg_change_percent: float
    timestamp: datetime

def process_clips_rules(market_data):
    insights = []
    
    try:
        # Reset environment
        clips.common.reset()
        
        # Define template and rule
        clips.common.build("""
        (deftemplate market-data
          (slot total_mcap)
          (slot btc_dominance)
          (slot eth_dominance)
          (slot coins_count)
          (slot active_markets)
          (slot total_volume)
          (slot mcap_change)
          (slot volume_change)
          (slot avg_change_percent))
        
        (defrule btc-dominance-high
          (market-data (btc_dominance ?btc_dominance&:(> ?btc_dominance 50)))
          =>
          (printout t "BOOM" crlf))
        """)
        
        # Assert fact
        clips.facts.assert_fact("""
        (market-data 
          (total_mcap {total_mcap})
          (btc_dominance {btc_dominance})
          (eth_dominance {eth_dominance})
          (coins_count {coins_count})
          (active_markets {active_markets})
          (total_volume {total_volume})
          (mcap_change {mcap_change})
          (volume_change {volume_change})
          (avg_change_percent {avg_change_percent}))
        """.format(**market_data))
        
        # Run rules
        clips.common.run()
        
    except Exception as e:
        return [f"CLIPS Processing Error: {str(e)}"]
    
    return insights
print
# API Routes
@app.get("/")
async def root():
    try:
        with SessionLocal() as db:
            result = db.execute(text("""
                SELECT * FROM crypto_market_data 
                ORDER BY timestamp DESC 
                LIMIT 1
            """)).fetchone()
            
            if not result:
                raise HTTPException(status_code=404, detail="No market data available")
            
            columns = ['id', 'timestamp', 'coins_count', 'active_markets', 
                      'total_mcap', 'total_volume', 'btc_dominance', 
                      'eth_dominance', 'mcap_change', 'volume_change', 
                      'avg_change_percent']
            market_data = dict(zip(columns, result))
            
            return {
    "message": "Welcome to the Crypto Market API",
    "data_source": "CoinLore",
    "current_market_data": market_data,
    "clips_insights": process_clips_rules(market_data)
}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")
    

    # none of the below stuff is really needed but when i commented it out the api would not work
    # I love coding :)
# @app.get("/health")
# async def health_check():
#     try:
#         with SessionLocal() as db:
#             db.execute("SELECT 1")
#             result = db.execute("""
#                 SELECT COUNT(*) 
#                 FROM crypto_market_data 
#                 WHERE timestamp >= NOW() - INTERVAL '10 minutes'
#             """).scalar()
#             return {
#                 "status": "healthy",
#                 "database": "connected",
#                 "recent_data_available": result > 0 if result is not None else False
#             }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Database error: {e}")

# @app.get("/market/current", response_model=MarketData)
# async def get_current_market_data():
#     """Get the most recent market data"""
#     try:
#         with SessionLocal() as db:
#             print("Querying the database for the most recent market data...")  # Debug log
#             result = db.execute("""
#                 SELECT * FROM crypto_market_data 
#                 ORDER BY timestamp DESC 
#                 LIMIT 1
#             """).fetchone()
            
#             if not result:
#                 print("No data found.")  # Debug log
#                 raise HTTPException(status_code=404, detail="No market data available")
            
#             print("Query result:", result)  # Debug log
            
#             # Convert row to dictionary using column names
#             columns = ['id', 'timestamp', 'coins_count', 'active_markets', 
#                        'total_mcap', 'total_volume', 'btc_dominance', 
#                        'eth_dominance', 'mcap_change', 'volume_change', 
#                        'avg_change_percent']
#             response_data = dict(zip(columns, result))
#             print("Response data to be returned:", response_data)  # Debug log
            
#             return response_data
#     except Exception as e:
#         print("Error occurred:", e)  # Debug log
#         raise HTTPException(status_code=500, detail=f"Internal Server Error: {e}")

# @app.get("/market/history")
# async def get_market_history(
#     start_date: Optional[datetime] = None,
#     end_date: Optional[datetime] = None,
#     limit: int = 100
# ):
#     """Get historical market data with optional date filtering"""
#     with SessionLocal() as db:
#         query = "SELECT * FROM crypto_market_data WHERE 1=1"
#         params = {}
        
#         if start_date:
#             query += " AND timestamp >= :start_date"
#             params["start_date"] = start_date
#         if end_date:
#             query += " AND timestamp <= :end_date"
#             params["end_date"] = end_date
            
#         query += " ORDER BY timestamp DESC LIMIT :limit"
#         params["limit"] = limit
        
#         results = db.execute(query, params).fetchall()
        
#         if not results:
#             raise HTTPException(status_code=404, detail="No data found for specified period")
            
#         columns = ['id', 'timestamp', 'coins_count', 'active_markets', 
#                        'total_mcap', 'total_volume', 'btc_dominance', 
#                        'eth_dominance', 'mcap_change', 'volume_change', 
#                        'avg_change_percent']
#         return [dict(zip(columns, row)) for row in results]

# @app.get("/market/stats/{timeframe}", response_model=MarketData)
# async def get_market_stats(timeframe: str):
#     """Get market statistics for a specific timeframe (24h, 7d, 30d)"""
#     timeframe_map = {
#         "24h": "24 hours",
#         "7d": "7 days",
#         "30d": "30 days"
#     }
    
#     if timeframe not in timeframe_map:
#         raise HTTPException(status_code=400, detail="Invalid timeframe. Use 24h, 7d, or 30d")
        
#     with SessionLocal() as db:
#         result = db.execute(f"""
#             WITH time_range AS (
#                 SELECT * FROM crypto_market_data 
#                 WHERE timestamp >= NOW() - INTERVAL '{timeframe_map[timeframe]}'
#             )
#             SELECT 
#                 AVG(total_mcap) as avg_mcap,
#                 AVG(total_volume) as avg_volume,
#                 AVG(btc_dominance) as avg_btc_dominance,
#                 AVG(eth_dominance) as avg_eth_dominance,
#                 MAX(total_mcap) as max_mcap,
#                 MIN(total_mcap) as min_mcap
#             FROM time_range
#         """).fetchone()
        
#         if not result:
#             raise HTTPException(status_code=404, detail=f"No data available for {timeframe}")
            
#         return {
#             "timeframe": timeframe,
#             "avg_mcap": result[0],
#             "avg_volume": result[1],
#             "avg_btc_dominance": result[2],
#             "avg_eth_dominance": result[3],
#             "max_mcap": result[4],
#             "min_mcap": result[5]
#         }

