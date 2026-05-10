-- Blood Bank and Organ Donation Portal — PostgreSQL schema
-- Apply to an existing database (e.g. Render PostgreSQL: use that DB only).
-- Local: createdb blood_bank_portal && psql -d blood_bank_portal -f database/schema.sql

-- Table: users (donors)
CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    age INTEGER NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    organ_donor BOOLEAN DEFAULT FALSE,
    phone VARCHAR(20),
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    city VARCHAR(100),
    availability_status VARCHAR(20) DEFAULT 'Available',
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_users_email UNIQUE (email),
    CONSTRAINT chk_users_blood_group CHECK (
        blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
    )
);

-- Table: hospitals
CREATE TABLE IF NOT EXISTS hospitals (
    id SERIAL PRIMARY KEY,
    hospital_name VARCHAR(150) NOT NULL,
    email VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    phone VARCHAR(20),
    city VARCHAR(100),
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_hospitals_email UNIQUE (email)
);

-- Table: admins
CREATE TABLE IF NOT EXISTS admins (
    id SERIAL PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    password VARCHAR(255) NOT NULL,
    CONSTRAINT uq_admins_username UNIQUE (username)
);

-- Table: blood_requests
CREATE TABLE IF NOT EXISTS blood_requests (
    id SERIAL PRIMARY KEY,
    hospital_id INTEGER NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    units_required INTEGER NOT NULL,
    city VARCHAR(100),
    urgency VARCHAR(20) DEFAULT 'Normal',
    status VARCHAR(20) DEFAULT 'Open',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_blood_requests_hospital FOREIGN KEY (hospital_id)
        REFERENCES hospitals (id) ON DELETE CASCADE,
    CONSTRAINT chk_blood_requests_blood_group CHECK (
        blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
    )
);

-- Table: organ_requests
CREATE TABLE IF NOT EXISTS organ_requests (
    id SERIAL PRIMARY KEY,
    hospital_id INTEGER NOT NULL,
    organ_type VARCHAR(100) NOT NULL,
    blood_group VARCHAR(5),
    city VARCHAR(100),
    urgency VARCHAR(20) DEFAULT 'Normal',
    status VARCHAR(20) DEFAULT 'Open',
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_organ_requests_hospital FOREIGN KEY (hospital_id)
        REFERENCES hospitals (id) ON DELETE CASCADE
);

-- Table: donations
CREATE TABLE IF NOT EXISTS donations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    hospital_id INTEGER NOT NULL,
    donation_type VARCHAR(20) DEFAULT 'Blood',
    donation_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_donations_user FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE CASCADE,
    CONSTRAINT fk_donations_hospital FOREIGN KEY (hospital_id)
        REFERENCES hospitals (id) ON DELETE CASCADE
);

-- Table: blood_stock
CREATE TABLE IF NOT EXISTS blood_stock (
    id SERIAL PRIMARY KEY,
    hospital_id INTEGER NOT NULL,
    blood_group VARCHAR(5) NOT NULL,
    units_available INTEGER DEFAULT 0,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_blood_stock_hospital FOREIGN KEY (hospital_id)
        REFERENCES hospitals (id) ON DELETE CASCADE,
    CONSTRAINT uq_blood_stock_hospital_group UNIQUE (hospital_id, blood_group),
    CONSTRAINT chk_blood_stock_blood_group CHECK (
        blood_group IN ('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-')
    )
);

-- Table: notifications
CREATE TABLE IF NOT EXISTS notifications (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    message TEXT NOT NULL,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notifications_user FOREIGN KEY (user_id)
        REFERENCES users (id) ON DELETE CASCADE
);

-- Auto-update blood_stock.updated_at on row change (replaces MySQL ON UPDATE CURRENT_TIMESTAMP)
CREATE OR REPLACE FUNCTION trg_set_blood_stock_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS blood_stock_updated_at ON blood_stock;

CREATE TRIGGER blood_stock_updated_at
    BEFORE UPDATE ON blood_stock
    FOR EACH ROW
    EXECUTE FUNCTION trg_set_blood_stock_updated_at();
