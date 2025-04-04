CREATE TABLE my_table (
    id SERIAL PRIMARY KEY,
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(100),
    phoneNumber VARCHAR(15)
);

INSERT INTO my_table (firstName, lastName, email, phoneNumber) VALUES
('John', 'Doe', 'john@doe.com', '0123456789'),
('Jane', 'Doe', 'jane@doe.com', '9876543210'),
('James', 'Bond', 'james.bond@mi6.co.uk', '0612345678');

