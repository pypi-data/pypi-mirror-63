=====
audyo
=====

Python audio manager

Description
===========

Simple i/o package for "audio things". You can easily record a phrase or play audio files.


Note
====

import audyo.microphone.Microphone

recorder = new Microphone(out_file='file.wav') 

recorder.record_to_file() # this will wait until the recording is complete

import audyo.speaker.Speaker

Speaker.play('file.wav') # this will play audio file


AUDYO-CLI
=========
Microphone object can record until silence is detected.
This package provide two terminal commands:

- audyo-rec: This command will record until silence to default "audyo.wav" file. (output parameter will be released soon)
- audyo-play: This command will play audio file passed by parameter (will be released soon)
