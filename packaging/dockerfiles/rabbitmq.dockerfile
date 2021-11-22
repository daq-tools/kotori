FROM rabbitmq:3.9
RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_mqtt
