-- Create Customer table
CREATE TABLE Customer (
    email VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    name VARCHAR(50) NOT NULL,
    building_num VARCHAR(20),
    street VARCHAR(100),
    city VARCHAR(50),
    state VARCHAR(50),
    phone_num VARCHAR(10),
    passport_number VARCHAR(50),
    passport_expiration DATE,
    passport_country VARCHAR(50),
    date_of_birth DATE
);

-- Create Airport table
CREATE TABLE Airport (
    Airport_id VARCHAR(10) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(50) NOT NULL,
    country VARCHAR(50) NOT NULL
);

-- Create Airline table
CREATE TABLE Airline (
    Name VARCHAR(50) PRIMARY KEY
);

-- Create Airplane table
CREATE TABLE Airplane (
    Airline_name VARCHAR(50),
    id VARCHAR(20),
    num_seats INTEGER NOT NULL,
    manufacturing_co VARCHAR(50),
    PRIMARY KEY (Airline_name, id),
    FOREIGN KEY (Airline_name) REFERENCES Airline(Name)
);

-- Create Flight table
CREATE TABLE Flight (
    Airline_Name VARCHAR(50),
    flight_no VARCHAR(20),
    departure_date_and_time DATETIME,
    departure_airport_id VARCHAR(10) NOT NULL,
    arrival_airport_id VARCHAR(10) NOT NULL,
    arrival_date_and_time DATETIME NOT NULL,
    status VARCHAR(20) NOT NULL,
    base_price DECIMAL(10,2) NOT NULL,
    Airplane_airline_name VARCHAR(50),
    Airplane_id VARCHAR(20),
    PRIMARY KEY (Airline_Name, flight_no, departure_date_and_time),
    FOREIGN KEY (departure_airport_id) REFERENCES Airport(Airport_id),
    FOREIGN KEY (arrival_airport_id) REFERENCES Airport(Airport_id),
    FOREIGN KEY (Airplane_airline_name, Airplane_id) REFERENCES Airplane(Airline_name, id),
    FOREIGN KEY (Airline_Name) REFERENCES Airline(Name)
);

-- Create Ticket table
CREATE TABLE Ticket (
    ticket_id VARCHAR(20) PRIMARY KEY,
    sold_price DECIMAL(10,2) NOT NULL,
    card_type VARCHAR(20),
    card_num VARCHAR(20),
    name_on_card VARCHAR(50),
    card_expiry_date DATE,
    Airline_name VARCHAR(50),
    flight_no VARCHAR(20),
    departure_date_and_time DATETIME,
    FOREIGN KEY (Airline_name, flight_no, departure_date_and_time) 
        REFERENCES Flight(Airline_Name, flight_no, departure_date_and_time)
);

-- Create Purchases table
CREATE TABLE Purchases (
    ticket_id VARCHAR(20),
    email VARCHAR(50),
    date_and_time DATETIME NOT NULL,
    PRIMARY KEY (ticket_id, email),
    FOREIGN KEY (ticket_id) REFERENCES Ticket(ticket_id),
    FOREIGN KEY (email) REFERENCES Customer(email)
);

-- Create Airline Staff table
CREATE TABLE Airline_Staff (
    username VARCHAR(50) PRIMARY KEY,
    password VARCHAR(50) NOT NULL,
    f_name VARCHAR(50) NOT NULL,
    l_name VARCHAR(50) NOT NULL,
    date_of_birth DATE,
    Airline_name VARCHAR(50),
    FOREIGN KEY(Airline_name) REFERENCES Airline(Name)
);

-- Create Phone_num table for Airline Staff
CREATE TABLE Phone_num (
    username VARCHAR(50),
    phone_num VARCHAR(10),
    PRIMARY KEY (username, phone_num),
    FOREIGN KEY (username) REFERENCES Airline_Staff(username)
);

-- Create Email table for Airline Staff
CREATE TABLE Email (
    username VARCHAR(50),
    email VARCHAR(50),
    PRIMARY KEY (username, email),
    FOREIGN KEY (username) REFERENCES Airline_Staff(username)
);

-- Create Review table
CREATE TABLE Review (
    email VARCHAR(100),
    Airline_Name VARCHAR(50),
    flight_no VARCHAR(20),
    departure_date_and_time DATETIME,
    rate INTEGER NOT NULL,
    comment TEXT,
    PRIMARY KEY (email, Airline_Name, flight_no, departure_date_and_time),
    FOREIGN KEY (email) REFERENCES Customer(email),
    FOREIGN KEY (Airline_Name, flight_no, departure_date_and_time) 
        REFERENCES Flight(Airline_Name, flight_no, departure_date_and_time)
);
