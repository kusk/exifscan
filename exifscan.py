import exifread
import os
import time
import sys, getopt

def ifslash(tal):
	splitted = tal.split("/")
	if (splitted[0] == str(0)) and (splitted[1] == str(0)):
		return 0
	else: 
		sum = int(float(splitted[0]) /  float("0." + splitted[1]))
		return str(sum)[0:2] + "." + str(sum)[2:6]

def whole(tallene, way):
	if "/" in tallene[0]:
		tallene[0] = ifslash(tallene[0])
	if "/" in tallene[1]:
		tallene[1] = ifslash(tallene[1])
	if "/" in tallene[2]:
		tallene[2] = ifslash(tallene[2])
	
	if (way == "S") or (way == "W"):
		way = "-"
	else:
		way = "+"

	return way + str(tallene[0]) + "." + str((float(tallene[1]) / 60) + (float(tallene[2]) / 3600)).replace(".", "")[1:6]
def main(argv):
	start = time.time()
	output = ""
	output+= '<?xml version="1.0" encoding="UTF-8"?>\n'
	output+= '<kml xmlns="http://www.opengis.net/kml/2.2">\n'
	output+= '<Document>\n'
	c = 0 # Count of all pictures
	cc = 0 # Count of pictures with EXIF+GPS

	try:
		opts, args = getopt.getopt(argv,"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print 'exifscan.py -o <output KML-file> -i <directory>'
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print 'exifscan.py -o <output KML-file> -i <directory>'
			print "\t-i\t Directory you want to scan. Will also scan subdirs"
			print "\t-o\t Filename for KML-file you want to output. Will overwrite existing file\n"
			print "exifscan - A python script that scan pictures for GPS-coordinates and outputs them to KML"
			print "v0.1 - Created by Anders Kusk - anderskusk@gmail.com"
			sys.exit()
		elif opt in ("-o", "--output"):
			output_file = arg
		elif opt in ("-i", "--input"):
			dir = arg



	
	try:
		dir
	except NameError:
		print 'exifscan.py -o <output KML-file> -i <directory>'
	else:
		for root, directories, filenames in os.walk(dir):
			

			#print '<?xml version="1.0" encoding="UTF-8"?>'
			#print '<kml xmlns="http://www.opengis.net/kml/2.2">'
			#print "<Document>"
			for directory in directories:
				os.path.join(root, directory) 
			for filename in filenames: 
				f = open(os.path.join(root,filename))
				tags = exifread.process_file(f)
				exifdata = tags
				gps = str(tags)
				c = c + 1
				if 'GPSLong' in gps:
					cc = cc + 1
					#file_out = open(output_file, "w")
					#print "GPS GPSLatitudeRef: " + str(exifdata['GPS GPSLatitudeRef'])
					#print "GPS GPSLongitudeRef: " + str(exifdata['GPS GPSLongitudeRef'])
					#print "GPSLongitude: " + str(exifdata['GPS GPSLongitude'])
					#print "GPSLatitude: " + str(exifdata['GPS GPSLatitude'])
					#print exifdata
					#print "<Placemark>"
					output+= "<Placemark>\n"
					output+= "\t<name>" + filename + "</name>\n"
					output+= "\t<description>" + root + "</description>\n"
					output+= "\t<Point>\n"
					output+= "\t\t<coordinates>"



					# coordinat = ["12", "35", "3072/125"]
					test =  str(exifdata['GPS GPSLongitude'])
					test = test.replace("[","")
					test = test.replace("]","")
					sane = test.split(", ")
					output+= whole(sane, str(exifdata['GPS GPSLongitudeRef']))
					output+= ","

					test =  str(exifdata['GPS GPSLatitude'])
					test = test.replace("[","")
					test = test.replace("]","")
					sane = test.split(", ")
					output+= whole(sane, str(exifdata['GPS GPSLatitudeRef']))
					output+= "</coordinates>\n\t</point>\n</Placemark>\n"


		output+= "</Document>\n</kml>"
		file_out = open(output_file, "w")
		file_out.write(output)
		file_out.close()



		print "Pictures searched for EXIF GPS metadata: " + str(c)
		print "Pictures with EXIF GPS metadata found: " + str(cc)
		print 'Processing took', time.time()-start, 'seconds.'

if __name__ == "__main__":
   main(sys.argv[1:])