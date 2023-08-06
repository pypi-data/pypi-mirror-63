# Zepl Broker
install:
```
pip install zepl-broker
```

# quick test
issue all commands in the same terminal!

start the broker, log listener and dummy in the background
```
$ zepl-broker &
-- Starting Zepl Broker --

$ zepl-client log &
-- Starting Zepl Client --

$ zepl-client -d --config dummy.json ctrl add &
-- Starting Zepl Client --
ZeplDevice initialized.
Added dummy1: :  [b'success']
```

say hello!
```
$ zepl-client -d dev greet dummy1
-- Starting Zepl Client --
greeting dummy1 runner -- :  [b'why hello there!']
greeting dummy1 device -- :  [b'not sure if...']
b'dummy1' -- b'DUMMY_DEV_RAW_OUT' --  b'why hello there!'
```

kill them all
```
$ kill $(jobs -p)
[1]   Terminated              zepl-broker
[2]-  Terminated              zepl-client log
[3]+  Terminated              zepl-client -d --config dummy.json ctrl add
```

for more see: [examples](examples/) and [doc](doc/)

## caveat
at this moment the command line tool is very picky about the arguments
