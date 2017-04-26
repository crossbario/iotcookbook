.PHONY: start

build:
	docker build -t cookbook-gamepad -f Dockerfile .

start: build
	docker run -it --rm \
		--privileged \
		--net=host \
		-e CBURL='wss://demo.crossbar.io/ws' \
		-e CBREALM='crossbardemo' \
		cookbook-gamepad
