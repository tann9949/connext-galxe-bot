CREATE DATABASE connext;

USE connext;

CREATE TABLE PolygonTransactions (
  id INT NOT NULL AUTO_INCREMENT,
  timestamp INT NOT NULL,
  chain INT NOT NULL,
  hash VARCHAR(255) NOT NULL,
  user_address VARCHAR(255) NOT NULL,
  token_address VARCHAR(255) NOT NULL,
  token_amount DOUBLE NOT NULL,
  action VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX user_token_index ON PolygonTransactions (user_address, token_address, chain);
CREATE TABLE ArbitrumTransactions (
  id INT NOT NULL AUTO_INCREMENT,
  timestamp INT NOT NULL,
  chain INT NOT NULL,
  hash VARCHAR(255) NOT NULL,
  user_address VARCHAR(255) NOT NULL,
  token_address VARCHAR(255) NOT NULL,
  token_amount DOUBLE NOT NULL,
  action VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX user_token_index ON ArbitrumTransactions (user_address, token_address, chain);
CREATE TABLE OptimismTransactions (
  id INT NOT NULL AUTO_INCREMENT,
  timestamp INT NOT NULL,
  chain INT NOT NULL,
  hash VARCHAR(255) NOT NULL,
  user_address VARCHAR(255) NOT NULL,
  token_address VARCHAR(255) NOT NULL,
  token_amount DOUBLE NOT NULL,
  action VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX user_token_index ON OptimismTransactions (user_address, token_address, chain);
CREATE TABLE BNBChainTransactions (
  id INT NOT NULL AUTO_INCREMENT,
  timestamp INT NOT NULL,
  chain INT NOT NULL,
  hash VARCHAR(255) NOT NULL,
  user_address VARCHAR(255) NOT NULL,
  token_address VARCHAR(255) NOT NULL,
  token_amount DOUBLE NOT NULL,
  action VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX user_token_index ON BNBChainTransactions (user_address, token_address, chain);
CREATE TABLE GnosisTransactions (
  id INT NOT NULL AUTO_INCREMENT,
  timestamp INT NOT NULL,
  chain INT NOT NULL,
  hash VARCHAR(255) NOT NULL,
  user_address VARCHAR(255) NOT NULL,
  token_address VARCHAR(255) NOT NULL,
  token_amount DOUBLE NOT NULL,
  action VARCHAR(255) NOT NULL,
  PRIMARY KEY (id)
);
CREATE INDEX user_token_index ON GnosisTransactions (user_address, token_address, chain);

CREATE TABLE Token (
  name VARCHAR(255) NOT NULL,
  symbol VARCHAR(255) NOT NULL,
  address VARCHAR(255) NOT NULL,
  `decimal` INT NOT NULL,
  chain INT NOT NULL,
  PRIMARY KEY (address, chain),
);
CREATE INDEX address_chain_index ON Token (address, chain);
