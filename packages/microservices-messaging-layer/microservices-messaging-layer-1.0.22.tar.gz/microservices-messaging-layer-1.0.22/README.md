# Triskelion

## A Kafka Messaging helper for Microservices 

![](ermes.png)



# Service description


Triskelion provides your code with a helper for Kafka and Confluent Kafka producers. 
The end goal of this project is to become a messages communication layer for microservices.
However, The code is at its earlier stage and there is room for improvements. If you want to contribute to it please contact me at antonio.dimariano[AT]gmail.com
If you find a bug please submit it [here](https://github.com/antoniodimariano/kafka_messaging_layer/issues)

I would like to thank all the [Confluent Community on Slack](https://confluentcommunity.slack.com/archives/C49G1J750) for the priceless help during my learning path.


<a name="confluent_kafka_producer_configuration"><h1>Confluent Kafka Producer Configuration</h1></a>
 

 

# Brokers 

 ENV variables name  | VALUE                                                                                    |
|---------------------|------------------------------------------------------------------------------------------|
| brokers             | mybroker1:9093,mybroker2:9093,mybroker3:9093                                                |
| schema_registry     | http://my_avro_schema_registry:8081                                                    |


# SASL Identification 

Please refer to https://docs.confluent.io/3.0.0/kafka/sasl.html. 
If your broker requires SASL authentication, these are the ENVironment variables to include


| ENV variables name  | VALUE                                                                                    |
|---------------------|------------------------------------------------------------------------------------------|
| sasl_mechanisms     | PLAIN                                                                                   |
| security_protocol   | SASL_SSL                                                                                   |
| sasl_username   | YOUR USERNAME HERE                                                                                   |
| sasl_password   | YOUR PASSWORD HERE                                                                                   |


If you schema registry requires authentication, these are the ENVironment variables to include

| ENV variables name  | VALUE                                                                                    |
|---------------------|------------------------------------------------------------------------------------------|
| schema\_registry\_basic\_auth\_user_info     | authentication string                                                |
| schema\_registry\_basic\_auth\_credentials_source   | USER_INFO                                                    |


# SSL certificate for brokers and schema registry

If your brokers and schema registry servers require a SSL certificate, these are the 

| ENV variables name  | VALUE                                                                                    |
|---------------------|------------------------------------------------------------------------------------------|
| security_protocol     | ssl string                                                |

You have to place your certificate in 

# How to use it 


## Confluent Kafka Producer  

The `produce_message` method accepts a list of messages. Messages are dispatched asynchronously to the Kafka Broker
The module provides you with two different Producers' class. Both of them have a public method `producer_message`.
However, If your are working with AVRO topics, you have to do `from messaging_middleware.confluent_producer.AVROProducer import AVROPRODUCER`. 
Otherwise you can `from messaging_middleware.confluent_producer.ConfluentProducer import ConfluentProducer`
The following is an example how to produce a message in both cases.


```python
from messaging_middleware.confluent_producer.ConfluentProducer import ConfluentProducer
from messaging_middleware.confluent_producer.AVROProducer import AVROPRODUCER

import os
default_key_value = {"service_name":"test"}

class OutboundCommunicationLayer:

    def __init__(self,topic,brokers_uri,security_protocol='plaintext',schema_registry=None):
        print("OS:",os.environ.get('brokers'),os.environ.get('schema_registry'))

        if schema_registry is None:
            self.producer = ConfluentProducer(
                brokers_uri=brokers_uri,
                topic=topic, security_protocol=security_protocol)
        else:
            self.avro_producer = AVROPRODUCER(
                brokers_uri=brokers_uri,
                schema_registry_url=schema_registry,
                topic=topic, security_protocol=security_protocol)

    def produce_topic(self,value):
        self.producer.produce_message(message=value)

    def produce_avro_topic(self, value,key=default_key_value):

        self.avro_producer.produce_message(value=value, key=key)




if __name__ == "__main__":

    o = OutboundCommunicationLayer(topic='my-test-2',brokers_uri=os.environ.get('brokers'),schema_registry=os.environ.get('schema_registry'))
    o.produce_avro_topic(value={"my_text":"ciaociaociaociao"},key=default_key_value)

```


# Using Synchronous Producer

Even though it is not always the best practise and it has its issues (https://github.com/edenhill/librdkafka/wiki/FAQ#why-is-there-no-sync-produce-interface) , there is no harm to have a synchronous producer. 
The module provides you with two classes to 




## Integrated Logging System 

The  Logger class aims to be used to print log messages and/or to produce logging message to an AVRO topic.
It uses the AVRO_PRODUCER and by default it produces messages to the AVRO topic `tcservicesmonitor` with the following schema 
If you want to configure the Confluent Kafka producer, you have to pass a `init_kafka=1` when creating your instance.

```json
logger = Logger(init_kafka=1, brokers_uri=os.environ.get('brokers'),
                    schema_registry_url=os.environ.get('schema_registry_url'))
```
* tcservicesmonitor-value
```json
 {
        "service_name": "string",
        "last_operation": "string",
        "timestamp": "string",
        "operation_result": "string",
        "operation_description": "string",
        "error_description": "string"
    }
```

* tcservicesmonitor-key 
```json
"service_name": "string"}
```

If you want to use another topic you have to specify it in the ENV variable `monitoring_topic`

In order to use the Logging system, please refer to the configuration used to set up a [Confluent Kafka Producer](#confluent_kafka_producer_configuration)   


```python
import os
from messaging_middleware.Logger.Logger import Logger
from datetime import datetime, timezone
    
    logger = Logger(init_kafka=1, brokers_uri=os.environ.get('brokers'),
                    schema_registry_url=os.environ.get('schema_registry_url'))
    logger.print_log('info', 'My log ', 10)
    logger.print_log('debug', 'my second log')
    message_to_produce = {
        "service_name": "my-test-microservice",
        "last_operation": "last-completed-operation",
        "timestamp": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "operation_result": "SUCCESS",
        "operation_description": "The operation description",
        "error_description": ""
    }


    logger.produce_msg(message_to_produce=message_to_produce, schema_key={
        "service_name": "my-test-service"})
```

