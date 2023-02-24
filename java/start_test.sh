#!/bin/bash
nohup java -jar -Dspring.config.location=./application_test.yml sync.jar > test.log 2>&1 &
