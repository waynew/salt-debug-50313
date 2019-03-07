#!/bin/bash
# Sync gitfs
/usr/bin/salt-run saltutil.sync_all

# This may be redundant, but ensure we sync the
# engines after we've got the latest code from gitfs
/usr/bin/salt-run saltutil.sync_engines

touch /tmp/entrypoint_ran

# Ensure that the saltapi password matches the
# $SALTAPI_PASSWORD environment variable
stty -echo
if [ -n "$SALTAPI_PASSWORD" ];
    then echo ${SALTAPI_PASSWORD} |  passwd --stdin saltapi;
fi
stty echo

# Run command
exec "$@"
