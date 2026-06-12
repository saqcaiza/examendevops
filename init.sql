CREATE TABLE IF NOT EXISTS productos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    precio NUMERIC(10, 2) NOT NULL,
    stock INT NOT NULL
);

INSERT INTO productos (nombre, precio, stock) VALUES
('Laptop Gamer', 1200.50, 10),
('Mouse Óptico', 25.00, 50),
('Teclado Mecánico', 85.00, 30),
('Monitor 24" 144Hz', 199.99, 15),
('Auriculares HyperX', 60.00, 25)
ON CONFLICT DO NOTHING;