DROP DATABASE IF EXISTS ticket_selling;
CREATE DATABASE ticket_selling
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE ticket_selling;

-- =====================================================
-- USERS
-- =====================================================

CREATE TABLE users (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    full_name VARCHAR(100) NOT NULL,

    email VARCHAR(100) NOT NULL UNIQUE,

    password VARCHAR(255) NOT NULL,

    role ENUM(
        'ADMIN',
        'ORGANIZER',
        'CUSTOMER'
    ) NOT NULL,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- =====================================================
-- CUSTOMERS
-- =====================================================

CREATE TABLE customers (

    id BIGINT PRIMARY KEY,

    preferences TEXT,

    FOREIGN KEY (id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

-- =====================================================
-- EVENT CATEGORY
-- =====================================================

CREATE TABLE event_categories (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    name VARCHAR(100) NOT NULL
);

-- =====================================================
-- EVENTS
-- =====================================================

CREATE TABLE events (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    organizer_id BIGINT NOT NULL,

    category_id BIGINT,

    name VARCHAR(255) NOT NULL,

    banner VARCHAR(255),

    description TEXT,

    location VARCHAR(255),

    start_time DATETIME,

    end_time DATETIME,

    sale_start DATETIME,

    sale_end DATETIME,

    status ENUM(
        'ACTIVE',
        'LOCKED',
        'CANCELLED'
    ) DEFAULT 'ACTIVE',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (organizer_id)
        REFERENCES users(id),

    FOREIGN KEY (category_id)
        REFERENCES event_categories(id)
);

-- =====================================================
-- TICKET TYPES
-- =====================================================

CREATE TABLE ticket_types (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    event_id BIGINT NOT NULL,

    name VARCHAR(100) NOT NULL,

    description TEXT,

    price DECIMAL(12,2) NOT NULL,

    max_quantity INT NOT NULL,

    current_stock INT NOT NULL,

    FOREIGN KEY(event_id)
        REFERENCES events(id)
        ON DELETE CASCADE
);

-- =====================================================
-- DISCOUNT CODE
-- =====================================================

CREATE TABLE discount_codes (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    code VARCHAR(50) UNIQUE,

    type ENUM(
        'PERCENT',
        'FIXED'
    ),

    discount_value DECIMAL(10,2),

    max_usage INT,

    used_count INT DEFAULT 0,

    expired_at DATETIME
);

-- =====================================================
-- ORDERS
-- =====================================================

CREATE TABLE orders (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    customer_id BIGINT NOT NULL,

    discount_code_id BIGINT NULL,

    payment_method ENUM(
        'MOMO',
        'VNPAY'
    ),

    total DECIMAL(12,2),

    status ENUM(
        'PENDING',
        'PAID',
        'FAILED',
        'CANCELLED'
    ) DEFAULT 'PENDING',

    created_date DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(customer_id)
        REFERENCES customers(id),

    FOREIGN KEY(discount_code_id)
        REFERENCES discount_codes(id)
);

-- =====================================================
-- ORDER DETAILS
-- =====================================================

CREATE TABLE order_details (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    order_id BIGINT NOT NULL,

    ticket_type_id BIGINT NOT NULL,

    quantity INT NOT NULL,

    unit_price DECIMAL(12,2) NOT NULL,

    sub_total DECIMAL(12,2) NOT NULL,

    FOREIGN KEY(order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE,

    FOREIGN KEY(ticket_type_id)
        REFERENCES ticket_types(id)
);

-- =====================================================
-- PAYMENT
-- =====================================================

CREATE TABLE payments (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    order_id BIGINT UNIQUE,

    gateway ENUM(
        'MOMO',
        'VNPAY'
    ),

    transaction_code VARCHAR(255),

    amount DECIMAL(12,2),

    status ENUM(
        'PENDING',
        'SUCCESS',
        'FAILED'
    ),

    payment_time DATETIME,

    FOREIGN KEY(order_id)
        REFERENCES orders(id)
        ON DELETE CASCADE
);

-- =====================================================
-- TICKETS
-- =====================================================

CREATE TABLE tickets (

    id BIGINT AUTO_INCREMENT PRIMARY KEY,

    order_detail_id BIGINT NOT NULL,

    qr_code VARCHAR(255) UNIQUE,

    seat_number VARCHAR(50),

    attached_face_url VARCHAR(255),

    status ENUM(
        'UNUSED',
        'USED',
        'CANCELLED'
    ) DEFAULT 'UNUSED',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY(order_detail_id)
        REFERENCES order_details(id)
        ON DELETE CASCADE
);

-- =====================================================
-- INDEXES
-- =====================================================

CREATE INDEX idx_event_name
ON events(name);

CREATE INDEX idx_event_status
ON events(status);

CREATE INDEX idx_ticket_status
ON tickets(status);

CREATE INDEX idx_order_status
ON orders(status);

CREATE INDEX idx_payment_status
ON payments(status);

CREATE INDEX idx_discount_code
ON discount_codes(code);