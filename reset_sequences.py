import psycopg2

password = input("Enter your Supabase database password: ")

conn = psycopg2.connect(
    host="aws-0-eu-west-1.pooler.supabase.com",
    port=5432,
    dbname="postgres",
    user="postgres.elpipcpnuaxvkatrnpvk",
    password=password,
    sslmode="require"
)

cursor = conn.cursor()

tables = [
    "users",
    "lessons",
    "usage",
    "payments",
    "extension_credits"
]

for table in tables:
    cursor.execute(
        f"""
        SELECT setval(
            pg_get_serial_sequence('public.{table}', 'id'),
            COALESCE((SELECT MAX(id) FROM public.{table}), 1),
            true
        )
        """
    )

conn.commit()

print("PostgreSQL ID sequences reset successfully.")

cursor.close()
conn.close()