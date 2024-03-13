

# PostgreSQL Database Management on Rocky Linux


## SSH Login to the PostgreSQL Server

```bash
ssh -p 1522 postgres@155.133.26.105
```

## Manage Databases and Permissions

1. **Login as the PostgreSQL User and Access the PostgreSQL Shell:**

```bash
psql -U postgres
```

2. **Delete Existing Database (if needed):**

```sql
DROP DATABASE IF EXISTS postgres_db;
```

3. **Create a New Database:**

```sql
CREATE DATABASE postgres_db;
```

4. **Restore Database from SQL Dump File:**

```bash
pg_restore -U postgres -d postgres_db Feb24_2024.sql
```
Replace `Feb24_2024.sql` with the actual file name of your SQL dump file.

5. **Grant Permissions to a User (e.g., 'g453f8r8'):**

```sql
GRANT ALL ON ALL TABLES IN SCHEMA public TO g453f8r8;
GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO g453f8r8;
GRANT ALL ON ALL FUNCTIONS IN SCHEMA public TO g453f8r8;
```

6. **Exit PostgreSQL Shell:**

```sql
\q
```

## Exit SSH Session

```bash
exit
```

