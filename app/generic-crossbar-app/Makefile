MAKE_CLIENT_CERT=utils/make_client_ssl.py
MAKE_SERVER_CERT=utils/make_server_ssl.py
RUN_MS=microservice_template/micro_service.py
RUN_AUTH=components/security.py
RUN_LOGGER=components/logger.py

.PHONY: dirs dhparam client_certs server_certs
.PHONY: clean_server clean_client run_microservices kill_microservices

all:
	@echo 'No default action'

rebuild: dirs clean_server clean_client server_certs client_certs dhparam

dirs:
	@echo 'Make sure "certs" exists'
	@mkdir -p certs

dhparam:
	@echo 'Rebuilding "dhparam", this takes quite a while!'
	@echo 'Please consider a 4096 key for production'
	openssl dhparam -2 2048 >certs/dhparam.pem

client_certs:
	@${MAKE_CLIENT_CERT} --host node1
	@${MAKE_CLIENT_CERT} --host node2
	@${MAKE_CLIENT_CERT} --host node3
	@${MAKE_CLIENT_CERT} --host node4
	@${MAKE_CLIENT_CERT} --host node5
	@${MAKE_CLIENT_CERT} --host auth1
	@${MAKE_CLIENT_CERT} --host auth2
	@${MAKE_CLIENT_CERT} --host log1
	@${MAKE_CLIENT_CERT} --host log2

server_certs:
	@${MAKE_SERVER_CERT} --weeks 4

clean: clean_client clean_server

clean_client:
	@echo "Cleaning client certificates"
	@rm -f certs/client_*

clean_server:
	@echo "Cleaning server certificates"
	@rm -f certs/server_*

run_auth:
	PYTHONPATH="." ${RUN_AUTH} --profile=profiles/auth1.ini &
	PYTHONPATH="." ${RUN_AUTH} --profile=profiles/auth2.ini &

run_logger:
	PYTHONPATH="." ${RUN_LOGGER} --profile=profiles/log1.ini &
	PYTHONPATH="." ${RUN_LOGGER} --profile=profiles/log2.ini &

run_microservices:
	PYTHONPATH="." ${RUN_MS} --profile=profiles/profile1.ini && sleep 1 &
	PYTHONPATH="." ${RUN_MS} --profile=profiles/profile2.ini && sleep 1 &
	PYTHONPATH="." ${RUN_MS} --profile=profiles/profile3.ini && sleep 1 &
	PYTHONPATH="." ${RUN_MS} --profile=profiles/profile4.ini && sleep 1 &
	PYTHONPATH="." ${RUN_MS} --profile=profiles/profile5.ini && sleep 1 &

kill_application:
	kill `ps ax | grep xbr_application|cut -c 1-6`

kill_auth:
	kill `ps ax | grep xbr_auth|cut -c 1-6`

kill_logger:
	kill `ps ax | grep xbr_logger|cut -c 1-6`
