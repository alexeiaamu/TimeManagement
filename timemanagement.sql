CREATE TABLE entries (
    id SERIAL PRIMARY KEY,
    start_time TIMESTAMP,
    end_time TIMESTAMP,
    lunch_break BOOLEAN,
    consultant_name VARCHAR(255),
    customer_name VARCHAR(255)
);

INSERT INTO entries (start_time, end_time, lunch_break, consultant_name, customer_name)
            VALUES ('2024-11-5 09:10:00', '2024-11-5 17:10:00', TRUE, 'Konsultti1', 'Asiakas1');

INSERT INTO entries (start_time, end_time, lunch_break, consultant_name, customer_name)
            VALUES ('2024-11-5 09:15:00', '2024-11-5 16:10:00', FALSE, 'Konsultti2', 'Asiakas2');

INSERT INTO entries (start_time, end_time, lunch_break, consultant_name, customer_name)
            VALUES ('2024-11-5 07:10:00', '2024-11-5 16:10:00', TRUE, 'Konsultti3', 'Asiakas1');