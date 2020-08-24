CREATE DATABASE py_temp;
CREATE TABLE readings(id INT NOT NULL AUTO_INCREMENT,temp INT NOT NULL,humidity INT NOT NULL,time DATE,PRIMARY KEY ( id ));
CREATE USER 'pythonuser'@'localhost' IDENTIFIED BY 'UEAkJFcwcmRQQCQkVzByZAo=';
GRANT ALL PRIVILEGES ON py_temp TO 'pythonuser'@'localhost';