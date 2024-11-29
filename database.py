import sqlite3

# Membuat koneksi ke database SQLite (akan membuat database baru jika belum ada)
conn = sqlite3.connect('skripsi.db')
cursor = conn.cursor()

# Membuat tabel PasswordResetTokens
cursor.execute('''
CREATE TABLE IF NOT EXISTS PasswordResetTokens (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    userId INTEGER NOT NULL,
    token TEXT NOT NULL,
    expiresAt TEXT NOT NULL,
    createdAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updatedAt TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);
''')

# Membuat tabel branch
cursor.execute('''
CREATE TABLE IF NOT EXISTS branch (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    city TEXT NOT NULL,
    from_active_time TEXT NOT NULL,
    to_active_time TEXT NOT NULL,
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL,
    deleteAt TEXT
);
''')

# Membuat tabel users
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL,
    password TEXT NOT NULL,
    role TEXT CHECK(role IN ('superadmin', 'admin', 'security')) NOT NULL,
    branch_id INTEGER NOT NULL,
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL,
    deleteAt TEXT,
    FOREIGN KEY (branch_id) REFERENCES branch(id)
);
''')

# Membuat tabel sensor
cursor.execute('''
CREATE TABLE IF NOT EXISTS sensor (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    code TEXT NOT NULL UNIQUE,
    branch_id INTEGER NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    isOn INTEGER NOT NULL DEFAULT 0,
    isOpen INTEGER NOT NULL DEFAULT 0,
    isDetected INTEGER NOT NULL DEFAULT 0,
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL,
    deleteAt TEXT,
    FOREIGN KEY (branch_id) REFERENCES branch(id)
);
''')

# Membuat tabel history
cursor.execute('''
CREATE TABLE IF NOT EXISTS history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sensor_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    description TEXT,
    date TEXT NOT NULL,
    branch_id INTEGER NOT NULL,
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL,
    deletedAt TEXT,
    FOREIGN KEY (sensor_id) REFERENCES sensor(id),
    FOREIGN KEY (user_id) REFERENCES users(id),
    FOREIGN KEY (branch_id) REFERENCES branch(id)
);
''')

# Membuat tabel foodFish
cursor.execute('''
CREATE TABLE IF NOT EXISTS foodFish (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    description TEXT NOT NULL,
    branch_id INTEGER NOT NULL,
    sensor_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    weight REAL NOT NULL,
    onStart TEXT NOT NULL,
    onEnd TEXT NOT NULL,
    createdAt TEXT NOT NULL,
    updatedAt TEXT NOT NULL,
    deletedAt TEXT,
    FOREIGN KEY (branch_id) REFERENCES branch(id),
    FOREIGN KEY (sensor_id) REFERENCES sensor(id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);
''')

# Commit perubahan dan menutup koneksi
conn.commit()

# Menutup koneksi ke database
conn.close()

print("Tabel-tabel telah berhasil dibuat.")
