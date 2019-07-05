# this spec file is a combination from the fedora cups.spec and the
# cups.spec as included in cups

%define _strip_opts --compress -i "*.cgi" --debuginfo -i "*.cgi"

%global _without_dbus 1
%global _without_dnssd 1
%global _without_systemd 1

#
# "$Id: cups.spec.in 9359 2010-11-11 19:09:24Z mike $"
#
#   RPM "spec" file for CUPS.
#
#   Original version by Jason McMullan <jmcc@ontv.com>.
#
#   Copyright 2007-2015 by Apple Inc.
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
#   dnssd    - Enable/disable DNS-SD support (default = enable)
#   libusb1  - Enable/disable LIBUSB 1.0 support (default = enable)
#   static   - Enable/disable static libraries (default = enable)
#   systemd  - Enable/disable systemd support (default = enable)

%{!?_with_dbus: %{!?_without_dbus: %global _with_dbus --with-dbus}}
%{?_with_dbus: %global _dbus --enable-dbus}
%{!?_with_dbus: %global _dbus --disable-dbus}

%{!?_with_dnssd: %{!?_without_dnssd: %global _with_dnssd --with-dnssd}}
%{?_with_dnssd: %global _dnssd --enable-dnssd}
%{!?_with_dnssd: %global _dnssd --disable-dnssd}

%{!?_with_libusb1: %{!?_without_libusb1: %global _with_libusb1 --with-libusb1}}
%{?_with_libusb1: %global _libusb1 --enable-libusb}
%{!?_with_libusb1: %global _libusb1 --disable-libusb}

%{!?_with_static: %{!?_without_static: %global _without_static --without-static}}
%{?_with_static: %global _static --enable-static}
%{!?_with_static: %global _static --disable-static}

%{!?_with_systemd: %{!?_without_systemd: %global _with_systemd --with-systemd}}
%{?_with_systemd: %global _systemd --enable-systemd}
%{!?_with_systemd: %global _systemd --disable-systemd}


Summary: CUPS
Name: cups
Version: 2.1.3
Release: 10%{?dist}
Epoch: 1

License: GPL
Group: System Environment/Daemons

Url: http://www.cups.org
Vendor: bww bitwise works GmbH
%scm_source  github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2-1

# Dependencies...
Requires: %{name}-filesystem = %{epoch}:%{version}-%{release}
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Requires: %{name}-client = %{epoch}:%{version}-%{release}

Provides: cupsddk, cupsddk-drivers

# Make sure we have some filters for converting to raster format
Requires: cups-filters

%if %{?_with_dbus:1}%{!?_with_dbus:0}
BuildRequires: dbus-devel
%endif

%if %{?_with_dnssd:1}%{!?_with_dnssd:0}
BuildRequires: avahi-devel
%endif

%if %{?_with_libusb1:1}%{!?_with_libusb1:0}
BuildRequires: libusb1-devel >= 1.0
%endif

%if %{?_with_systemd:1}%{!?_with_systemd:0}
BuildRequires: systemd-devel
%endif

BuildRequires: libpng-devel, libjpeg-devel, libtiff-devel
BuildRequires: openssl-devel, zlib-devel
BuildRequires: libpoll-devel

# Use buildroot so as not to disturb the version already installed
BuildRoot: %{_tmppath}/%{name}-root

%package devel
Summary: CUPS printing system - development environment
Group: Development/Libraries
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Provides: cupsddk-devel

%package libs
Summary: CUPS printing system - shared libraries
Group: System Environment/Libraries

%package filesystem
Summary: CUPS printing system - directory layout
BuildArch: noarch

%package lpd
Summary: CUPS printing system - lpd emulation
Group: System Environment/Daemons
Requires: %{name} = %{epoch}:%{version}-%{release}
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Provides: lpd

%package ipptool
Summary: CUPS printing system - tool for performing IPP requests
Requires: %{name} = %{epoch}:%{version}-%{release}

%package client
Summary: CUPS printing system - client programs
Requires: %{name}-libs = %{epoch}:%{version}-%{release}
Provides: lpr

%description
CUPS printing system provides a portable printing layer for
UNIX© operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.
CUPS was ported to OS/2 to have the same benefit as UNIX has.

%description client
CUPS printing system provides a portable printing layer for
UNIX© operating systems. This package contains command-line client
programs.

%description devel
CUPS printing system provides a portable printing layer for
UNIX© operating systems. This is the development package for creating
additional printer drivers, and other CUPS services.

%description libs
CUPS printing system provides a portable printing layer for
UNIX© operating systems. It has been developed by Apple Inc.
to promote a standard printing solution for all UNIX vendors and users.
CUPS provides the System V and Berkeley command-line interfaces.
CUPS was ported to OS/2 to have the same benefit as UNIX has.
The cups-libs package provides libraries used by applications to use CUPS
natively, without needing the lpp/lpr commands.

%description filesystem
CUPS printing system provides a portable printing layer for
UNIX© operating systems. This package provides some directories which are
required by other packages that add CUPS drivers (i.e. filters, backends etc.)

%description lpd
CUPS printing system provides a portable printing layer for
UNIX© operating systems. This is the package that provides standard
lpd emulation.

%description ipptool
Sends IPP requests to the specified URI and tests and/or displays the result.

%debug_package

%prep
%scm_setup

autoconf --force

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
# --with-rcdir=no - don't install SysV init script
# --with-system_groups=admin - add a value to SystemGroups parameter
CFLAGS="$RPM_OPT_FLAGS" CXXFLAGS="$RPM_OPT_FLAGS" LDFLAGS="$LDFLAGS $RPM_OPT_FLAGS" \
    %configure %{_dbus} %{_dnssd} %{_libusb1} %{_static} \
     --with-rcdir=no \
     --with-system_groups=admin \
     --with-cupsd_file_perm=755 \
     --with-domainsocket=/socket/cups.sock

# If we got this far, all prerequisite libraries must be here.
make

%install
# Make sure the RPM_BUILD_ROOT directory exists.
rm -rf $RPM_BUILD_ROOT

make BUILDROOT=$RPM_BUILD_ROOT install

# rename some files
mv %{buildroot}%{_mandir}/man1/cancel.1.gz %{buildroot}%{_mandir}/man1/cancel-cups.1.gz
mv %{buildroot}%{_mandir}/man1/lp.1.gz %{buildroot}%{_mandir}/man1/lp-cups.1.gz
mv %{buildroot}%{_mandir}/man1/lpq.1.gz %{buildroot}%{_mandir}/man1/lpq-cups.1.gz
mv %{buildroot}%{_mandir}/man1/lprm.1.gz %{buildroot}%{_mandir}/man1/lprm-cups.1.gz
mv %{buildroot}%{_mandir}/man1/lpstat.1.gz %{buildroot}%{_mandir}/man1/lpstat-cups.1.gz
mv %{buildroot}%{_mandir}/man8/lpc.8.gz %{buildroot}%{_mandir}/man8/lpc-cups.8.gz

# Ship an rpm macro for where to put driver executables
mkdir -p %{buildroot}/%{_rpmconfigdir}/macros.d
install -m 0644 %{_builddir}/%{buildsubdir}/macros.cups %{buildroot}%{_rpmconfigdir}/macros.d

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README.txt CREDITS.txt CHANGES.txt
%docdir %{_datadir}/doc/cups
%defattr(-,root,root)
%dir %{_sysconfdir}/cups
%config(noreplace) %{_sysconfdir}/cups/*.conf
%{_sysconfdir}/cups/cups-files.conf.default
%{_sysconfdir}/cups/cupsd.conf.default
%{_sysconfdir}/cups/snmp.conf.default
%dir %{_sysconfdir}/cups/interfaces
%dir %{_sysconfdir}/cups/ppd
%attr(0700,root,root) %dir %{_sysconfdir}/cups/ssl

%if %{?_with_dbus:1}%{!?_with_dbus:0}
# DBUS
%{_sysconfdir}/dbus-1/system.d/*
%endif

%{_bindir}/cupstestdsc.exe
%{_bindir}/cupstestppd.exe
%dir %{_libdir}/cups
%dir %{_libdir}/cups/backend
%if %{?_with_dnssd:1}%{!?_with_dnssd:0}
# DNS-SD
%{_libdir}/cups/backend/dnssd
%endif
%{_libdir}/cups/backend/http
#{_libdir}/cups/backend/https
%attr(0700,root,root) %{_libdir}/cups/backend/ipp.exe
#{_libdir}/cups/backend/ipps
%attr(0700,root,root) %{_libdir}/cups/backend/lpd.exe
%{_libdir}/cups/backend/snmp.exe
%{_libdir}/cups/backend/socket.exe
%{_libdir}/cups/backend/usb.exe
%dir %{_libdir}/cups/cgi-bin
%{_libdir}/cups/cgi-bin/*.cgi
%dir %{_libdir}/cups/daemon
%{_libdir}/cups/daemon/cups-deviced.exe
%{_libdir}/cups/daemon/cups-driverd.exe
%{_libdir}/cups/daemon/cups-exec.exe
%dir %{_libdir}/cups/driver
%dir %{_libdir}/cups/filter
%{_libdir}/cups/filter/*
%exclude %{_libdir}/cups/filter/*.dbg
%dir %{_libdir}/cups/monitor
%{_libdir}/cups/monitor/*.exe
%dir %{_libdir}/cups/notifier
%{_libdir}/cups/notifier/*.exe

%{_sbindir}/cups*
%exclude %{_sbindir}/cups*.dbg
%{_sbindir}/lpadmin.exe
%{_sbindir}/lpinfo.exe
%{_sbindir}/lpmove.exe
%{_sbindir}/accept
%{_sbindir}/reject
%{_datadir}/cups/drv/*
%{_datadir}/cups/mime/*
%{_datadir}/cups/ppdc/*
%dir %{_datadir}/cups/templates
%{_datadir}/cups/templates/*
%if %{?_with_libusb1:1}%{!?_with_libusb1:0}
# LIBUSB quirks files
%dir %{_datadir}/cups/usb
%{_datadir}/cups/usb/*
%endif

%dir %{_datadir}/doc/cups
%{_datadir}/doc/cups/*.*
%dir %{_datadir}/doc/cups/help
%{_datadir}/doc/cups/help/accounting.html
%{_datadir}/doc/cups/help/cgi.html
%{_datadir}/doc/cups/help/glossary.html
%{_datadir}/doc/cups/help/kerberos.html
%{_datadir}/doc/cups/help/license.html
%{_datadir}/doc/cups/help/man-*.html
%{_datadir}/doc/cups/help/network.html
%{_datadir}/doc/cups/help/options.html
%{_datadir}/doc/cups/help/overview.html
%{_datadir}/doc/cups/help/policies.html
%{_datadir}/doc/cups/help/ref-*.html
%{_datadir}/doc/cups/help/security.html
%{_datadir}/doc/cups/help/sharing.html
%{_datadir}/doc/cups/help/translation.html
%dir %{_datadir}/doc/cups/images
%{_datadir}/doc/cups/images/*

%dir %{_datadir}/doc/cups/de
%{_datadir}/doc/cups/de/*
%dir %{_datadir}/doc/cups/es
%{_datadir}/doc/cups/es/*
%dir %{_datadir}/doc/cups/ja
%{_datadir}/doc/cups/ja/*
%dir %{_datadir}/doc/cups/ru
%{_datadir}/doc/cups/ru/*

%{_datadir}/locale/*

%dir %{_datadir}/man
%dir %{_datadir}/man/man1
%{_datadir}/man/man1/*.1.gz
%exclude %{_datadir}/man/man1/ppd*.1.gz
%exclude %{_datadir}/man/man1/cups-config.1.gz
%exclude %{_datadir}/man/man1/ipptool*.1.gz
%exclude %{_datadir}/man/man1/cancel-cups*.1.gz
%exclude %{_datadir}/man/man1/lp*.1.gz
%dir %{_datadir}/man/man5
%{_datadir}/man/man5/*.5.gz
%exclude %{_datadir}/man/man5/ppdcfile.5.gz
%exclude %{_datadir}/man/man5/ipptool*.5.gz
%dir %{_datadir}/man/man8
%{_datadir}/man/man8/*.8.gz
%exclude %{_datadir}/man/man8/cups-lpd.8.gz
%exclude %{_datadir}/man/man8/lpc-cups.8.gz

%dir %{_var}/cache/cups
%attr(0775,root,root) %dir %{_var}/cache/cups/rss
%dir %{_var}/log/cups
%dir %{_var}/run/cups
#attr(0711,root,root) %dir %{_var}/run/cups/certs
%attr(0710,root,root) %dir %{_var}/spool/cups
%attr(1770,root,root) %dir %{_var}/spool/cups/tmp

%files client
%{_sbindir}/lpc.exe
%{_bindir}/cancel.exe
%{_bindir}/lp*.exe
%dir %{_datadir}/man/man1
%{_datadir}/man/man1/lp*.1.gz
%{_datadir}/man/man1/cancel-cups*.1.gz
%dir %{_datadir}/man/man8
%{_datadir}/man/man8/lpc-cups.8.gz

%files libs
%doc LICENSE.txt
%defattr(-,root,root)
%{_libdir}/*.dll

%files filesystem
%dir %{_libdir}/cups
%dir %{_libdir}/cups/backend
%dir %{_libdir}/cups/driver
%dir %{_libdir}/cups/filter
%dir %{_datadir}/cups
%dir %{_datadir}/cups/data
%dir %{_datadir}/cups/drv
%dir %{_datadir}/cups/mime
%dir %{_datadir}/cups/model
%dir %{_datadir}/cups/ppdc
#dir %{_datadir}/ppd

%files devel
%defattr(-,root,root)
%{_bindir}/cups-config
%{_bindir}/ppd*.exe
%{_libdir}/*.a
%dir %{_includedir}/cups
%{_includedir}/cups/*
%{_rpmconfigdir}/macros.d/macros.cups

%dir %{_datadir}/cups/examples
%{_datadir}/cups/examples/*
%dir %{_datadir}/man
%dir %{_datadir}/man/man1
%{_datadir}/man/man1/cups-config.1.gz
%{_datadir}/man/man1/ppd*.1.gz
%dir %{_datadir}/man/man5
%{_datadir}/man/man5/ppdcfile.5.gz
%dir %{_datadir}/man/man7
%{_datadir}/man/man7/backend.7.gz
%{_datadir}/man/man7/filter.7.gz
%{_datadir}/man/man7/notifier.7.gz

%if %{?_with_static:1}%{!?_with_static:0}
%{_libdir}/*_s.a
%endif

%dir %{_datadir}/doc/cups/help
%{_datadir}/doc/cups/help/api*.html
%{_datadir}/doc/cups/help/postscript-driver.html
%{_datadir}/doc/cups/help/ppd-compiler.html
%{_datadir}/doc/cups/help/raster-driver.html
%{_datadir}/doc/cups/help/spec*.html

%files lpd
%defattr(-,root,root)
%if %{?_with_systemd:1}%{!?_with_systemd:0}
# SystemD
%{_libdir}/systemd/system/org.cups.cups-lpd*
%else
# Legacy xinetd
#{_sysconfdir}/xinetd.d/cups-lpd
%endif

%dir %{_libdir}/cups
%dir %{_libdir}/cups/daemon
%{_libdir}/cups/daemon/cups-lpd.exe
%dir %{_datadir}/man/man8
%{_datadir}/man/man8/cups-lpd.8.gz

%files ipptool
%defattr(-,root,root)
%if %{?_with_dnssd:1}%{!?_with_dnssd:0}
%{_bindir}/ippfind.exe
%endif
%{_bindir}/ipptool.exe
%dir %{_datadir}/cups/ipptool
%{_datadir}/cups/ipptool/*
%dir %{_datadir}/man/man1
%{_datadir}/man/man1/ipptool*.1.gz
%dir %{_datadir}/man/man5
%{_datadir}/man/man5/ipptool*.5.gz

%changelog
* Mon Nov 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-10
- add ETC to the env, as otherwise tcpip32.dll doesn't find any dns names

* Tue Oct 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-9
- moved source to github
- fixed a regression of the below /socket/cups.sock change

* Tue Aug 22 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-8
- add bldlevel to the dll
- fix search for ppd in cups-driver
- change LIBS
- change /@unixroot/var/run/cups/cups.sock to /socket/cups.sock
- adjust spec to scm_ macros usage

* Thu May 12 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-7
- fix timestamps absence in the jobs part of the webinterface

* Wed May 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-6
- disable the use of poll completely (fixes printing of large pdf)

* Fri Apr 29 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-5
- fix version info in german index.html (upstream bug)
- workaround for the webinterface issues (select() hack)
- remove .exe in httpSeperateURI
- don't deliver readonly cupsd

* Tue Apr 19 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-4
- add req for cups-filters
- don't use posix_spawn

* Wed Mar 16 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-3
- ship a rpm macro for cups_serverbin
- removed dbg packages from sbin dir in normal installation

* Fri Mar 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-2
- removed dbg packages from normal installation
- added SystemGroups value
- fixed some pipe() problems

* Mon Mar 07 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.3-1
- updated to version 2.1.3

* Fri Mar 04 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.8-5
- fixed lpd
- added more socketpair vs pipe changes
- also compress and strip debug info from cgi files

* Tue Jan 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.8-4
- poppler-utils needs to be at least 0.38.0-2
- remove wrong req for cups-lpr
- install all .a files for the dll

* Mon Jan 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.8-3
- rebuild with latest libraries
- adjusted debug package creation to latest rpm macros
- add poppler-utils as a requirement

* Sun Feb 15 2015 yd <yd@os2power.com> 1.4.8-1 1.4.8-2
- rebuild for new libpng release.

* Thu Dec 18 2014 yd
- r944, initial unixroot build.
