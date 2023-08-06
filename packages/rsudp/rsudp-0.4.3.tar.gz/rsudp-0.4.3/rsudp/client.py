import sys, os
import signal
import getopt
import time
import json
import re
import logging
from queue import Queue
from rsudp import printM, printW, printE, default_loc, init_dirs, output_dir, add_debug_handler, start_logging
from rsudp import COLOR
import rsudp.test as t
import rsudp.raspberryshake as rs
from rsudp.packetize import packetize
from rsudp.c_consumer import Consumer
from rsudp.p_producer import Producer
from rsudp.c_printraw import PrintRaw
from rsudp.c_write import Write
from rsudp.c_plot import Plot, MPL
from rsudp.c_forward import Forward
from rsudp.c_alert import Alert
from rsudp.c_alertsound import AlertSound
from rsudp.c_custom import Custom
from rsudp.c_tweet import Tweeter
from rsudp.c_telegram import Telegrammer
from rsudp.c_testing import Testing
from rsudp.t_testdata import TestData
import pkg_resources as pr
import fnmatch
try:
	from pydub import AudioSegment
	PYDUB_EXISTS = True
except ImportError:
	PYDUB_EXISTS = False


DESTINATIONS, THREADS = [], []
PROD = False
PLOTTER = False
SOUND = False
TESTING = False
TESTQUEUE = False
TESTFILE = pr.resource_filename('rsudp', os.path.join('test', 'testdata'))
SENDER = 'Main'

def handler(sig, frame):
	'''
	Function passed to :py:func:`signal.signal` to handle close events
	'''
	rs.producer = False

def _xit(code=0):
	'''
	End the program. Called after all running threads have stopped.

	:param int code: The process code to exit with. 0=OK, 1=ERROR.
	'''
	if TESTING:
		TESTQUEUE.put(b'ENDTEST')
	for thread in THREADS:
		del thread
	
	printM('Shutdown successful.', sender=SENDER)
	print()
	sys.exit(code)

def test_mode(mode=None):
	'''
	Sets the TESTING global variable to ``True`` to indicate that
	testing-specific actions should be taken in routines.

	:param bool mode: if ``True`` or ``False``, sets testing mode state. if anything else, returns state only.
	:return: testing mode state
	:rtype: bool
	'''
	global TESTING
	if (mode == True) or (mode == False):
		TESTING = mode
	return TESTING

def print_stats():
	s = 'Main'
	printW('Initialization stats:', s, announce=False)
	printW('                Port: %s' % rs.port, sender=SENDER, announce=False)
	printW('  Sending IP address: %s' % rs.firstaddr, sender=SENDER, announce=False)
	printW('    Set station name: %s' % rs.stn, sender=SENDER, announce=False)
	printW('  Number of channels: %s' % rs.numchns, sender=SENDER, announce=False)
	printW('  Transmission freq.: %s ms/packet' % rs.tf, sender=SENDER, announce=False)
	printW('   Transmission rate: %s packets/sec' % rs.tr, sender=SENDER, announce=False)
	printW('  Samples per second: %s sps' % rs.sps, sender=SENDER, announce=False)
	if rs.inv:
		printW('           Inventory: %s' % rs.inv.get_contents()['stations'][0],
			   sender=SENDER, announce=False)



def mk_q():
	'''
	Makes a queue and appends it to the :py:data:`destinations`
	variable to be passed to the master consumer thread
	:py:class:`rsudp.c_consumer.Consumer`.

	:rtype: queue.Queue
	:return: Returns the queue to pass to the sub-consumer.
	'''
	q = Queue(rs.qsize)
	DESTINATIONS.append(q)
	return q

def mk_p(proc):
	'''
	Appends a process to the list of threads to start and stop.

	:param threading.Thread proc: The process thread to append to the list of threads.
	'''
	THREADS.append(proc)


def start():
	'''
	Start Consumer, Threads, and Producer.
	'''
	global PROD, PLOTTER, THREADS, DESTINATIONS
	# master queue and consumer
	queue = Queue(rs.qsize)
	cons = Consumer(queue, DESTINATIONS)
	cons.start()

	for thread in THREADS:
		thread.start()

	PROD = Producer(queue, THREADS)
	PROD.start()

	if PLOTTER and MPL:
		# give the plotter the master queue
		# so that it can issue a TERM signal if closed
		PLOTTER.master_queue = queue
		# start plotting (in this thread, not a separate one)
		PLOTTER.run()
	else:
		while not PROD.stop:
			time.sleep(0.1) # wait until processes end


	time.sleep(0.5) # give threads time to exit
	PROD.stop = True


def run(settings, debug):
	'''
	Main setup function. Takes configuration values and passes them to
	the appropriate threads and functions.

	:param dict settings: settings dictionary (see :ref:`defaults` for guidance)
	:param bool debug: whether or not to show debug output (should be turned off if starting as daemon)
	'''
	global PLOTTER, SOUND
	# handler for the exit signal
	signal.signal(signal.SIGINT, handler)

	if TESTING:
		global TESTQUEUE
		# initialize the test data to read information from file and put it on the port
		TESTQUEUE = Queue()		# separate from client library because this is not downstream of the producer
		tdata = TestData(q=TESTQUEUE, data_file=TESTFILE, port=settings['settings']['port'])
		tdata.start()

	# initialize the central library
	rs.initRSlib(dport=settings['settings']['port'],
				 rsstn=settings['settings']['station'])

	if TESTING:
		t.TEST['n_port'][1] = True	# port has been opened
		print_stats()
		if rs.sps == 0:
			printE('There is already a Raspberry Shake sending data to this port.', sender=SENDER)
			printE('For testing, please change the port in your settings file to an unused one.',
					sender=SENDER, spaces=True)
			_xit(1)


	output_dir = settings['settings']['output_dir']


	if settings['printdata']['enabled']:
		# set up queue and process
		q = mk_q()
		prnt = PrintRaw(q)
		mk_p(prnt)

	if settings['write']['enabled']:
		# set up queue and process
		cha = settings['write']['channels']
		q = mk_q()
		writer = Write(q=q, cha=cha)
		mk_p(writer)

	if settings['plot']['enabled'] and MPL:
		while True:
			if rs.numchns == 0:
				time.sleep(0.01)
				continue
			else:
				break
		cha = settings['plot']['channels']
		sec = settings['plot']['duration']
		spec = settings['plot']['spectrogram']
		full = settings['plot']['fullscreen']
		kiosk = settings['plot']['kiosk']
		screencap = settings['plot']['eq_screenshots']
		alert = settings['alert']['enabled']
		if settings['plot']['deconvolve']:
			if settings['plot']['units'].upper() in rs.UNITS:
				deconv = settings['plot']['units'].upper()
			else:
				deconv = 'CHAN'
		else:
			deconv = False
		pq = mk_q()
		PLOTTER = Plot(cha=cha, seconds=sec, spectrogram=spec,
						fullscreen=full, kiosk=kiosk, deconv=deconv, q=pq,
						screencap=screencap, alert=alert)
		# no mk_p() here because the plotter must be controlled by the main thread (this one)

	if settings['forward']['enabled']:
		# put settings in namespace
		addr = settings['forward']['address']
		port = settings['forward']['port']
		cha = settings['forward']['channels']
		# set up queue and process
		q = mk_q()
		forward = Forward(addr=addr, port=port, cha=cha, q=q)
		mk_p(forward)

	if settings['alert']['enabled']:
		# put settings in namespace
		sta = settings['alert']['sta']
		lta = settings['alert']['lta']
		thresh = settings['alert']['threshold']
		reset = settings['alert']['reset']
		bp = [settings['alert']['highpass'], settings['alert']['lowpass']]
		cha = settings['alert']['channel']
		if settings['alert']['deconvolve']:
			if settings['alert']['units'].upper() in rs.UNITS:
				deconv = settings['alert']['units'].upper()
			else:
				deconv = 'CHAN'
		else:
			deconv = False

		# set up queue and process
		q = mk_q()
		alrt = Alert(sta=sta, lta=lta, thresh=thresh, reset=reset, bp=bp,
					 cha=cha, debug=debug, q=q,
					 deconv=deconv)
		mk_p(alrt)

	if settings['alertsound']['enabled']:
		sender = 'AlertSound'
		SOUND = False
		if PYDUB_EXISTS:
			soundloc = os.path.expanduser(os.path.expanduser(settings['alertsound']['mp3file']))
			if soundloc in ['doorbell', 'alarm', 'beeps', 'sonar']:
				soundloc = pr.resource_filename('rsudp', os.path.join('rs_sounds', '%s.mp3' % soundloc))
			if os.path.exists(soundloc):
				try:
					SOUND = AudioSegment.from_file(soundloc, format="mp3")
					printM('Loaded %.2f sec alert sound from %s' % (len(SOUND)/1000., soundloc), sender='AlertSound')
				except FileNotFoundError as e:
					printW("You have chosen to play a sound, but don't have ffmpeg or libav installed.", sender='AlertSound')
					printW('Sound playback requires one of these dependencies.', sender='AlertSound', spaces=True)
					printW("To install either dependency, follow the instructions at:", sender='AlertSound', spaces=True)
					printW('https://github.com/jiaaro/pydub#playback', sender='AlertSound', spaces=True)
					printW('The program will now continue without sound playback.', sender='AlertSound', spaces=True)
					SOUND = False
			else:
				printW("The file %s could not be found." % (soundloc), sender='AlertSound')
				printW('The program will now continue without sound playback.', sender='AlertSound', spaces=True)
		else:
			printW("You don't have pydub installed, so no sound will play.", sender='AlertSound')
			printW('To install pydub, follow the instructions at:', sender='AlertSound', spaces=True)
			printW('https://github.com/jiaaro/pydub#installation', sender='AlertSound', spaces=True)
			printW('Sound playback also requires you to install either ffmpeg or libav.', sender='AlertSound', spaces=True)

		q = mk_q()
		alsnd = AlertSound(q=q, sound=SOUND, soundloc=soundloc)
		mk_p(alsnd)

	runcustom = False
	try:
		if settings['custom']['enabled']:
			# put settings in namespace
			f = settings['custom']['codefile']
			win_ovr = settings['custom']['win_override']
			if f == 'n/a':
				f = False
			runcustom = True
	except KeyError as e:
		if settings['alert']['exec'] != 'eqAlert':
			printW('the custom code function has moved to its own module (rsudp.c_custom)', sender='Custom')
			f = settings['alert']['exec']
			win_ovr = settings['alert']['win_override']
			runcustom = True
		else:
			raise KeyError(e)
	if runcustom:
		# set up queue and process
		q = mk_q()
		cstm = Custom(q=q, codefile=f, win_ovr=win_ovr)
		mk_p(cstm)


	if settings['tweets']['enabled']:
		consumer_key = settings['tweets']['api_key']
		consumer_secret = settings['tweets']['api_secret']
		access_token = settings['tweets']['access_token']
		access_token_secret = settings['tweets']['access_secret']
		tweet_images = settings['tweets']['tweet_images']

		q = mk_q()
		tweet = Tweeter(q=q, consumer_key=consumer_key, consumer_secret=consumer_secret,
						access_token=access_token, access_token_secret=access_token_secret,
						tweet_images=tweet_images)
		mk_p(tweet)

	if settings['telegram']['enabled']:
		token = settings['telegram']['token']
		chat_id = settings['telegram']['chat_id']
		send_images = settings['telegram']['send_images']

		q = mk_q()
		telegram = Telegrammer(q=q, token=token, chat_id=chat_id,
							   send_images=send_images)
		mk_p(telegram)

	# start additional modules here!
	################################


	################################

	if TESTING:
		# initialize test consumer
		q = mk_q()
		test = Testing(q=q)
		mk_p(test)


	# start the producer, consumer, and activated modules
	start()

	PLOTTER = False
	if not TESTING:
		_xit()
	else:
		printW('Client has exited, ending tests...', sender=SENDER, announce=False)
		if SOUND:
			t.TEST['d_pydub'][1] = True


def dump_default(settings_loc, default_settings):
	'''
	Dumps a default settings file to a specified location.

	:param str settings_loc: The location to create the new settings JSON.
	:param str default_settings: The default settings to dump to file.
	'''
	if not TESTING:
		print('Creating a default settings file at %s' % settings_loc)
	with open(settings_loc, 'w+') as f:
		f.write(default_settings)
		f.write('\n')

	if TESTING:
		return True


def default_settings(output_dir='%s/rsudp' % os.path.expanduser('~').replace('\\', '/'), verbose=True):
	'''
	Returns a formatted json string of default settings.

	:param str output_dir: the user's specified output location. defaults to ``~/rsudp``.
	:param bool verbose: if ``True``, displays some information as the string is created.
	:return: default settings string in formatted json
	:rtype: str
	'''
	def_settings = r"""{
"settings": {
    "port": 8888,
    "station": "Z0000",
    "output_dir": "%s",
    "debug": true},
"printdata": {
    "enabled": false},
"write": {
    "enabled": false,
    "channels": ["all"]},
"plot": {
    "enabled": true,
    "duration": 30,
    "spectrogram": true,
    "fullscreen": false,
    "kiosk": false,
    "eq_screenshots": false,
    "channels": ["HZ", "HDF"],
    "deconvolve": false,
    "units": "CHAN"},
"forward": {
    "enabled": false,
    "address": "192.168.1.254",
    "port": 8888,
    "channels": ["all"]},
"alert": {
    "enabled": true,
    "channel": "HZ",
    "sta": 6,
    "lta": 30,
    "threshold": 1.7,
    "reset": 1.6,
    "highpass": 0,
    "lowpass": 50,
    "deconvolve": false,
    "units": "VEL"},
"alertsound": {
    "enabled": false,
    "mp3file": "doorbell"},
"custom": {
    "enabled": false,
    "codefile": "n/a",
    "win_override": false},
"tweets": {
    "enabled": false,
    "tweet_images": true,
    "api_key": "n/a",
    "api_secret": "n/a",
    "access_token": "n/a",
    "access_secret": "n/a"},
"telegram": {
    "enabled": false,
    "send_images": true,
    "token": "n/a",
    "chat_id": "n/a"}
}

""" % (output_dir)
	if verbose:
		print('By default output_dir is set to %s' % output_dir)
	return def_settings

def read_settings(settings_loc):
	settings_loc = os.path.abspath(os.path.expanduser(settings_loc)).replace('\\', '/')
	if os.path.exists(settings_loc):
		with open(settings_loc, 'r') as f:
			try:
				data = f.read().replace('\\', '/')
				settings = json.loads(data)
			except Exception as e:
				print(COLOR['red'] + 'ERROR: Could not load settings file. Perhaps the JSON is malformed?' + COLOR['white'])
				print(COLOR['red'] + '       detail: %s' % e + COLOR['white'])
				print(COLOR['red'] + '       If you would like to overwrite and rebuild the file, you can enter the command below:' + COLOR['white'])
				print(COLOR['bold'] + '       shake_client -d %s' % a + COLOR['white'])
				exit(2)
	else:
		print(COLOR['red'] + 'ERROR: could not find the settings file you specified. Check the path and try again.' + COLOR['white'])
		print()
		exit(2)
	return settings


def main():
	'''
	Loads settings to start the main client.
	Supply -h from the command line to see help text.
	'''
	settings_loc = os.path.join(default_loc, 'rsudp_settings.json').replace('\\', '/')

	hlp_txt='''
###########################################
##     R A S P B E R R Y  S H A K E      ##
##              UDP Client               ##
##            by Ian Nesbitt             ##
##            GNU GPLv3 2020             ##
##                                       ##
## Do various tasks with Shake data      ##
## like plot, trigger alerts, and write  ##
## to miniSEED.                          ##
##                                       ##
##  Requires:                            ##
##  - numpy, obspy, matplotlib 3, pydub  ##
##                                       ##
###########################################

Usage: rs-client [ OPTIONS ]
where OPTIONS := {
    -h | --help
            display this help message
    -d | --dump=default or /path/to/settings/json
            dump the default settings to a JSON-formatted file
    -s | --settings=/path/to/settings/json
            specify the path to a JSON-formatted settings file
    }

rs-client with no arguments will start the program with
settings in %s
''' % settings_loc


	settings = json.loads(default_settings(verbose=False))

	# get arguments
	try:
		opts = getopt.getopt(sys.argv[1:], 'hid:s:',
			['help', 'install', 'dump=', 'settings=']
			)[0]
	except Exception as e:
		print(COLOR['red'] + 'ERROR: %s' % e + COLOR['white'])
		print(hlp_txt)

	if len(opts) == 0:
		if not os.path.exists(settings_loc):
			print(COLOR['yellow'] + 'Could not find rsudp settings file, creating one at %s' % settings_loc + COLOR['white'])
			dump_default(settings_loc, default_settings())
		else:
			with open(os.path.abspath(settings_loc), 'r') as f:
				try:
					data = f.read().replace('\\', '/')
					settings = json.loads(data)
				except Exception as e:
					print(COLOR['red'] + 'ERROR: Could not load default settings file from %s' % settings_loc + COLOR['white'])
					print(COLOR['red'] + '       detail: %s' % e + COLOR['white'])
					print(COLOR['red'] + '       Either correct the file, or overwrite the default settings file using the command:' + COLOR['white'])
					print(COLOR['bold'] + '       shake_client -d default' + COLOR['white'])
					exit(2)

	for o, a in opts:
		if o in ('-h', '--help'):
			print(hlp_txt)
			exit(0)
		if o in ('-i', '--install'):
			'''
			This is only meant to be used by the install script.
			'''
			os.makedirs(default_loc, exist_ok=True)
			dump_default(settings_loc, default_settings(output_dir='@@DIR@@', verbose=False))
			exit(0)
		if o in ('-d', '--dump='):
			'''
			Dump the settings to a file, specified after the `-d` flag, or `-d default` to let the software decide where to put it.
			'''
			if str(a) in 'default':
				os.makedirs(default_loc, exist_ok=True)
				dump_default(settings_loc, default_settings())
			else:
				dump_default(os.path.abspath(os.path.expanduser(a)), default_settings())
			exit(0)
		if o in ('-s', 'settings='):
			'''
			Start the program with a specific settings file, for example: `-s settings.json`.
			'''
			settings = read_settings(a)

	start_logging()
	debug = settings['settings']['debug']
	if debug:
		add_debug_handler()
		printM('Logging initialized successfully.', sender=SENDER)

	printM('Using settings file: %s' % settings_loc)

	odir = os.path.abspath(os.path.expanduser(settings['settings']['output_dir']))
	init_dirs(odir)
	if debug:
		printM('Output directory is: %s' % odir)

	run(settings, debug=debug)

def test():
	'''
	.. versionadded:: 0.4.3

	Set up tests, run modules, report test results.
	For a list of tests run, see :py:mod:`rsudp.test`.
	'''
	global TESTFILE
	hlp_txt='''
###########################################
##     R A S P B E R R Y  S H A K E      ##
##            Testing Module             ##
##            by Ian Nesbitt             ##
##            GNU GPLv3 2020             ##
##                                       ##
## Test settings with archived Shake     ##
## data to determine optimal             ##
## configuration.                        ##
##                                       ##
##  Requires:                            ##
##  - numpy, obspy, matplotlib 3         ##
##                                       ##
###########################################

Usage: rs-test [ OPTIONS ]
where OPTIONS := {
    -h | --help
            display this help message
    -f | --file=default or /path/to/data/file
            specify the path to a seismic data file
    -s | --settings=/path/to/settings/json
            specify the path to a JSON-formatted settings file
    }

rs-test with no arguments will start the test with
default settings and the data file at
%s
''' % (TESTFILE)

	test_mode(True)
	settings = default_settings(verbose=False)
	settings_are_default = True

	try:
		opts = getopt.getopt(sys.argv[1:], 'hf:s:',
			['help', 'file=', 'settings=']
			)[0]
	except Exception as e:
		print(COLOR['red'] + 'ERROR: %s' % e + COLOR['white'])
		print(hlp_txt)
		exit(1)

	for o, a in opts:
		if o in ('-h', '--help'):
			print(hlp_txt)
			exit(0)
		if o in ('-f', '--file='):
			'''
			The data file.
			'''
			a = os.path.expanduser(a)
			if os.path.exists(a):
				try:
					out = '%s.txt' % (a)
					packetize(inf=a, outf=out)
					TESTFILE = out
				except Exception as e:
					print(COLOR['red'] + 'ERROR: %s' % e + COLOR['white'])
					print(hlp_txt)
					exit(1)
		if o in ('-s', '--settings='):
			'''
			Dump the settings to a file, specified after the `-d` flag, or `-d default` to let the software decide where to put it.
			'''
			settings_loc = os.path.abspath(os.path.expanduser(a)).replace('\\', '/')
			if os.path.exists(settings_loc):
				settings = read_settings(settings_loc)
				settings_are_default = False
			else:
				print(COLOR['red'] + 'ERROR: could not find settings file at %s' % (a) + COLOR['white'])
				exit(1)

	t.TEST['n_internet'][1] = t.is_connected('www.google.com')

	if settings_are_default:
		settings = t.make_test_settings(settings=settings, inet=t.TEST['n_internet'][1])


	t.TEST['p_log_dir'][1] = t.logdir_permissions()
	t.TEST['p_log_file'][1] = start_logging(testing=True)
	t.TEST['p_log_std'][1] = add_debug_handler(testing=True)

	t.TEST['p_output_dirs'][1] = init_dirs(os.path.expanduser(settings['settings']['output_dir']))
	t.TEST['p_data_dir'][1] = t.datadir_permissions(os.path.expanduser(settings['settings']['output_dir']))
	t.TEST['p_screenshot_dir'][1] = t.ss_permissions(os.path.expanduser(settings['settings']['output_dir']))

	if MPL:
		t.TEST['d_matplotlib'][1] = True
	else:
		printW('matplotlib backend failed to load')

	run(settings, debug=True)

	TESTQUEUE.put(b'ENDTEST')
	printW('Test finished.', sender=SENDER, announce=False)

	print()

	code = 0
	printM('Test results:')
	for i in t.TEST:
		printM('%s: %s' % (t.TEST[i][0], t.TRANS[t.TEST[i][1]]))
		if not t.TEST[i][1]:
			# if a test fails, change the system exit code to indicate an error occurred
			code = 1
	_xit(code)


if __name__ == '__main__':
	main()
