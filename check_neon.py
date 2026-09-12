import psycopg2

conn = psycopg2.connect("postgresql://neondb_owner:npg_2pfHFcloB7Mr@ep-rapid-thunder-azkzd3yt-pooler.c-3.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")
cur = conn.cursor()

cur.execute("SELECT COUNT(*) FROM fact_sales;")
print("Row count:", cur.fetchone()[0])

cur.execute("SELECT * FROM fact_sales LIMIT 3;")
for row in cur.fetchall():
    print(row)

cur.execute("SELECT SUM(revenue) FROM fact_sales;")
print("Total revenue:", cur.fetchone()[0])

conn.close()