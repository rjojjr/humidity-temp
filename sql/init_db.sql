CREATE DATABASE py_temp;
CREATE TABLE readings(id INT NOT NULL AUTO_INCREMENT,room VARCHAR(50),temp INT NOT NULL,room VARCHAR(50) humidity INT NOT NULL,time DATETIME,PRIMARY KEY ( id ));
CREATE USER 'pythonuser'@'localhost' IDENTIFIED BY 'UEAkJFcwcmRQQCQkVzByZAo=';
GRANT ALL PRIVILEGES ON py_temp TO 'pythonuser'@'localhost';