import psycopg2
import time

regions = [
    'ap-south-1',      # Mumbai
    'us-east-1',       # N. Virginia
    'us-west-1',       # N. California
    'us-west-2',       # Oregon
    'eu-central-1',    # Frankfurt
    'eu-west-1',       # Ireland
    'eu-west-2',       # London
    'ap-southeast-1',  # Singapore
    'ap-northeast-1',  # Tokyo
    'ap-southeast-2',  # Sydney
    'sa-east-1',       # Sao Paulo
    'ca-central-1',    # Canada
]

print("Scanning for correct Supabase pooler region...")
found = False

for region in regions:
    host = f'aws-0-{region}.pooler.supabase.com'
    print(f"Trying {host}...")
    try:
        conn = psycopg2.connect(
            host=host,
            user='postgres.pmmiddrxjkfqkmldmbwf',
            password='Shannu@2430',
            database='postgres',
            port=6543,
            connect_timeout=5
        )
        print(f"\nSUCCESS! Found the correct region: {region}")
        print(f"Connection String: postgresql://postgres.pmmiddrxjkfqkmldmbwf:Shannu@2430@{host}:6543/postgres")
        conn.close()
        found = True
        break
    except Exception as e:
        # Ignore errors and move to next
        pass

if not found:
    print("\nCould not find the region automatically.")
