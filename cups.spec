#define svn_url     F:/rd/ports/cups/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/cups/trunk
%define svn_rev     944

%define _without_dbus 1
%define _without_php 1

#
# "$Id: cups.spec.in 9359 2010-11-11 19:09:24Z mike $"
#
#   RPM "spec" file for CUPS.
#
#   Original version by Jason McMullan <jmcc@ontv.com>.
#
#   Copyright 2007-2010 by Apple Inc.
#   Copyright 1999-2007 by Easy Software Products, all rights reserved.
#
#   These coded instructions, statements, and computer programs are the
#   property of Apple Inc. and are protected by Federal copyright
#   law.  Distribution and use rights are outlined in the file "LICENSE.txt"
#   which should have been included with this file.  If this file is
#   file is missing or damaged, see the license at "http://www.cups.org/".
#

# Conditional build options (--with name/--without name):
#
#   dbus     - Enable/disable DBUS support (default = enable)
#   php      - Enable/disable PHP support (default = enable)

%{!?_with_dbus: %{!?_without_dbus: %define _with_dbus --with-dbus}}
%{?_with_dbus: %define _dbus --enable-dbus}
%{!?_with_dbus: %define _dbus --disable-dbus}

%{!?_with_php: %{!?_without_php: %define _with_php --with-php}}
%{?_with_php: %define _php --with-php}
%{!?_with_php: %define _php --without-php}

%{!?_with_static: %{!?_without_static: %define _without_static --without-static}}
%{?_with_static: %define _static --enable-static}
%{!?_with_static: %define _static --disable-static}

Summary: CUPS
Name: cups
Version: 1.4.8
Release: 0%{?dist}
Epoch: 1

License: GPL
Group: System Environment/Daemons

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Url: http://www.cups.org
Packager: Anonymous <anonymous@foo.com>
Vendor: Apple Inc.

# Use buildroot so as not to disturb the version already installed
BuildRoot: /tmp/%{name}-root

# Dependencies...
Requires: %{name}-libs = %{epoch}:%{version}
Obsoletes: lpd, lpr, LPRng
Provides: lpd, lpr, LPRng
Obsoletes: cups-da, cups-de, cups-es, cups-et, cups-fi, cups-fr, cups-he
Obsoletes: cups-id, cups-it, cups-ja, cups-ko, cups-nl, cups-no, cups-pl
Obsoletes: cups-pt, cups-ru, cups-sv, cups-zh

%package devel
Summary: CUPS - development environment
Group: Development/Libraries
Requires: %{name}-libs = %{epoch}:%{version}

%package libs
Summary: CUPS - shared libraries
Group: System Environment/Libraries
Provides: libcups1

%package lpd
Summary: CUPS - LPD support
Group: System Environment/Daemons
Requires: %{name} = %{epoch}:%{version} xinetd

%if %{?_with_php:1}%{!?_with_php:0}
%package php
Summary: CUPS - PHP support
Group: Development/Languages
Requires: %{name}-libs = %{epoch}:%{version}
%endif

%description
CUPS is the standards-based, open source printing system developed by
Apple Inc. for Mac OS� X and other UNIX�-like operating systems.

%description devel
This package provides the CUPS headers and development environment.

%description libs
This package provides the CUPS shared libraries.

%description lpd
This package provides LPD client support.

%if %{?_with_php:1}%{!?_with_php:0}
%description php
This package provides PHP support for CUPS.
%endif

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
export CONFIG_SITE="/@unixroot/usr/share/config.legacy";
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe";
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp";
export LIBS="-lurpo";
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$LDFLAGS $RPM_OPT_FLAGS" \
    %configure %{_dbus} %{_php} %{_static}
# If we got this far, all prerequisite libraries must be here.
make

%install
# Make sure the RPM_BUILD_ROOT directory exists.
rm -rf $RPM_BUILD_ROOT

make BUILDROOT=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%docdir %{_datadir}/doc/cups
%defattr(-,root,root)
%dir %{_sysconfdir}/cups
%config(noreplace) %{_sysconfdir}/cups/*.conf
%{_sysconfdir}/cups/cupsd.conf.default
%dir %{_sysconfdir}/cups/interfaces
%dir %{_sysconfdir}/cups/ppd
%attr(0700,root,root) %dir %{_sysconfdir}/cups/ssl

%if %{?_with_dbus:1}%{!?_with_dbus:0}
# DBUS
%{_sysconfdir}/dbus-1/system.d/*
%endif

%{_bindir}/cancel.exe
%{_bindir}/cupstestdsc.exe
%{_bindir}/cupstestppd.exe
%{_bindir}/lp*.exe
%dir %{_libdir}/cups
%dir %{_libdir}/cups/backend
%{_libdir}/cups/backend/http
%attr(0700,root,root) %{_libdir}/cups/backend/ipp.exe
%attr(0700,root,root) %{_libdir}/cups/backend/lpd.exe
%{_libdir}/cups/backend/parallel.exe
%{_libdir}/cups/backend/scsi.exe
#%{_libdir}/cups/backend/serial.exe
%{_libdir}/cups/backend/snmp.exe
%{_libdir}/cups/backend/socket.exe
%{_libdir}/cups/backend/usb.exe
%dir %{_libdir}/cups/cgi-bin
%{_libdir}/cups/cgi-bin/*
%dir %{_libdir}/cups/daemon
%{_libdir}/cups/daemon/cups-deviced.exe
%{_libdir}/cups/daemon/cups-driverd.exe
%{_libdir}/cups/daemon/cups-polld.exe
%dir %{_libdir}/cups/driver
%dir %{_libdir}/cups/filter
%{_libdir}/cups/filter/*
%dir %{_libdir}/cups/monitor
%{_libdir}/cups/monitor/*
%dir %{_libdir}/cups/notifier
%{_libdir}/cups/notifier/*

%{_sbindir}/*
%dir %{_datadir}/cups
%dir %{_datadir}/cups/banners
%{_datadir}/cups/banners/*
%dir %{_datadir}/cups/charmaps
%{_datadir}/cups/charmaps/*
%dir %{_datadir}/cups/charsets
%{_datadir}/cups/charsets/*
%dir %{_datadir}/cups/data
%{_datadir}/cups/data/*
%dir %{_datadir}/cups/drv
%{_datadir}/cups/drv/*
%dir %{_datadir}/cups/fonts
%{_datadir}/cups/fonts/*
%dir %{_datadir}/cups/mime
%{_datadir}/cups/mime/*
%dir %{_datadir}/cups/model
%dir %{_datadir}/cups/ppdc
%{_datadir}/cups/ppdc/*
%dir %{_datadir}/cups/templates
%{_datadir}/cups/templates/*
%dir %{_datadir}/doc/cups
%{_datadir}/doc/cups/*.*
%dir %{_datadir}/doc/cups/help
%{_datadir}/doc/cups/help/accounting.html
%{_datadir}/doc/cups/help/cgi.html
%{_datadir}/doc/cups/help/glossary.html
%{_datadir}/doc/cups/help/kerberos.html
%{_datadir}/doc/cups/help/license.html
#%{_datadir}/doc/cups/help/man-*.html
%{_datadir}/doc/cups/help/network.html
%{_datadir}/doc/cups/help/options.html
%{_datadir}/doc/cups/help/overview.html
%{_datadir}/doc/cups/help/policies.html
%{_datadir}/doc/cups/help/ref-*.html
%{_datadir}/doc/cups/help/security.html
%{_datadir}/doc/cups/help/sharing.html
%{_datadir}/doc/cups/help/standard.html
%{_datadir}/doc/cups/help/translation.html
%{_datadir}/doc/cups/help/whatsnew.html
%dir %{_datadir}/doc/cups/images
%{_datadir}/doc/cups/images/*
#%{_datadir}/locale/*

#%dir %{_datadir}/man

%dir /%{_var}/cache/cups
%attr(0775,root,sys) %dir /%{_var}/cache/cups/rss
%dir /%{_var}/log/cups
%dir /%{_var}/run/cups
#%attr(0711,lp,sys) %dir /%{_var}/run/cups/certs
%attr(0710,lp,sys) %dir /%{_var}/spool/cups
%attr(1770,lp,sys) %dir /%{_var}/spool/cups/tmp

%files devel
%defattr(-,root,root)
%dir %{_datadir}/cups/examples
%{_datadir}/cups/examples/*
#%dir %{_datadir}/man

%{_bindir}/cups-config
%{_bindir}/ppd*.exe
%dir %{_includedir}/cups
%{_includedir}/cups/*
%{_libdir}/*.a

%dir %{_datadir}/doc/cups/help
%{_datadir}/doc/cups/help/api*.html
%{_datadir}/doc/cups/help/postscript-driver.html
%{_datadir}/doc/cups/help/ppd-compiler.html
%{_datadir}/doc/cups/help/raster-driver.html
%{_datadir}/doc/cups/help/spec*.html

%files libs
%defattr(-,root,root)
%{_libdir}/*.dll

%files lpd
%defattr(-,root,root)
#%{_sysconfdir}/xinetd.d/cups-lpd
%dir %{_libdir}/cups
%dir %{_libdir}/cups/daemon
%{_libdir}/cups/daemon/cups-lpd.exe
#%dir %{_datadir}/man/man8
#%{_datadir}/man/man8/cups-lpd.8.gz

%if %{?_with_php:1}%{!?_with_php:0}
%files php
# PHP
/usr/lib*/php*
%endif

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_sbindir}/*.dbg
%{_libdir}/*.dbg
%{_libdir}/cups/backend/*.dbg
%{_libdir}/cups/daemon/*.dbg

%changelog
* Tue Dec 18 2014 yd
- r944, initial unixroot build.