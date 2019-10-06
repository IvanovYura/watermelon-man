# OS Metrics Generator 

## Description

There is a metrics generator with Kafka as a stream platform (queue) and Postgres as DB.
It has two packages: `metrics_generator` and `metrics_consumer`, to produce messages and consume/write to DB consequently.

Metrics to collect:
- memory (free, available, used)
- disk usage (free, percent, used)
- cpu usage in percent (default metric)

To get help message and read how to setup arguments:
```shell
python metrics_generator/core/producer.py --help
```

## How to run

1. Specify environment variables. See the [Development](##development) section.
2. Run the command:
```shell
doker-compose -f docker-compose.yml up
```

It will run Producer and Consumer. 
You should see in log how messages are sent by Producer and that after the message is got, it is written to DB.

To check that data is really written to DB, connect to Postgress (either in container or your local):
```shell 
psql <db_host:db_port> -U <db_user> <db_name>
```

Check by SQL query:

```sql
SELECT * FROM os_metrics;
```

## Development 

To develop each part of the system, generator or consumer, it has to be done separatly.
Each directory has its own `Pipfile*` and `Dockerfile`.

To install all dependencies (and set up virtual environment), i.e. for `metrics_generator`:
```shell
python -m pipenv install
```

Also environment variables should be specified:
```shell
export KAFKA_BROKER_URL=<kafka_broker_url> &&
export KAFKA_TOPIC=<kafka_topic> &&
export DB_HOST=<db_host> &&
export DB_NAME=<db_name> &&
export DB_PORT=<db_port> &&
export DB_USER=<db_user> &&
export DB_PASSWORD=<db_password>
```

For *local development*:

run docker-compose:
```shell 
doker-compose -f doker-compose.local.yml up
```

It will run Kafka instances with Zookeeper and Postgres.

To check that messages are really sent to Kafka (for example if there is not Consumer) inside the Kafka container run the command:
```shell
kafka-console-consumer.sh --topic <topic_name> --bootstrap-server localhost:9092
```
Where `<topic_name>` is the topic specified to send messages by Porducer.

## Testing

To run unit tests use for `metrics_generator` or `metrics_consumer`:
```shell
coverage run --source core/ -m unittest discover -s test/ && coverage report -m
```

## List with useful links

* psutil doc: https://psutil.readthedocs.io/en/latest/
* Kafka Producer/Consumer CLI: https://cleanprogrammer.net/running-kafka-producer-and-consumer-from-command-line/
* How to set up Kafka Producer: https://help.aiven.io/en/articles/489572-getting-started-with-aiven-kafka
* Kafka-Python: https://kafka-python.readthedocs.io/en/master/usage.html
