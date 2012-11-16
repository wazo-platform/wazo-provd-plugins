SHELL := /bin/sh
PGBUILD := ./pgbuild.py

BUILDDIR := _build
PLUGINS_PATH := $(BUILDDIR)/plugins
DEV_PATH := $(BUILDDIR)/dev
STABLE_PATH := $(BUILDDIR)/stable

REMOTE_HOST := provd.xivo.fr
REMOTE_USER := root
REMOTE_DEV_PATH := /var/www/provd.xivo.fr/plugins/1/testing
REMOTE_STABLE_PATH := /var/www/provd.xivo.fr/plugins/1/stable


.PHONY : build
build :
	rm -rf $(PLUGINS_PATH) $(DEV_PATH)
	mkdir -p $(PLUGINS_PATH) $(DEV_PATH)
	$(PGBUILD) -B -s . -d $(PLUGINS_PATH)
	$(PGBUILD) -P -s $(PLUGINS_PATH) -d $(DEV_PATH)
	$(PGBUILD) -D -s $(DEV_PATH) -d $(DEV_PATH)
	chmod +r $(DEV_PATH)/*


.PHONY : upload
upload : build
	rsync -v -rt --delete $(DEV_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_DEV_PATH)


.PHONY : download-stable
download-stable :
	rsync -v -rt --delete $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_STABLE_PATH)/ $(STABLE_PATH)


.PHONY : build-stable
build-stable :
	$(PGBUILD) -D -s $(STABLE_PATH) -d $(STABLE_PATH)
	chmod +r $(STABLE_PATH)/*


.PHONY : upload-stable
upload-stable : build-stable
	rsync -v -rt --delete $(STABLE_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_STABLE_PATH)


.PHONY : clean
clean :
	rm -rf $(BUILDDIR)/*
