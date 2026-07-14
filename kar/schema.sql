-- DriveGO Lock System — MySQL Schema
-- Run: mysql -u root -p drivego < schema.sql

CREATE DATABASE IF NOT EXISTS drivego;
USE drivego;

-- Users
CREATE TABLE IF NOT EXISTS users (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  name        VARCHAR(100) NOT NULL,
  email       VARCHAR(150) NOT NULL UNIQUE,
  pin_hash    VARCHAR(255) DEFAULT NULL,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Vehicles
CREATE TABLE IF NOT EXISTS vehicles (
  id           VARCHAR(20) PRIMARY KEY,
  vehicle_name VARCHAR(100) NOT NULL,
  plate        VARCHAR(30)  NOT NULL,
  is_locked    TINYINT(1)   NOT NULL DEFAULT 1,
  locked_at    DATETIME     DEFAULT CURRENT_TIMESTAMP,
  updated_at   DATETIME     DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- OTP codes (persisted — survives server restarts)
CREATE TABLE IF NOT EXISTS otp_codes (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  email        VARCHAR(150) NOT NULL,
  vehicle_id   VARCHAR(20)  NOT NULL,
  otp_hash     VARCHAR(255) NOT NULL,          -- bcrypt hash of the 6-digit code
  expires_at   DATETIME     NOT NULL,           -- NOW() + 5 minutes
  used         TINYINT(1)   NOT NULL DEFAULT 0,
  attempts     INT          NOT NULL DEFAULT 0,
  lockout_until DATETIME    DEFAULT NULL,       -- set when attempts >= 5
  created_at   DATETIME     DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_email_vehicle (email, vehicle_id),
  INDEX idx_expires (expires_at)
);

-- Activity log
CREATE TABLE IF NOT EXISTS lock_logs (
  id           INT AUTO_INCREMENT PRIMARY KEY,
  vehicle_id   VARCHAR(20)  NOT NULL,
  action       VARCHAR(100) NOT NULL,          -- e.g. "Vehicle Unlocked", "OTP Failed"
  method       VARCHAR(30)  DEFAULT NULL,      -- otp | pin | qr | system
  performed_by VARCHAR(150) DEFAULT NULL,      -- email or "System"
  status       ENUM('success','failed','info') DEFAULT 'info',
  created_at   DATETIME     DEFAULT CURRENT_TIMESTAMP,
  INDEX idx_vehicle_time (vehicle_id, created_at)
);

-- Seed data — one demo vehicle + demo user
INSERT IGNORE INTO vehicles (id, vehicle_name, plate, is_locked)
VALUES ('VH-001', 'Toyota Innova Crysta', 'KA-01-AB-1234', 1);

INSERT IGNORE INTO users (name, email)
VALUES ('Demo User', 'demo@drivego.com');