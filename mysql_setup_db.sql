-- prepares a MySQL server for the project
CREATE DATABASE IF NOT EXISTS `heroes`;
CREATE USER IF NOT EXISTS 'levi'@'localhost' IDENTIFIED BY 'levipassword';
GRANT USAGE ON *.* TO 'levi'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'levi'@'localhost';
GRANT ALL PRIVILEGES ON `heroes`.* TO 'levi'@'localhost';
FLUSH PRIVILEGES;