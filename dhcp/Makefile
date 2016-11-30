SHELL := /bin/sh
SRCDIR := dhcp
SRCFILES := $(shell find $(SRCDIR) -type f)
TARFILE := dhcpd.tar.bz2


$(TARFILE) : $(SRCFILES)
	cd $(SRCDIR) && tar caf "$$OLDPWD/$(TARFILE)" --exclude '.*' *


.PHONY : upload
upload : $(TARFILE)
	scp $(TARFILE) root@provd.wazo.community:/var/www/provd.wazo.community/xivo/dhcpd-update/13.17


.PHONY : clean
clean :
	rm -f $(TARFILE)
