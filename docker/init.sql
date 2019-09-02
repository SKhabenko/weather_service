CREATE TABLE IF NOT EXISTS logs
(
  log_level  varchar(8) NOT NULL,
  created_at timestamp DEFAULT current_timestamp,
  message    varchar(1024),
  details    varchar(1024)
);