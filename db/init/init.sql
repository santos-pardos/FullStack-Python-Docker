CREATE TABLE IF NOT EXISTS accounts (
  id SERIAL PRIMARY KEY,
  owner_name VARCHAR(100) NOT NULL,
  balance NUMERIC(12,2) NOT NULL DEFAULT 0.00
);

CREATE TABLE IF NOT EXISTS transactions (
  id SERIAL PRIMARY KEY,
  account_id INTEGER NOT NULL REFERENCES accounts(id) ON DELETE CASCADE,
  amount NUMERIC(12,2) NOT NULL,
  kind VARCHAR(20) NOT NULL CHECK (kind IN ('deposit','withdrawal','transfer_in','transfer_out')),
  created_at TIMESTAMP NOT NULL DEFAULT NOW(),
  note TEXT
);

INSERT INTO accounts (owner_name, balance) VALUES
('Alice', 1200.50),
('Bob', 560.00);

INSERT INTO transactions (account_id, amount, kind, note) VALUES
(1, 1200.50, 'deposit', 'Initial funding'),
(2, 560.00, 'deposit', 'Initial funding');
