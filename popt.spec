%define name popt
%define version 1.15

Summary:	C library for parsing command line parameters
Name:		%{name}
Version:	%{version}
Release:	1
Epoch:		1
License:	MIT
Group:		System/Libraries
Url:		http://rpm5.org/files/popt/
Source0:	http://rpm5.org/files/popt/%{name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires: popt-libs

%description
Popt is a C library for parsing command line parameters. Popt was
heavily influenced by the getopt() and getopt_long() functions, but
it improves on them by allowing more powerful argument expansion.
Popt can parse arbitrary argv[] style arrays and automatically set
variables based on command line arguments. Popt allows command line
arguments to be aliased via configuration files and includes utility
functions for parsing arbitrary strings into argv[] arrays using
shell-like rules.

%package libs
Summary:	Main %{name} library
Group:		System/Libraries
Requires:	popt-data = %{epoch}:%{version}

%description libs
This package contains the library needed to run programs dynamically
linked with the %{name} library.

%package devel
Summary:	Development headers and libraries for %{name}
Group:		Development/C
Requires:	popt-libs >= %{epoch}:%{version}

%description devel
This package contains the header files and libraries needed for
developing programs using the %{name} library.

%package data
Summary:	Data files for %{name}
Group:		System/Libraries

%description data
This package contains popt data files like locales.

%prep
%setup -q

%build
CONFIG_SHELL="/bin/sh" ; export CONFIG_SHELL ; \
%configure --disable-rpath \
    --disable-shared --enable-static \
        "--cache-file=%{_topdir}/cache/%{name}.cache"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make DESTDIR=${RPM_BUILD_ROOT} install
#%find_lang %name

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README

%files libs
%defattr(-,root,root)
%doc README
#/%{_lib}/lib%{name}.so.%{lib_major}*

%files devel
%defattr(-,root,root)
%{_includedir}/%{name}.h
%{_libdir}/%{name}*a
%{_libdir}/lib%{name}*a
#/%{_lib}/lib%{name}.so
%{_mandir}/man3/popt.*

%files data
# -f %{name}.lang
%defattr(-,root,root)
%{_usr}/share/locale/cs/LC_MESSAGES/popt.mo
%{_usr}/share/locale/da/LC_MESSAGES/popt.mo
%{_usr}/share/locale/de/LC_MESSAGES/popt.mo
%{_usr}/share/locale/eo/LC_MESSAGES/popt.mo
%{_usr}/share/locale/es/LC_MESSAGES/popt.mo
%{_usr}/share/locale/fi/LC_MESSAGES/popt.mo
%{_usr}/share/locale/fr/LC_MESSAGES/popt.mo
%{_usr}/share/locale/ga/LC_MESSAGES/popt.mo
%{_usr}/share/locale/gl/LC_MESSAGES/popt.mo
%{_usr}/share/locale/hu/LC_MESSAGES/popt.mo
%{_usr}/share/locale/id/LC_MESSAGES/popt.mo
%{_usr}/share/locale/is/LC_MESSAGES/popt.mo
%{_usr}/share/locale/it/LC_MESSAGES/popt.mo
%{_usr}/share/locale/ja/LC_MESSAGES/popt.mo
%{_usr}/share/locale/ko/LC_MESSAGES/popt.mo
%{_usr}/share/locale/nb/LC_MESSAGES/popt.mo
%{_usr}/share/locale/nl/LC_MESSAGES/popt.mo
%{_usr}/share/locale/pl/LC_MESSAGES/popt.mo
%{_usr}/share/locale/pt/LC_MESSAGES/popt.mo
%{_usr}/share/locale/ro/LC_MESSAGES/popt.mo
%{_usr}/share/locale/ru/LC_MESSAGES/popt.mo
%{_usr}/share/locale/sk/LC_MESSAGES/popt.mo
%{_usr}/share/locale/sl/LC_MESSAGES/popt.mo
%{_usr}/share/locale/sv/LC_MESSAGES/popt.mo
%{_usr}/share/locale/th/LC_MESSAGES/popt.mo
%{_usr}/share/locale/tr/LC_MESSAGES/popt.mo
%{_usr}/share/locale/uk/LC_MESSAGES/popt.mo
%{_usr}/share/locale/vi/LC_MESSAGES/popt.mo
%{_usr}/share/locale/wa/LC_MESSAGES/popt.mo
%{_usr}/share/locale/zh_CN/LC_MESSAGES/popt.mo
%{_usr}/share/locale/zh_TW/LC_MESSAGES/popt.mo


%changelog
