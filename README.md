# Trashy Image Recognition

(Born out of Hackathon 2019)

A basic image recognition tool to determine if your trash is recyclable or not.

Currently hosted on:
https://trashy-image-recognition.herokuapp.com

Tensorflow's Inception v3 [model](https://github.com/tensorflow/models)  is used for image recognition.
It has been slightly modified for our use. Any credit for brilliance belongs to Tensorflow, 
and every mistake is mine.

[NEA](https://www.nea.gov.sg/docs/default-source/our-services/waste-management/list-of-items-that-are-recyclable-and-not.pdf), 
MEWR and zerowastesg's list of recyclables and non-recyclables is used for 
classification of trash.

## Instructions
1. Run `python classify_trash/get_list_of_recyclables.py` to get list of recyclables from MEWR and zerowastesg.

2. Run `python classify_trash/update_classification.py` to update classifications with customized labels.
