#!/bin/env python3
from pathlib import Path
import shutil
import os

out_directory = Path("sdcard")
splitcmd = \
	'mp3splt -t "{track_length}>00.30" -a -p min={min_silence_length} {file} -d {outdir} -o @n3'

struct = {
	1 : {
		"dir" : "Hörbücher/WeihnachtenMitJuli",	
		"mode" : "Hörbuch",
		"min_silence_length" : 1.0,
		"track_length" : "02.00",
	},
	2 : {
		"dir" : "Hörspiele/MeineErstenMinutenGeschichten_Tiere",
		"mode" : "Hörspiel",
	},
	3 : {
		"dir" : [ "Musik/Kinderlieder Vol.1  SWR2", "Musik/Kinderlieder Vol.2  SWR2" ],
		"mode" : "Party",
	},
}

out_directory.mkdir(exist_ok=True)

for outdir, config in struct.items():
	outdir = out_directory / "{:02d}".format(outdir)
	outdir.mkdir( exist_ok = True )
	print("Mapping Input Folder", config["dir"], "to SDCard Folder", outdir)
	is_not_empty = any( outdir.iterdir() )
	if is_not_empty:
		print(f"{outdir}", "not empty, skipping" )
		continue
		
	# create list of files in input directory
	files=[]
	if isinstance(config["dir"], list):
		for d in config["dir"]:
			flist = Path( d ).glob("*mp3")
			flist = sorted([ x for x in flist if x.is_file() ])
			files += flist
	else:
		files = Path( config["dir"] ).glob("*")
		files = sorted([ x for x in files if x.is_file() ])
		
	if config["mode"] == "Hörbuch":
		# Split file in dir using mp3splt
		# only 1 file should be present in Hörbuch mode
		if len(files) > 1:
			print("More then one file in Hörbuch mode, skipping")
			continue
		for file in files:
			config["outdir"] = outdir
			config["file"] = file
			os.system( splitcmd.format( **config ))
		
	elif config["mode"] == "Hörspiel" or config["mode"] == "Party":
		# only copy files and rename
		for num, infile in enumerate(files):
			outfile = "{:03d}.mp3".format( num+1 )
			outfile = outdir / outfile
			print("Copy", infile, "to", outfile)
			shutil.copy( infile, outfile )

		
