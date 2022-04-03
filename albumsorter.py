#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sys import exit,argv
from os import rename,listdir
from os.path import isdir,exists,join
from mutagen.id3 import ID3
from mutagen.flac import FLAC

known_formats = ['.mp3','.flac']

#----------------------------------------------------------------------
class tagObject:
	def __init__(self, file_path):
		self.VA = False
		if file_path[-4:] == ".mp3":
			self.extension = "mp3"
			# print("Extracting ID3: ")
			audio = ID3(file_path)
			# print("Encoding " + audio['TIT2'].encoding)
			self.artist = audio['TPE1'].text[0]
			self.title = audio['TIT2'].text[0]
			self.trackno = audio['TRCK'].text[0]
			self.trackno = self.trackno.replace('/','-')
			try:
				if audio['TPE2'].text[0] == 'Various Artists': self.VA = True
			except KeyError:
				pass
		if file_path[-5:] == ".flac":
			self.extension = "flac"
			# print("Extracting FLAC")
			audio = FLAC(file_path)
			self.artist = audio['artist'][0]
			self.title = audio['title'][0]
			self.trackno = audio['tracknumber'][0]
			try:
				if int(audio['totaldiscs'][0]) > 1:
					print("it's multiCD!")
					self.trackno = audio['discnumber'][0] + "-" + self.trackno
			except KeyError:
				pass
		
#----------------------------------------------------------------------
def search_songs(curr_dir):
	# print("Current directory: " + curr_dir)
	for file_name in listdir(curr_dir):
		file = join(curr_dir,file_name)
		if isdir(file): search_songs(file)
		for format in known_formats:
			if format == file[-len(format):]:
				print("Found " + file)
				song = tagObject(file)
				print(song.trackno + " – " + song.title + "." + song.extension)
				break

#----------------------------------------------------------------------

target_dir = argv[1]
if not isdir(target_dir):
	print("Not a directory!")
	exit()
	
search_songs(target_dir)

