%define without_dbus 1
%define without_braille 1


Summary: OpenPrinting CUPS filters and backends
Name:    cups-filters
Version: 1.25.6
Release: 1%{?dist}

# For a breakdown of the licensing, see COPYING file
# GPLv2:   filters: commandto*, imagetoraster, pdftops, rasterto*,
#                   imagetopdf, pstopdf, texttopdf
#         backends: parallel, serial
# GPLv2+:  filters: gstopxl, textonly, texttops, imagetops, foomatic-rip
# GPLv3:   filters: bannertopdf
# GPLv3+:  filters: urftopdf, rastertopdf
# LGPLv2+:   utils: cups-browsed
# MIT:     filters: gstoraster, pdftoijs, pdftoopvp, pdftopdf, pdftoraster
License: GPLv2 and GPLv2+ and GPLv3 and GPLv3+ and LGPLv2+ and MIT and BSD with advertising

Url:     http://www.linuxfoundation.org/collaborate/workgroups/openprinting/cups-filters
Vendor:  bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2

Requires: cups-filters-libs = %{version}-%{release}

# gcc and gcc-c++ is not in buildroot by default

# gcc for backends (implicitclass, parallel, serial, backend error handling)
# cupsfilters (colord, color manager...), filter (banners, 
# commandto*, braille, foomatic-rip, imagetoraster, imagetopdf, gstoraster e.g.),
# fontembed, cups-browsed
BuildRequires: gcc
# gcc-c++ for pdftoopvp, pdftopdf
#BuildRequires: gcc-c++

BuildRequires: cups-devel
BuildRequires: pkgconfig
# pdftopdf
BuildRequires: qpdf-devel
# pdftops
BuildRequires: poppler-utils
# pdftoijs, pdftoopvp, pdftoraster, gstoraster
BuildRequires: pkgconfig(poppler)
BuildRequires: poppler-cpp-devel
BuildRequires: libjpeg-turbo-devel
BuildRequires: libtiff-devel
BuildRequires: pkgconfig(libpng)
BuildRequires: pkgconfig(zlib)
%if 0%{!?without_dbus:1}
BuildRequires: pkgconfig(dbus-1)
%endif
BuildRequires: ghostscript
# libijs
BuildRequires: ghostscript-devel
BuildRequires: pkgconfig(freetype2)
BuildRequires: pkgconfig(fontconfig)
BuildRequires: pkgconfig(lcms2)
# cups-browsed
%if 0%{!?without_dbus:1}
BuildRequires: avahi-devel
BuildRequires: pkgconfig(avahi-glib)
%endif
BuildRequires:  glib2-devel
%if 0%{!?without_dbus:1}
BuildRequires: systemd
%endif

# Make sure we get postscriptdriver tags.
#BuildRequires: python-cups

# Testing font for test scripts.
#BuildRequires: dejavu-sans-fonts

# autogen.sh
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool

Requires: cups-filesystem
# if --with-pdftops is set to hybrid, we use poppler filters for several printers
# and for printing banners, for other printers we need gs - ghostscript
Requires: poppler-utils
# several filters calls 'gs' binary during filtering
Requires: ghostscript

# for getting ICC profiles for filters (dbus must run)
#Requires: colord

# texttopdf
# not needed, as we have courier installed anyway
#Requires: liberation-mono-fonts

# pstopdf
Requires: bc grep sed which

# cups-browsed
Requires: cups
%if 0%{!?without_dbus:1}
Requires(post): systemd
Requires(preun): systemd
Requires(postun): systemd
%endif

# some installations can have ghostscript-cups or foomatic-filters installed,
# but they are provided by cups-filters, so we need to obsolete them to have
# them uninstalled - remove these obsoletes when F31+
Obsoletes: ghostscript-cups
Obsoletes: foomatic-filters

%package libs
Summary: OpenPrinting CUPS filters and backends - cupsfilters and fontembed libraries
# LGPLv2: libcupsfilters
# MIT:    libfontembed
License: LGPLv2 and MIT

%package devel
Summary: OpenPrinting CUPS filters and backends - development environment
License: LGPLv2 and MIT
Requires: cups-filters-libs = %{version}-%{release}

%description
Contains backends, filters, and other software that was
once part of the core CUPS distribution but is no longer maintained by
Apple Inc. In addition it contains additional filters developed
independently of Apple, especially filters for the PDF-centric printing
workflow introduced by OpenPrinting.

%description libs
This package provides cupsfilters and fontembed libraries.

%description devel
This is the development package for OpenPrinting CUPS filters and backends.

%debug_package

%prep
%scm_setup

%build
# work-around Rpath
./autogen.sh

# --with-pdftops=hybrid - use Poppler's pdftops instead of Ghostscript
#                         Brother, Minolta, and Konica Minolta to work around
#                         bugs in the printer's PS interpreters
# --with-rcdir=no - don't install SysV init script
# --enable-auto-setup-driverless - enable automatic setup of IPP network printers
#                                  with driverless support
# --enable-driverless - enable PPD generator for driverless printing in 
#                       /usr/lib/cups/driver, it is for manual setup of 
#                       driverless printers with printer setup tool
# --disable-static - do not build static libraries (becuase of Fedora Packaging
#                    Guidelines)
# --enable-dbus - enable DBus Connection Manager's code
# --disable-silent-rules - verbose build output
# --disable-mutool - mupdf is retired in Fedora, use qpdf
# --enable-pclm - support for pclm language
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%configure --disable-static \
           --disable-silent-rules \
           --with-pdftops=pdftops \
%if 0%{!?without_dbus:1}
           --enable-dbus \
%else
           --enable-dbus=no \
%endif
           --with-rcdir=no \
%if 0%{!?without_braille:1}
           --enable-braille \
%else
           --enable-braille=no \
%endif
           --disable-avahi \
           --disable-mutool \
           --enable-driverless \
           --enable-auto-setup-driverless \
           --enable-pclm \
           --with-test-font-path=/@system_drive/psfonts/DejaVuSans.ttf \
           --with-shell=%{_bindir}/sh \
           --docdir=%{_pkgdocdir}

make %{?_smp_mflags}

%install
make install DESTDIR=%{buildroot}

# Don't ship libtool la files.
rm -f %{buildroot}%{_libdir}/lib*.la

# Not sure what is this good for.
rm -f %{buildroot}%{_bindir}/ttfread.exe

rm -f %{buildroot}%{_pkgdocdir}/INSTALL
mkdir -p %{buildroot}%{_pkgdocdir}/fontembed/
cp -p fontembed/README %{buildroot}%{_pkgdocdir}/fontembed/

# systemd unit file
#mkdir -p %{buildroot}%{_unitdir}
#install -p -m 644 utils/cups-browsed.service %{buildroot}%{_unitdir}

# LSB3.2 requires /usr/bin/foomatic-rip,
# create it temporarily as a relative symlink
#ln -sf ../lib/cups/filter/foomatic-rip.exe %{buildroot}%{_bindir}/foomatic-rip

# Don't ship urftopdf for now (bug #1002947).
rm -f %{buildroot}%{_cups_serverbin}/filter/urftopdf.exe
sed -i '/urftopdf/d' %{buildroot}%{_datadir}/cups/mime/cupsfilters.convs

# Don't ship pdftoopvp for now (bug #1027557).
rm -f %{buildroot}%{_cups_serverbin}/filter/pdftoopvp.exe
rm -f %{buildroot}%{_sysconfdir}/fonts/conf.d/99pdftoopvp.conf


%check
# this export is needed, as else the dll for the tests are not found
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/.libs
make check


%post
#systemd_post cups-browsed.service

%preun
#systemd_preun cups-browsed.service

%postun
#systemd_postun_with_restart cups-browsed.service 

#ldconfig_scriptlets libs


%files
%{_pkgdocdir}/README
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/NEWS
%{_pkgdocdir}/ABOUT-NLS
%config(noreplace) %{_sysconfdir}/cups/cups-browsed.conf
%attr(0755,root,root) %{_cups_serverbin}/filter/*.exe
%attr(0755,root,root) %{_cups_serverbin}/filter/gstopdf
%attr(0755,root,root) %{_cups_serverbin}/filter/gstopxl
%attr(0755,root,root) %{_cups_serverbin}/filter/imagetops
%attr(0755,root,root) %{_cups_serverbin}/filter/texttops
%attr(0755,root,root) %{_cups_serverbin}/filter/rastertopclm
%attr(0755,root,root) %{_cups_serverbin}/backend/parallel.exe
# Serial backend needs to run as root (bug #212577#c4).
#attr(0700,root,root) %{_cups_serverbin}/backend/serial
%attr(0755,root,root) %{_cups_serverbin}/backend/implicitclass.exe
%attr(0755,root,root) %{_cups_serverbin}/backend/beh.exe
# cups-brf needs to be run as root, otherwise it leaves error messages
# in journal
%if 0%{!?without_braille:1}
%attr(0700,root,root) %{_cups_serverbin}/backend/cups-brf.exe
%endif
%{_bindir}/foomatic-rip
%{_bindir}/driverless
%{_cups_serverbin}/backend/driverless
%{_cups_serverbin}/driver/driverless.exe
%{_datadir}/cups/banners
%if 0%{!?without_braille:1}
%{_datadir}/cups/braille
%endif
%{_datadir}/cups/charsets
%{_datadir}/cups/data/*
# this needs to be in the main package because of cupsfilters.drv
%{_datadir}/cups/ppdc/pcl.h
%if 0%{!?without_braille:1}
%{_datadir}/cups/ppdc/braille.defs
%{_datadir}/cups/ppdc/fr-braille.po
%{_datadir}/cups/ppdc/imagemagick.defs
%{_datadir}/cups/ppdc/index.defs
%{_datadir}/cups/ppdc/liblouis.defs
%{_datadir}/cups/ppdc/liblouis1.defs
%{_datadir}/cups/ppdc/liblouis2.defs
%{_datadir}/cups/ppdc/liblouis3.defs
%{_datadir}/cups/ppdc/liblouis4.defs
%{_datadir}/cups/ppdc/media-braille.defs
%endif
%{_datadir}/cups/drv/cupsfilters.drv
%if 0%{!?without_braille:1}
%{_datadir}/cups/drv/generic-brf.drv
%{_datadir}/cups/drv/generic-ubrl.drv
%{_datadir}/cups/drv/indexv3.drv
%{_datadir}/cups/drv/indexv4.drv
%endif
%{_datadir}/cups/mime/cupsfilters.types
%{_datadir}/cups/mime/cupsfilters.convs
%{_datadir}/cups/mime/cupsfilters-ghostscript.convs
%{_datadir}/cups/mime/cupsfilters-poppler.convs
%if 0%{!?without_braille:1}
%{_datadir}/cups/mime/braille.convs
%{_datadir}/cups/mime/braille.types
%endif
%{_datadir}/ppd/cupsfilters
%if 0%{!?without_dbus:1}
%{_sbindir}/cups-browsed.exe
%{_unitdir}/cups-browsed.service
%endif
%{_mandir}/man8/cups-browsed.8.gz
%{_mandir}/man5/cups-browsed.conf.5.gz
%{_mandir}/man1/foomatic-rip.1.gz
%{_mandir}/man1/driverless.1.gz

%files libs
%dir %{_pkgdocdir}/
%{_pkgdocdir}/COPYING
%{_pkgdocdir}/fontembed/README
%{_libdir}/cupsfil*.dll
%{_libdir}/fontemb*.dll

%files devel
%{_includedir}/cupsfilters
%{_includedir}/fontembed
%{_datadir}/cups/ppdc/escp.h
%{_libdir}/pkgconfig/libcupsfilters.pc
%{_libdir}/pkgconfig/libfontembed.pc
%{_libdir}/cupsfilters*_dll.a
%{_libdir}/fontembed*_dll.a

%changelog
* Fri Oct 11 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.25.6-1
- update to version 1.25.6

* Fri Dec 15 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.17.2-3
- fix ghostscript execution (gs can't work with \, so provide / only)

* Mon Nov 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.17.2-2
- fix a path issue with pdftops from poppler

* Tue Oct 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.17.2-1
- moved source to github
- update to vendor version 1.17.2

* Tue Aug 22 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.13.3-2
- fix symlink

* Tue Feb 14 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.13.3-1
- use printf instead of echo -e
- add bldlevel to the dll
- fix using of bash as shell
- adjust spec to scm_ macros usage
- update to vendor version 1.13.3

* Wed Aug 24 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.8.2-5
- lower the gs req to 9.14
- rebuild with new poppler

* Tue Apr 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.8.2-4
- more binary read fixes
- backout setmode

* Fri Apr 1 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.8.2-3
- remove LDFLAG -Zbin-files

* Thu Mar 17 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.8.2-2
- remove libaration font req

* Mon Mar 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.8.2-1
- first version
