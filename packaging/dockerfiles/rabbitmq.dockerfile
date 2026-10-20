FROM rabbitmq:4.4
RUN rabbitmq-plugins enable --offline rabbitmq_management rabbitmq_mqtt
