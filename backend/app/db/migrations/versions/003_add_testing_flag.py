# backend/app/db/migrations/versions/003_add_testing_flag.py
from ...connection import get_db

version = 3
name = "add_testing_flag"


def up():
    """Add is_testing column to arr_config table"""
    with get_db() as conn:
        # Add the new column with a default value of 0 (false)
        conn.execute('''
        ALTER TABLE arr_config
        ADD COLUMN is_testing BOOLEAN DEFAULT 0
        ''')
        conn.commit()


def down():
    """Remove is_testing column from arr_config table"""
    with get_db() as conn:
        # Create a temporary table without the is_testing column
        conn.execute('''
        CREATE TEMPORARY TABLE arr_config_backup (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            type TEXT NOT NULL,
            tags TEXT,
            arr_server TEXT NOT NULL,
            api_key TEXT NOT NULL,
            data_to_sync TEXT,
            last_sync_time TIMESTAMP,
            sync_percentage INTEGER DEFAULT 0,
            sync_method TEXT DEFAULT 'manual',
            sync_interval INTEGER DEFAULT 0,
            import_as_unique BOOLEAN DEFAULT 0,
            import_task_id INTEGER DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')

        # Copy data to the backup table
        conn.execute('''
        INSERT INTO arr_config_backup 
        SELECT id, name, type, tags, arr_server, api_key, data_to_sync, 
               last_sync_time, sync_percentage, sync_method, sync_interval,
               import_as_unique, import_task_id, created_at, updated_at
        FROM arr_config
        ''')

        # Drop the original table
        conn.execute('DROP TABLE arr_config')

        # Rename the backup table to the original name
        conn.execute('ALTER TABLE arr_config_backup RENAME TO arr_config')

        conn.commit()
