#!/bin/bash
nohup java -jar -Dspring.config.location=./application_pro.yml sync.jar > pro.log 2>&1 &
