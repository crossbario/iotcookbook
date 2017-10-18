.PHONY: start

build:
	docker build -t cookbook-camera -f Dockerfile .

start: build
	docker run -it --rm \
		--device /dev/ttyAMA0 \
		--device /dev/mem \
		--device /dev/gpiomem \
		--privileged \
		--net=host \
		-e CBURL='wss://demo.crossbar.io/ws' \
		-e CBREALM='crossbardemo' \
		cookbook-camera

autostart: build
	docker run --detach \
		--restart=always \
		--name button \
		--device /dev/ttyAMA0 \
		--device /dev/mem \
		--device /dev/gpiomem \
		--privileged \
		--net=host \
		-e CBURL='wss://demo.crossbar.io/ws' \
		-e CBREALM='crossbardemo' \
		cookbook-camera
