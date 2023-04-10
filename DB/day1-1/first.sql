CREATE TABLE contacts (
    name TEXT NOT NULL,
    age INTEGER NOT NULL,   
    email TEXT NOT NULL UNIQUE
);

ALTER TABLE contacts RENAME TO new_contacts;
ALTER TABLE new_contacts RENAME COLUMN email TO new_email;

CREATE TABLE users (
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    age INTEGER NOT NULL,
    country TEXT NOT NULL,
    phone TEXT NOT NULL,
    balance INTEGER NOT NULL
);

SELECT country FROM users;


DROP TABLE new_contacts;

SELECT first_name, age, balance FROM users WHERE age>=30 AND balance>500000;
SELECT first_name, last_name FROM users WHERE first_name LIKE '%준';
SELECT first_name, last_name FROM users WHERE first_name LIKE '%호%';
SELECT first_name, phone FROM users WHERE phone LIKE '02-%';
SELECT first_name, age FROM users WHERE age LIKE '2_';
SELECT first_name, phone FROM users WHERE phone LIKE '%-51__-%';
SELECT first_name, country FROM users WHERE country IN('경기도', '강원도');
SELECT first_name, country FROM users WHERE country NOT IN ('경기도', '강원도');
SELECT first_name, age FROM users WHERE age BETWEEN 20 AND 30;
SELECT first_name, age FROM users WHERE age NOT BETWEEN 20 AND 30;
SELECT rowid, first_name FROM users LIMIT 10;
SELECT first_name, balance FROM users ORDER BY balance DESC LIMIT 10;
SELECT first_name, age FROM users ORDER BY age LIMIT 5;

SELECT DISTINCT country FROM users;
SELECT country,  avg(age) FROM users GROUP BY country ORDER BY avg(age);

SELECT first_name, age, balance FROM users ORDER BY age, balance DESC;
SELECT first_name, age FROM users ORDER BY first_name, age DESC;

SELECT first_name, country FROM users WHERE first_name='건우' AND country='경기도';
SELECT * FROM users WHERE country NOT IN ('경기도', '강원도') AND age BETWEEN 20 AND 30 ORDER BY age;

SELECT first_name, phone FROM users WHERE phone LIKE '%-51__-%' AND NOT country='서울';
