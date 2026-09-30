#!/bin/bash
# Dev-container-only environment. gemini-rtsw-ci/dev_environment.sh sources this
# file, diffs the environment before and after, and forwards only the variables
# it *changed* into the container as -e arguments. It is never installed by the
# RPM and never read at runtime, so nothing here can affect a real workstation.
#
# This file is not specific to any one module: a dev image ships the package's
# RPM but none of the gemsoft site environment a workstation gets from its own
# profile, so every DM screen repo needs the same two variables. Copy it to the
# root of a new one as-is.

# Root of the gemsoft tree. The <mod><SITE>_dm.sh scripts build
# EPICS_DISPLAY_PATH from it; unset, that collapses to "/share/dl/<mod>" and
# dm2-4 starts but finds no screens.
export GEMINI_TOP=/gemsoft

# Which site's screens <mod>_dm.sh dispatches to: MK or CP.
export GEMINI_SITE=MK

# The site broadcast addresses baked into the per-site scripts are not reachable
# from a container, so PVs stay disconnected (white). Point this at a local soft
# IOC to get live values; leave it alone to just check screen layout.
# export EPICS_CA_ADDR_LIST=127.0.0.1
# export EPICS_CA_AUTO_ADDR_LIST=NO
