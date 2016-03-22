#define svn_url     e:/trees/gutenprint/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/gutenprint/trunk
%define svn_rev     1467

Name:           gutenprint
Summary:        Printer Drivers Package
Version:        5.2.11
Release:        1%{?dist}
URL:            http://gimp-print.sourceforge.net/
License:        GPLv2+
Vendor:         bww bitwise works GmbH
Source:         %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Requires:       %{name}-libs = %{version}-%{release}
BuildRequires:  cups-libs, cups-devel, cups
BuildRequires:  gettext-devel,pkgconfig
BuildRequires:  libtiff-devel,libjpeg-devel,libpng-devel
BuildRequires:  libusb1-devel
#BuildRequires:  foomatic
BuildRequires:  ghostscript-devel

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

#package foomatic
#Summary:        Foomatic printer database information for gutenprint
#Requires:       %{name} = %{version}-%{release}
#Requires(post): foomatic
# python3-cups is required for the update script (bug #1226871)
#Requires(post): python3-cups
#Requires:       foomatic-db

#description  foomatic
#This package contains a database of printers,printer drivers,
#and driver descriptions.

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
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
# rebuild all configure and the like files
export NOCONFIGURE=1
autogen.sh

export LDFLAGS=" -Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
#  --with-foomatic 
%configure --disable-static --enable-shared  \
            --with-modules=no --with-ghostscript \
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
rm -f %{buildroot}%{_sysconfdir}/cups/command.types

%find_lang %{name}
sed 's!%{_datadir}/locale/\([^/]*\)/LC_MESSAGES/gutenprint.mo!%{_datadir}/locale/\1/gutenprint_\1.po!g' %{name}.lang >%{name}-po.lang
rm -f %{name}.lang
%find_lang %{name} --all-name
cat %{name}-po.lang >>%{name}.lang

echo .so man1/ijsgutenprint.1 > %{buildroot}%{_mandir}/man1/ijsgutenprint.5.2.1
echo .so man8/cups-genppd.8 > %{buildroot}%{_mandir}/man8/cups-genppd.5.2.8

#post libs -p /sbin/ldconfig

#postun libs -p /sbin/ldconfig

%post cups
%{_sbindir}/cups-genppdupdate >/dev/null 2>&1 || :
#/sbin/service cups reload >/dev/null 2>&1 || :
exit 0


%files -f %{name}.lang
%doc COPYING
%{_bindir}/escputil.exe
%{_mandir}/man1/escputil.1*
%{_bindir}/ijsgutenprint.5.2.exe
%{_mandir}/man1/ijsgutenprint.5.2.1*
%{_mandir}/man1/ijsgutenprint.1*
%{_datadir}/gutenprint/5.2

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

#%files foomatic
#doc 
#{_sbindir}/gutenprint-foomaticppdupdate
#{_mandir}/man8/gutenprint-foomaticppdupdate.8*
#{_datadir}/foomatic/db/source/driver/*
#{_datadir}/foomatic/db/source/opt/*

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
%{_mandir}/man8/cups-calibrate.8*
%{_mandir}/man8/cups-genppd*.8*

#post foomatic
#rm -f /var/cache/foomatic/*
#if [ $1 -eq 2 ]; then
#  %{_sbindir}/gutenprint-foomaticppdupdate %{version} >/dev/null 2>&1 || :
#fi

#postun foomatic
#rm -f /var/cache/foomatic/*

%changelog
* Tue Mar 22 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 5.2.11-1
- first version
