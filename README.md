1. For local development use doker-compose.local.yml:
doker-compose -f doker-compose.local.yml up

It will run containers with Kafka and Postgres.

To check that messages are got by Consumer you can go inside the kafka container itself and run the command:
afka-console-consumer.sh --topic topic_1 --bootstrap-server localhost:9092

2. To run the whole system use: doker-compose -f docker-compose.yml up

It will run Producer and Consumer. 
You should see in log how messages are sent by Producer and that after the message is got, it is written to DB.

3. to run tests use command: coverage run --source core/ -m unittest discover -s test/ && coverage report -m

It should be run for each module
