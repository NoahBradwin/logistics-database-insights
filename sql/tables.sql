CREATE TABLE customers (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	email VARCHAR(150) NOT NULL,
	phone VARCHAR(20),
	address text NOT NULL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE drivers (
	id SERIAL PRIMARY KEY,
	name VARCHAR(100) NOT NULL,
	license_number VARCHAR(50) UNIQUE NOT NULL,
	phone VARCHAR(20) NOT NULL,
	is_active BOOLEAN DEFAULT TRUE
);

CREATE TABLE packages (
	id SERIAL PRIMARY KEY,
	tracking_number VARCHAR(50) UNIQUE NOT NULL,
	sender_id INT REFERENCES customers(id) NOT NULL,
	recipient_id INT REFERENCES customers(id) NOT NULL,
	weight_kg DECIMAL(10, 2),
	assigned_driver_id INT REFERENCES drivers(id),
	current_status package_status DEFAULT 'created',
	estimated_delivery DATE,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE tracking_events (
	id SERIAL PRIMARY KEY,
	package_id INT REFERENCES packages(id) ON DELETE CASCADE,
	status package_status NOT NULL,
	event_location TEXT,
	notes TEXT,
	event_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
)