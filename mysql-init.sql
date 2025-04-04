CREATE TABLE IF NOT EXISTS my_table (
    firstName VARCHAR(50),
    lastName VARCHAR(50),
    email VARCHAR(50),
    phoneNumber VARCHAR(15)
);

INSERT INTO my_table (firstName, lastName, email, phoneNumber) VALUES
('John', 'Doe', 'john@doe.com', '0123456789'),
('Jane', 'Doe', 'jane@doe.com', '9876543210'),
('James', 'Bond', 'james.bond@mi6.co.uk', '0612345678');

