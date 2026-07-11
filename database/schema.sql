CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('Restaurant','NGO','Delivery','Admin') NOT NULL,
    phone VARCHAR(15),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE ngo (
    ngo_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    ngo_name VARCHAR(100) NOT NULL,
    capacity INT,
    location VARCHAR(255),
    CONSTRAINT fk_ngo_user
        FOREIGN KEY (user_id)
        REFERENCES users(user_id)
);

CREATE TABLE restaurants (
    restaurant_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT UNIQUE,
    restaurant_name VARCHAR(100) NOT NULL,
    license_no VARCHAR(50),
    location VARCHAR(255),
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE food (
    food_id INT AUTO_INCREMENT PRIMARY KEY,
    restaurant_id INT,
    food_name VARCHAR(100) NOT NULL,
    quantity INT NOT NULL,
    food_type ENUM('Veg','Non-Veg'),
    cooked_at DATETIME,
    expiry_time DATETIME,
    status ENUM('Available','Accepted','Delivered') DEFAULT 'Available',
    FOREIGN KEY (restaurant_id) REFERENCES restaurants(restaurant_id)
);

CREATE TABLE requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    food_id INT,
    ngo_id INT,
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status ENUM('Pending','Accepted','Rejected') DEFAULT 'Pending',
    FOREIGN KEY (food_id) REFERENCES food(food_id),
    FOREIGN KEY (ngo_id) REFERENCES ngo(ngo_id)
);

CREATE TABLE deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT,
    partner_id INT,
    pickup_time DATETIME,
    delivery_time DATETIME,
    status ENUM('Assigned','Picked Up','Delivered') DEFAULT 'Assigned',
    FOREIGN KEY (request_id) REFERENCES requests(request_id),
    FOREIGN KEY (partner_id) REFERENCES users(user_id)
);

CREATE TABLE history (
    history_id INT AUTO_INCREMENT PRIMARY KEY,
    food_id INT,
    ngo_id INT,
    delivery_id INT,
    completed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (food_id) REFERENCES food(food_id),
    FOREIGN KEY (ngo_id) REFERENCES ngo(ngo_id),
    FOREIGN KEY (delivery_id) REFERENCES deliveries(delivery_id)
);
