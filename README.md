# Issue 50313 - Memory Leak

Trying to reproduce https://github.com/saltstack/salt/issues/50313

To make this work, clone the repo and run:

```
docker-compose up -d
docker exec salt-50313-master salt-key -A -y
```

This will start the salt master and minion, and accept the keys on the master.
Then let's start tracking things:

```
python track.py
```

You can view a <strike>pretty</strike> graph in the browser with

```
python3 -m http.server
```
