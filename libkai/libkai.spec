# The default OS/2 Toolkit path, use --define to override on the command line
Summary: K Audio Interface library for OS/2 multimedia subsystem
Name: libkai
Version: 1.2.0
Release: 1%{?dist}
License:  LGPLv2+
Group: System Environment/Libraries
Vendor: bww bitwise works GmbH
URL: https://github.com/komh/kai

%define github_name kai
%define github_url  https://github.com/komh/%{github_name}/archive
%define github_rev  kai-%{version}

Source: %{github_name}-%{github_rev}.zip

BuildRequires: gcc make curl zip

BuildRequires: os2tk45-headers os2tk45-libs

%description
K Audio Interface is a frontend library that simplifies access to OS/2
audio hardware making it easier to write programs that play sounds.
Currently, it supports playing sounds through the standard OS/2
MMPM/DART subsystem and through the UNIAUD driver directly.

%package devel
Summary: K Audio Interface developer package
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Contains headers and libraries necessary to compile audio-enabled
applications that use K Audio Interface.

%package static
Summary: K Audio Interface static library
Group: Development/Libraries
Requires: %{name}-devel = %{version}-%{release}

%description static
Contains headers the static K Audio Interface library.

%debug_package

%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -n "%{github_name}-%{github_rev}" -q
%else
%setup -n "%{github_name}-%{github_rev}" -Tc
rm -f "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
curl -sSL "%{github_url}/%{github_rev}.zip" -o "%{_sourcedir}/%{github_name}-%{github_rev}.zip"
unzip "%{_sourcedir}/%{github_name}-%{github_rev}.zip" -d ..
%endif

%build
make PREFIX=%{_prefix} CC="gcc -idirafter %{_includedir}/os2tk45 -DOS2EMX_PLAIN_CHAR"

%install
make PREFIX=%{_prefix} INSTALL=%{_bindir}/install DESTDIR=%{buildroot} install

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.dll

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*_dll.*

%files static
%defattr(-,root,root)
%exclude %{_libdir}/*_dll.*
%{_libdir}/*.*

%changelog
* Thu Jan 28 2016 Dmitriy Kuminov <coding@dmik.org> 1.2.0-1
- Update to version 1.2.0 from vendor:
+ uniaud: Fix device selection by index.
+ uniaud: Improve volume control.
- Add .a libraries (for use with ld, e.g. in non-Zomf mode).

* Wed Jul 1 2015 Dmitriy Kuminov <coding@dmik.org> 1.1.4-1
- Initial package for version 1.1.4.
