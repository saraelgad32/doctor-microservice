# config.py

# INSTRUCTIONS FOR FRIENDS:
# 1. Open SQL Server Management Studio (SSMS).
# 2. Look at the "Server Name" in the Connect box.
# 3. Paste that name below inside the quotes.

DB_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'SARAHP414'
,  # <--- THEY CHANGE THIS LINE ONLY
    'database': 'DoctorServiceDB',
    'trusted_connection': 'yes'
}