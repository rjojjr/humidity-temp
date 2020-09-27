CREATE DATABASE py_temp;
CREATE TABLE readings(id INT NOT NULL AUTO_INCREMENT,room VARCHAR(50),temp INT NOT NULL, humidity INT NOT NULL,time DATETIME,PRIMARY KEY ( id ));
CREATE TABLE notifications(id INT NOT NULL AUTO_INCREMENT,uuid VARCHAR(50),type VARCHAR(50),message VARCHAR(300), sent VARCHAR(1), subject VARCHAR(100), recipients VARCHAR(1000),generated_time DATETIME,sent_time DATETIME,PRIMARY KEY ( id ));
CREATE USER 'pythonuser'@'localhost' IDENTIFIED BY 'UEAkJFcwcmRQQCQkVzByZAo=';
GRANT ALL PRIVILEGES ON py_temp.readings TO 'pythonuser'@'localhost';
CREATE USER 'pythonuser'@'192.168.1.167' IDENTIFIED BY 'UEAkJFcwcmRQQCQkVzByZAo=';
GRANT ALL PRIVILEGES ON py_temp.readings TO 'pythonuser'@'192.168.1.167';
GRANT ALL PRIVILEGES ON py_temp.notifications TO 'pythonuser'@'localhost';

"select * from readings where time between '2020/08/25 17:00:00' and '2020/08/25 00:00:00';"