CREATE TABLE crypto_market_data (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    coins_count INTEGER,
    active_markets INTEGER,
    total_mcap NUMERIC(20,2),  -- More precise for large financial numbers
    total_volume NUMERIC(20,2), -- More precise for large financial numbers
    btc_dominance NUMERIC(5,2), -- Percentage value (0-100)
    eth_dominance NUMERIC(5,2), -- Percentage value (0-100)
    mcap_change NUMERIC(5,2),   -- Percentage value
    volume_change NUMERIC(5,2),  -- Percentage value
    avg_change_percent NUMERIC(5,2) -- Percentage value
); 