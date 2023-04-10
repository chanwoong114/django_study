CREATE TABLE animal (
    animal_name TEXT  NOT NULL,
    height INTEGER NOT NULL,
    weight INTEGER NOT NULL,
    age INTEGER NOT NULL
);

ALTER TABLE animal ADD COLUMN meal TEXT;
ALTER TABLE animal RENAME COLUMN animal_name TO name;

DROP TABLE animal;
