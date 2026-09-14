import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(os.environ["DATABASE_URL"])
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM fact_sales;")
print("Row count:", cur.fetchone()[0])

cur.execute("SELECT * FROM fact_sales LIMIT 3;")
for row in cur.fetchall():
    print(row)

cur.execute("SELECT SUM(revenue) FROM fact_sales;")
print("Total revenue:", cur.fetchone()[0])

conn.close()
