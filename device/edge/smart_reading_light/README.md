# Smart Reading Light

This is a project started by members of the [IoT Meetup Franken](https://www.meetup.com/de-DE/IoT-Meetup-Franken/), a local meetup of tinkerers in Erlangen, Germany.

Anybody is welcome to participate!

## Project idea

Intelligent lighting for reading in bed.

Turns on when a book is openend in a reading position.

Tracks the position of the book and adjusts a spotlight based on this.

Once the book is closed, slowly dims the lighting.


### Benefit over a non-smart reading lamp

Ability to use very focused, local light while still being able to re-position the book while reading.

Natural control model.


## Hardware:

* LED spotlight
* Holder for this, can move spotlight in 2 dimensions
* Camera  


## Tracking situation:

* Relatively darker room
* Reading normal printed book: mainly white paper, darker print
* Light is focused enough to allow reading sitting beside a partner in bed and not disturb the partner
* The reading light is installed in a permanent position
* Position is probably slightly to one side and above the reader


# Problems

* What if the reading is in bed with white bedsheets, or on a sofa with a white carpet?
* Turning on/off - Turning on cannot be via the camera, since we have a low light situation initially


# Version 1 prototype

* Reading light with fade-out after the book is closed

* simple code for capturing a sequence of images is in "acquire_training_images.py" - use to generate example images of book reading and closing


# Development coordination

- here on GitHub (file and comment on issues, pull requests)
- on request you can be added to a slack channel and get access to online storage for test images (mail to alexander.goedde@crossbario.com)

# Future features

* Light remembers the last read page in book  

--- 

to do:

- get the book shape recogintion working, e.g. based on https://pythontips.com/2015/03/11/a-guide-to-finding-books-in-images-using-python-and-opencv/
- find a way to differentiate the Pi (starter kit) from the book, should both be recognized
- differentiate open book and closed book based on ratios of sides

# Reading materials

- https://pythontips.com/2015/03/11/a-guide-to-finding-books-in-images-using-python-and-opencv/
- https://docs.opencv.org/3.4/dc/d88/tutorial_traincascade.html

