# Supabase Setup Guide

## Step 1: Create Tables in Supabase

### Option A: Using Supabase Dashboard
1. Go to your Supabase project: https://app.supabase.com
2. Click on **SQL Editor** in the left sidebar
3. Click **New Query**
4. Copy the entire content from `database/schema_postgresql.sql`
5. Paste it into the SQL Editor
6. Click **Run**

### Option B: Using psql Command Line
```bash
psql -h db.pmmiddrxjkfqkmldmbwf.supabase.co -U postgres -d postgres -f database/schema_postgresql.sql
```
When prompted, enter password: `Shannu@2430`

---

## Step 2: Verify Configuration

Your app is already configured with Supabase credentials in `.env`:
```
POSTGRES_HOST=db.pmmiddrxjkfqkmldmbwf.supabase.co
POSTGRES_USER=postgres
POSTGRES_PASSWORD=Shannu@2430
POSTGRES_DB=postgres
POSTGRES_PORT=5432
```

## Step 3: Start Using the App

The Flask server is already running on:
- **URL**: http://localhost:5000
- **Database**: Connected to Supabase

---

## Troubleshooting

### Connection Issues
- Ensure your Supabase project allows public access (RLS policies)
- Check that the IP isn't blocked by Supabase firewall
- Verify credentials in `.env` file

### Table Creation Issues
- Supabase SQL Editor has a 5MB limit per query
- If schema is too large, run it in smaller chunks
- Monitor for any PostgreSQL syntax errors

---

## Next Steps

1. **Create tables using the PostgreSQL schema**
2. **Refresh your browser** at http://localhost:5000
3. **Try registering** a new student account
4. **Login** with the credentials you created

The app will now store all data in your Supabase PostgreSQL database!
