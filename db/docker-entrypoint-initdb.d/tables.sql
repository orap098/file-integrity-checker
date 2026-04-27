
CREATE TABLE hashes (
id SERIAL PRIMARY KEY,
path VARCHAR(255),
hash VARCHAR(255),
algoritmo VARCHAR(100),
data_criacao TIMESTAMP
);
