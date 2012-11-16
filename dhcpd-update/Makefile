SHELL := /bin/sh
SRCDIR := dhcp
SRCFILES := $(shell find $(SRCDIR) -type f)
TARFILE := dhcpd.tar.bz2


$(TARFILE) : $(SRCFILES)
	cd $(SRCDIR) && tar caf "$$OLDPWD/$(TARFILE)" *


.PHONY : upload
upload : $(TARFILE)
	scp $(TARFILE) root@provd.xivo.fr:/var/www/provd.xivo.fr/xivo/dhcpd-update/1.2


.PHONY : clean
clean :
	rm -f $(TARFILE)
