BINDIR = /@unixroot/usr/bin
DESTDIR = /@unixroot/usr/share/sgml/docbook/dsssl-stylesheets-1.74b
MANDIR= /@unixroot/usr/share/man

all: install

install: install-bin install-dtd install-dsl install-img install-misc install-man

install-bin:
	mkdir -p $(BINDIR)
	install -p bin/collateindex.pl $(BINDIR)

install-man:
	mkdir -p $(MANDIR)/man1
	install -m 644 -p bin/collateindex.pl.1 $(MANDIR)/man1

install-dtd:
	mkdir -p $(DESTDIR)/dtds/decls
	mkdir -p $(DESTDIR)/dtds/dbdsssl
	mkdir -p $(DESTDIR)/dtds/html
	mkdir -p $(DESTDIR)/dtds/imagelib
	mkdir -p $(DESTDIR)/dtds/olink
	cp -p dtds/decls/docbook.dcl $(DESTDIR)/dtds/decls
	cp -p dtds/decls/xml.dcl $(DESTDIR)/dtds/decls
	cp -p dtds/dbdsssl/dbdsssl.dtd $(DESTDIR)/dtds/dbdsssl
	cp -p dtds/html/dbhtml.dtd $(DESTDIR)/dtds/html
	cp -p dtds/html/ISOlat1.gml $(DESTDIR)/dtds/html
	cp -p dtds/imagelib/imagelib.dtd $(DESTDIR)/dtds/imagelib
	cp -p dtds/olink/olinksum.dtd $(DESTDIR)/dtds/olink

install-dsl:
	mkdir -p $(DESTDIR)/lib
	mkdir -p $(DESTDIR)/common
	mkdir -p $(DESTDIR)/html
	mkdir -p $(DESTDIR)/print
	mkdir -p $(DESTDIR)/olink
	cp -p lib/dblib.dsl $(DESTDIR)/lib
	cp -p common/*.dsl $(DESTDIR)/common
	cp -p common/*.ent $(DESTDIR)/common
	cp -p html/*.dsl $(DESTDIR)/html
	cp -p lib/dblib.dsl $(DESTDIR)/lib
	cp -p print/*.dsl $(DESTDIR)/print
	cp -p olink/*.dsl $(DESTDIR)/olink

install-img:
	mkdir -p $(DESTDIR)/images/callouts
	cp -p images/*.gif $(DESTDIR)/images
	cp -p images/callouts/*.gif $(DESTDIR)/images/callouts

#install-test:
#	mkdir -p $(DESTDIR)/test/{cases,imagelib,xml}
#	cp test/*.* $(DESTDIR)/test
#	cp test/cases/*.* $(DESTDIR)/test/cases
#	cp test/imagelib/*.* $(DESTDIR)/test/imagelib
#	cp test/xml/*.* $(DESTDIR)/test/xml

install-misc:
	cp -p catalog $(DESTDIR)
	cp -p VERSION $(DESTDIR)
