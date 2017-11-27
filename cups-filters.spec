Summary: OpenPrinting CUPS filters and backends
Name:    cups-filters
Version: 1.17.2
Release: 2%{?dist}

# For a breakdown of the licensing, see COPYING file
# GPLv2:   filters: commandto*, imagetoraster, pdftops, rasterto*,
#                   imagetopdf, pstopdf, texttopdf
#         backends: parallel, serial
# GPLv2+:  filters: gstopxl, textonly, texttops, imagetops, foomatic-rip
# GPLv3:   filters: bannertopdf
# GPLv3+:  filters: urftopdf, rastertopdf
# LGPLv2+:   utils: cups-browsed
# MIT:     filters: gstoraster, pdftoijs, pdftoopvp, pdftopdf, pdftoraster
License: GPLv2 and GPLv2+ and GPLv3 and GPLv3+ and LGPLv2+ and MIT

Url:     http://www.linuxfoundation.org/collaborate/workgroups/openprinting/cups-filters
Vendor:  bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/%{name}-os2 master

Requires: cups-filters-libs = %{version}-%{release}

# Obsolete cups-php (bug #971741)
Obsoletes: cups-php < 1:1.6.0-1
# Don't Provide it because we don't build the php module
#Provides: cups-php = 1:1.6.0-1

BuildRequires: cups-devel
BuildRequires: pkgconfig
# pdftopdf
BuildRequires: qpdf-devel
# pdftops
BuildRequires: poppler-utils >= 0.38.0-2
# pdftoijs, pdftoopvp, pdftoraster, gstoraster
BuildRequires: poppler-devel
BuildRequires: poppler-cpp-devel
BuildRequires: libjpeg-devel
BuildRequires: libtiff-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
#BuildRequires: pkgconfig(dbus-1)
# libijs
BuildRequires: ghostscript-devel
BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: lcms2-devel
# cups-browsed
#BuildRequires: avahi-devel
#BuildRequires: pkgconfig(avahi-glib)
BuildRequires:  glib2-devel
#BuildRequires: systemd

# Make sure we get postscriptdriver tags.
#BuildRequires: python-cups

# Testing font for test scripts.
#BuildRequires: dejavu-sans-fonts

# autogen.sh
BuildRequires: autoconf
BuildRequires: automake
BuildRequires: libtool
#BuildRequires: mupdf

Requires: cups-filesystem
Requires: poppler-utils >= 0.38.0-2
Requires: ghostscript >= 9.14

# texttopdf
# not needed, as we have courier installed anyway
#Requires: liberation-mono-fonts

# pstopdf
Requires: bc grep sed

# cups-browsed
#Requires(post): systemd
#Requires(preun): systemd
#Requires(postun): systemd

# Ghostscript CUPS filters live here since Ghostscript 9.08.
Provides: ghostscript-cups = 9.08
Obsoletes: ghostscript-cups < 9.08

# foomatic-rip's upstream moved from foomatic-filters to cups-filters-1.0.42
Provides: foomatic-filters = 4.0.9-8
Obsoletes: foomatic-filters < 4.0.9-8

%package libs
Summary: OpenPrinting CUPS filters and backends - cupsfilters and fontembed libraries
Group:   System Environment/Libraries
# LGPLv2: libcupsfilters
# MIT:    libfontembed
License: LGPLv2 and MIT

%package devel
Summary: OpenPrinting CUPS filters and backends - development environment
Group:   Development/Libraries
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
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%configure --disable-static \
           --disable-silent-rules \
           --with-pdftops=pdftops \
           --with-rcdir=no \
           --enable-dbus=no \
           --enable-braille=no \
           --disable-avahi \
           --disable-mutool \
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

# imagetobrf is going to be mapped as /usr/lib/cups/filter/imagetoubrl
#ln -sf imagetobrf %{buildroot}%{_cups_serverbin}/filter/imagetoubrl

# textbrftoindex3 is going to be mapped as /usr/lib/cups/filter/textbrftoindexv4
#ln -sf textbrftoindexv3 %{buildroot}%{_cups_serverbin}/filter/textbrftoindexv4

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

# Initial installation
if [ $1 -eq 1 ] ; then
    IN=%{_sysconfdir}/cups/cupsd.conf
    OUT=%{_sysconfdir}/cups/cups-browsed.conf
    keyword=BrowsePoll

    # We can remove this after few releases, it's just for the introduction of cups-browsed.
    if [ -f "$OUT" ]; then
        printf "\n# NOTE: This file is not part of CUPS.\n# You need to enable cups-browsed service\n# and allow ipp-client service in firewall." >> "$OUT"
    fi

    # move BrowsePoll from cupsd.conf to cups-browsed.conf
    if [ -f "$IN" ] && grep -iq ^$keyword "$IN"; then
        if ! grep -iq ^$keyword "$OUT"; then
            (cat >> "$OUT" <<EOF

# Settings automatically moved from cupsd.conf by RPM package:
EOF
            ) || :
            (grep -i ^$keyword "$IN" >> "$OUT") || :
            #systemctl enable cups-browsed.service >/dev/null 2>&1 || :
        fi
        sed -i -e "s,^$keyword,#$keyword directive moved to cups-browsed.conf\n#$keyword,i" "$IN" || :
    fi
fi

%preun
#systemd_preun cups-browsed.service

%postun
#systemd_postun_with_restart cups-browsed.service 

#post libs -p /sbin/ldconfig

#postun libs -p /sbin/ldconfig


%files
%{_pkgdocdir}/README
%{_pkgdocdir}/AUTHORS
%{_pkgdocdir}/NEWS
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
%{_bindir}/foomatic-rip
%{_bindir}/driverless
%{_cups_serverbin}/backend/driverless
%{_cups_serverbin}/driver/driverless.exe
%{_datadir}/cups/banners
#%{_datadir}/cups/braille
%{_datadir}/cups/charsets
%{_datadir}/cups/data/*
# this needs to be in the main package because of cupsfilters.drv
%{_datadir}/cups/ppdc/pcl.h
#%{_datadir}/cups/ppdc/braille.defs
#%{_datadir}/cups/ppdc/fr-braille.po
#%{_datadir}/cups/ppdc/imagemagick.defs
#%{_datadir}/cups/ppdc/index.defs
#%{_datadir}/cups/ppdc/liblouis.defs
#%{_datadir}/cups/ppdc/liblouis1.defs
#%{_datadir}/cups/ppdc/liblouis2.defs
#%{_datadir}/cups/ppdc/liblouis3.defs
#%{_datadir}/cups/ppdc/liblouis4.defs
#%{_datadir}/cups/ppdc/media-braille.defs
%{_datadir}/cups/drv/cupsfilters.drv
#%{_datadir}/cups/drv/generic-brf.drv
#%{_datadir}/cups/drv/indexv3.drv
#%{_datadir}/cups/drv/indexv4.drv
%{_datadir}/cups/mime/cupsfilters.types
%{_datadir}/cups/mime/cupsfilters.convs
%{_datadir}/cups/mime/cupsfilters-ghostscript.convs
#%{_datadir}/cups/mime/cupsfilters-mupdf.convs
%{_datadir}/cups/mime/cupsfilters-poppler.convs
#%{_datadir}/cups/mime/braille.convs
#%{_datadir}/cups/mime/braille.types
%{_datadir}/ppd/cupsfilters
#{_sbindir}/cups-browsed.exe
#{_unitdir}/cups-browsed.service
%{_mandir}/man8/cups-browsed.8*
%{_mandir}/man5/cups-browsed.conf.5*
%{_mandir}/man1/foomatic-rip.1*
%{_mandir}/man1/driverless.1*

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
