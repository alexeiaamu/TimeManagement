CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    lunch_break BOOLEAN,
    consultant_id integer NOT NULL,
    consultant_name VARCHAR(255),
    customer_id integer NOT NULL,
    customer_name VARCHAR(255)
);

INSERT INTO entries (start_time, end_time, lunch_break, consultant_name, customer_name, consultant_id, customer_id) 
            VALUES ('2024-11-5 09:10:00', '2024-11-5 17:10:00', TRUE, 'Konsultti1', 'Asiakas1', 1, 1);

INSERT INTO entries (start_time, end_time, lunch_break, consultant_name, customer_name, consultant_id, customer_id)
            VALUES ('2024-11-5 09:15:00', '2024-11-5 16:10:00', FALSE, 'Konsultti2', 'Asiakas2', 2, 2);

INSERT INTO entries (start_time, end_time, lunch_break, consultant_name, customer_name, consultant_id, customer_id)
            VALUES ('2024-11-5 07:10:00', '2024-11-5 16:10:00', TRUE, 'Konsultti3', 'Asiakas1', 3, 1);

CREATE TABLE total_hours (
    id SERIAL PRIMARY KEY,
    consultant_id INT,
    total_hours FLOAT
);
