TOP = ../..

include $(TOP)/configure/CONFIG

DATA    =  colors.dl template.dl \
           $(patsubst ../%.adl, %.dl, $(wildcard ../*.adl ../*.bit ../*.cfg ../*.tk ../*.test))

SCRIPTS_HOST  += $(wildcard ../*.sh)

include $(TOP)/configure/RULES

%.dl: ../%.adl
	$(RM) $@
	-$(ADL2DL) $< >/dev/null

%.dl: %.adl
	$(RM) $@
	-$(ADL2DL) $< >/dev/null
