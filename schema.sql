CREATE TABLE users (
    user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    telegram_id INT NOT NULL UNIQUE
    chat_id INT
);

CREATE TABLE user_balance_ops (
    user_id INT NOT NULL,
    opdate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    amount INT NOT NULL
);

CREATE TABLE user_keys (
    user_id INT NOT NULL,
    key_id INT UNIQUE,
    name VARCHAR(50) NOT NULL,
    start_date DATETIME NOT NULL,
    stop_date DATETIME NOT NULL
);

CREATE TABLE servers (
    server_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    country VARCHAR(64) NOT NULL
);

CREATE TABLE outline_keys (
    key_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    outline_key_id INT NOT NULL,
    server_id INT NOT NULL,
    key_value VARCHAR(255) NOT NULL,
    used TINYINT(1) NOT NULL
);
