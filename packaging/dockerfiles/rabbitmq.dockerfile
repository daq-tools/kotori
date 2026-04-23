FROM rabbitmq:4.3
RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_mqtt
