Name:           gutenprint
Summary:        Printer Drivers Package
Version:        5.3.3
Release:        2%{?dist}
URL:            http://gimp-print.sourceforge.net/
License:        GPLv2+

Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/gutenprint-os2 %{version}-os2

Requires:       %{name}-libs = %{version}-%{release}
BuildRequires:  cups-libs, cups-devel, cups
BuildRequires:  gettext-devel,pkgconfig
BuildRequires:  libtiff-devel,libjpeg-devel,libpng-devel
BuildRequires:  libusb1-devel

# Make sure we get postscriptdriver tags.
#BuildRequires:  python3-cups

# autoreconf
BuildRequires: autoconf automake libtool

## NOTE ##
# The README file in this package contains suggestions from upstream
# on how to package this software. I'd be inclined to follow those
# suggestions unless there's a good reason not to do so.

%description
Gutenprint is a package of high quality printer drivers for Linux, BSD,
Solaris, IRIX, and other UNIX-alike operating systems.
Gutenprint was formerly called Gimp-Print.

%package doc
Summary:        Documentation for gutenprint

%description doc
Documentation for gutenprint.

%package libs
Summary:       libgutenprint library

%description libs
This package includes libgutenprint library, necessary to run gutenprint.

%package devel
Summary:        Library development files for gutenprint
Requires:       %{name} = %{version}-%{release}

%description devel
This package contains headers and libraries required to build applications that
uses gutenprint package.

%package extras
Summary:        Sample test pattern generator for gutenprint-devel
Requires:       %{name} = %{version}-%{release}

%description extras
This package contains test pattern generator and the sample test pattern
that is used by gutenprint-devel package.

%package cups
Summary:        CUPS drivers for Canon, Epson, HP and compatible printers
Requires:       cups
Requires:       %{name} = %{version}-%{release}

%description cups
This package contains native CUPS support for a wide range of Canon,
Epson, HP and compatible printers.

%debug_package

%prep
%scm_setup

%build
# rebuild all configure and the like files
touch %{_builddir}/%{buildsubdir}/doc/developer/html-stamp

export NOCONFIGURE=1
autogen.sh

export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure --disable-static --enable-shared  \
            --with-modules=no \
            --enable-samples --enable-escputil \
            --enable-test --disable-rpath \
            --enable-cups-1_2-enhancements \
            --disable-cups-ppds \
            --enable-simplified-cups-ppds

# this export is needed, as else the dll for the tests are not found
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/main/.libs
make %{?_smp_mflags}

%check
# Test suite disabled due to too long runtime
# this export is needed, as else the dll for the tests are not found
#export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/main/.libs
#make check
 
%install
make DESTDIR=%{buildroot} install

# Don't ship libtool la files.
rm -f %{buildroot}%{_libdir}/lib*.la

rm -rf %{buildroot}%{_datadir}/gutenprint/doc
rm -f %{buildroot}%{_datadir}/foomatic/kitload.log
rm -rf %{buildroot}%{_libdir}/gutenprint/5.3/modules/*.la
rm -f %{buildroot}%{_sysconfdir}/cups/command.types

%find_lang %{name}
sed 's!%{_datadir}/locale/\([^/]*\)/LC_MESSAGES/gutenprint.mo!%{_datadir}/locale/\1/gutenprint_\1.po!g' %{name}.lang >%{name}-po.lang
rm -f %{name}.lang
%find_lang %{name} --all-name
cat %{name}-po.lang >>%{name}.lang

echo .so man8/cups-genppd.8 > %{buildroot}%{_mandir}/man8/cups-genppd.5.3.3

#post libs -p /sbin/ldconfig

#postun libs -p /sbin/ldconfig

%post cups
%{_sbindir}/cups-genppdupdate -x >/dev/null 2>&1 || :
#/sbin/service cups reload >/dev/null 2>&1 || :
exit 0


%files -f %{name}.lang
%doc COPYING
%{_bindir}/escputil.exe
%{_mandir}/man1/escputil.1*
%{_datadir}/%{name}/5.3

%files doc
%doc COPYING AUTHORS NEWS README doc/FAQ.html doc/gutenprint-users-manual.odt doc/gutenprint-users-manual.pdf

%files libs
%{_libdir}/gutenpr*.dll

%files devel
%doc ChangeLog doc/developer/reference-html doc/developer/gutenprint.pdf
%doc doc/gutenprint
%{_includedir}/gutenprint/
%{_libdir}/*.a
%{_libdir}/pkgconfig/gutenprint.pc
%{_libdir}/%{name}/5.3/config.summary

%files extras
%doc
%{_bindir}/testpattern.exe
%{_datadir}/gutenprint/samples/*

%files cups
%doc
%{_datadir}/cups/calibrate.ppm
%{_datadir}/cups/usb/net.sf.gimp-print.usb-quirks
%{_cups_serverbin}/filter/*.exe
%{_cups_serverbin}/driver/*.exe
%{_cups_serverbin}/backend/*.exe
%{_bindir}/cups-calibrate.exe
%{_sbindir}/cups-genppd*.exe
%{_sbindir}/cups-genppdupdate
%{_mandir}/man8/cups-calibrate*
%{_mandir}/man8/cups-genppd*


%changelog
* Fri Oct 11 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.3.3-2
- update cups ppd files across versions

* Mon Oct 07 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.3.3-1
- update gutenprint to version 5.3.3

* Tue Mar 21 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.2.12-1
- use scm_ macros
- update gutenprint to version 5.2.12

* Fri May 13 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.2.11-3
- escape /@unixroot right and add binmode to cups-genppdupdate script
- fix cups-genppdupdate to find the driver_bin

* Thu Apr 21 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.2.11-2
- remove Zbin-files

* Tue Mar 22 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.2.11-1
- first version
