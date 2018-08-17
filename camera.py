from picamera import PiCamera
from os import path, listdir, remove
from shutil import disk_usage
from time import sleep
import json
from datetime import datetime
from sendmail import Mail


def getresolution():
	"""
	Get resolution for video recording
	:return: A dictionnary {"width": x, "height":y}
	"""
	res = {}
	with open('config.json') as f:
		data = json.load(f)
		res = data["resolution"]  # type: dict
		return res


def gethome():
	"""
	Get video save folder.
	:return: a string containing a path
	"""
	with open('config.json') as f:
		data = json.load(f)
		homepath = data["home"]   # type: str
		return homepath


def getframerate():
	"""
	Get the number of frame per second from the
	:return: an integer representing the number of frame per second.
	"""
	with open('config.json') as f:
		data = json.load(f)
		frm = data["framerate"]  # type: int
		return frm


def gettimestamp():
	"""
	Get the desired choice regarding having a timestamp or not
	:return: an integer between 0 and 1
	"""
	with open('config.json') as f:
		data = json.load(f)
		tm = data["timestamp"]  # type: int
		return tm


def getcameraname():
	"""
	Get the desired camera name provided in the saved video filename
	:return: a string containing the camera name
	"""
	with open('config.json') as f:
		data = json.load(f)
		name = data["cameraname"]  # type: str
		return name
	
	
def getvideolength():
	"""
	Get the length of each video file.
	:return: an integer representing the number of seconds
	"""
	with open('config.json') as f:
		data = json.load(f)
		length = data["videolength"] * 60  # type: int
		return length


def formatfilename():
	"""
	Get the name of the current file
	:return: string containing the name of the file
	"""
	cameraname = getcameraname()
	date = datetime.now()
	date_in_second = int(date.strftime('%s'))
	formateddate = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
	filename = cameraname + '_' + str(date_in_second) + '_' + formateddate + '.h264'
	return filename


# Get config
home = gethome()
resolution = getresolution()
framerate = getframerate()
timestamp = gettimestamp()
videolength = getvideolength()

# Init PiCamera
camera = PiCamera()
camera.resolution = (resolution["width"], resolution["height"])
camera.framerate = framerate

if timestamp == 1:
	camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	
sleep(2)
mailstarted = Mail()
mailstarted.webcamstarted()

# Run
while True:
	filepath = home + formatfilename()
	total_bytes, used_bytes, free_bytes = disk_usage(path.realpath(home))
	free_bytes = free_bytes / 1000000000
	
	if free_bytes < 5.0:
		filelist = listdir(home)
		remove(filelist[0])
	start = datetime.now()
	
	try:
		if timestamp == 1:
			camera.start_recording(filepath)
			while (datetime.now() - start).seconds < videolength:
				camera.annotate_text = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
				camera.wait_recording(0.2)
		else:
			camera.start_recording(filepath)
			camera.wait_recording(videolength)
		camera.stop_recording()
	except Exception:
		mailerror = Mail()
		mailerror.webcamerror()
