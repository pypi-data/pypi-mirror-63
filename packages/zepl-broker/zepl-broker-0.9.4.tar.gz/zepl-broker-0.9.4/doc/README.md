## MicroPython device example config
{
	"dut2": {
		"dev_ip": "192.168.0.87",	# required
		"dev_port": 8266,		# required
		"proto": "WebREPL",		# required
		"dev_pw": "asdf",		# required
		"dev_mac": "240ac444e2e4",	# optional (test app only)
		"fpath": "./mpy-scripts",	# optional, MicroPython scripts directory (relative to working dir of broker)
		"init_sync": false,		# required: sync directory without checking remote hashes
		"sync_flist": [			# self-explanatory
			"app_a.py",
			"app_b.py",
			"wifi_util.py",
			"wifi.secret",		# copy wifi.json for this
			"main.py",
			"boot.py"
		"init_run": "3"			# optional (test app only), initial 'app' to run
		],
	},
	...
}

## Dummy Workload for RaspberryPi

![](syn_load.png)

## ZeroMQ Model

#### Legend
* black arrows: flow of data
* orange: Hardware
* grey: coroutine
* boxes: logical blocks (e.g. classes)
* green: minimal example app

![](model.png)
