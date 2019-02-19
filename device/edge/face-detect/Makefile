.PHONY: crossbar crossbar-pypy camera-streamer face-detector view-finder

crossbar:
	crossbar start --cbdir crossbar

crossbar-pypy:
	crossbar start --cbdir crossbar

camera-streamer:
	python3 -u camera-streamer/main.py

face-detector:
	python3 -u face-detector/main.py

view-finder:
	xdg-open frontend/index.html
