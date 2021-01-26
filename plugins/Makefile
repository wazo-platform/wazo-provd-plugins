SHELL := /bin/sh
PGBUILD := ./pgbuild.py

BUILDDIR := _build
PLUGINS_PATH := $(BUILDDIR)/plugins
TESTING_PATH := $(BUILDDIR)/testing
STABLE_PATH := $(BUILDDIR)/stable
ARCHIVE_PATH := $(BUILDDIR)/archive
FIRMWARES_PATH := _firmwares

REMOTE_HOST := webserver.wazo.community
REMOTE_USER := root
REMOTE_TESTING_PATH := /var/www/provd/plugins/1/testing
REMOTE_STABLE_PATH := /var/www/provd/plugins/1/stable
REMOTE_ARCHIVE_PATH := /var/www/provd/plugins/1/archive
REMOTE_FIRMWARES_PATH := /var/www/provd/firmwares


.PHONY : download
download :
	mkdir -p $(TESTING_PATH)
	rsync -v -rt --delete $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_TESTING_PATH)/ $(TESTING_PATH)

.PHONY : build
build :
	rm -rf $(PLUGINS_PATH) $(TESTING_PATH)
	mkdir -p $(PLUGINS_PATH) $(TESTING_PATH)
	$(PGBUILD) -B -s . -d $(PLUGINS_PATH)
	$(PGBUILD) -P -s $(PLUGINS_PATH) -d $(TESTING_PATH)
	$(PGBUILD) -D -s $(TESTING_PATH) -d $(TESTING_PATH)
	chmod +r $(TESTING_PATH)/*


.PHONY : upload
upload : build
	rsync -v -rt --delete $(TESTING_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_TESTING_PATH)


.PHONY : download-stable
download-stable :
	mkdir -p $(STABLE_PATH)
	rsync -v -rt --delete $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_STABLE_PATH)/ $(STABLE_PATH)


.PHONY : build-stable
build-stable :
	$(PGBUILD) -D -s $(STABLE_PATH) -d $(STABLE_PATH)
	chmod +r $(STABLE_PATH)/*


.PHONY : upload-stable
upload-stable : build-stable
	rsync -v -rt --delete $(STABLE_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_STABLE_PATH)


.PHONY : download-archive
download-archive :
	mkdir -p $(ARCHIVE_PATH)
	rsync -v -rt --delete $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_ARCHIVE_PATH)/ $(ARCHIVE_PATH)


.PHONY : build-archive
build-archive :
	$(PGBUILD) -D -s $(ARCHIVE_PATH) -d $(ARCHIVE_PATH)
	chmod +r $(ARCHIVE_PATH)/*


.PHONY : upload-archive
upload-archive : build-archive
	rsync -v -rt --delete $(ARCHIVE_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_ARCHIVE_PATH)


.PHONY : download-firmwares
download-firmwares :
	mkdir -p $(FIRMWARES_PATH)
	rsync -v -rt $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_FIRMWARES_PATH)/ $(FIRMWARES_PATH)


.PHONY : upload-firmwares
upload-firmwares:
	rsync -v -rt $(FIRMWARES_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_FIRMWARES_PATH)


.PHONY : clean
clean :
	rm -rf $(BUILDDIR)/*
