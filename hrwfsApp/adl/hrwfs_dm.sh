#!/bin/csh -f

setenv EPICS_DISPLAY_PATH .:$GEMINI_TOP/share/dl/hrwfs
dm2-4 -iconic wfs_main.dl "top=hrwfs:, sadtop=hrwfs" &
