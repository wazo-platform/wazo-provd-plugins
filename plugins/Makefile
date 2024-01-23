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
REMOTE_TESTING_PATH := /var/www/provd/plugins/2/testing
REMOTE_STABLE_PATH := /var/www/provd/plugins/2/stable
REMOTE_ARCHIVE_PATH := /var/www/provd/plugins/2/archive
REMOTE_FIRMWARES_PATH := /var/www/provd/firmwares


.PHONY : download
download :
	mkdir -p $(TESTING_PATH)
	rsync -v --recursive --times --delete $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_TESTING_PATH)/ $(TESTING_PATH)

.PHONY : build
build :
	rm -rf $(PLUGINS_PATH) $(TESTING_PATH)
	mkdir -p $(PLUGINS_PATH) $(TESTING_PATH)
	$(PGBUILD) --build --source . --destination $(PLUGINS_PATH)
	$(PGBUILD) --package --source $(PLUGINS_PATH) --destination $(TESTING_PATH)
	$(PGBUILD) --db --source $(TESTING_PATH) --destination $(TESTING_PATH)
	chmod +r $(TESTING_PATH)/*


.PHONY : build-tests
build-tests :
	rm -rf $(PLUGINS_PATH) $(TESTING_PATH)
	mkdir -p $(PLUGINS_PATH) $(TESTING_PATH)
	$(PGBUILD) --build --source . --destination $(PLUGINS_PATH) wazo_test_plugins
	$(PGBUILD) --package --source $(PLUGINS_PATH) --destination $(TESTING_PATH)
	$(PGBUILD) --db --source $(TESTING_PATH) --destination $(TESTING_PATH)
	chmod +r $(TESTING_PATH)/*


.PHONY : upload
upload : build
	rsync -v --recursive --times --delete $(TESTING_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_TESTING_PATH)


.PHONY : download-stable
download-stable :
	mkdir -p $(STABLE_PATH)
	rsync -v --recursive --times --delete $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_STABLE_PATH)/ $(STABLE_PATH)


.PHONY : build-stable
build-stable :
	$(PGBUILD) --db --source $(STABLE_PATH) --destination $(STABLE_PATH)
	chmod +r $(STABLE_PATH)/*


.PHONY : upload-stable
upload-stable : build-stable
	rsync -v --recursive --times --delete $(STABLE_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_STABLE_PATH)


.PHONY : download-archive
download-archive :
	mkdir -p $(ARCHIVE_PATH)
	rsync -v --recursive --times --delete $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_ARCHIVE_PATH)/ $(ARCHIVE_PATH)


.PHONY : build-archive
build-archive :
	$(PGBUILD) --db --source $(ARCHIVE_PATH) --destination $(ARCHIVE_PATH)
	chmod +r $(ARCHIVE_PATH)/*


.PHONY : upload-archive
upload-archive : build-archive
	rsync -v --recursive --times --delete $(ARCHIVE_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_ARCHIVE_PATH)


.PHONY : download-firmwares
download-firmwares :
	mkdir -p $(FIRMWARES_PATH)
	rsync -v --recursive --times $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_FIRMWARES_PATH)/ $(FIRMWARES_PATH)


.PHONY : upload-firmwares
upload-firmwares:
	chmod +r $(FIRMWARES_PATH)/*
	rsync -v --recursive --times $(FIRMWARES_PATH)/ $(REMOTE_USER)@$(REMOTE_HOST):$(REMOTE_FIRMWARES_PATH)


.PHONY : clean
clean :
	rm -rf $(BUILDDIR)/*
