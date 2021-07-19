# The default OS/2 Toolkit path, use --define to override on the command line
Summary: K Audio Interface library for OS/2 multimedia subsystem
Name: libkai
Version: 2.1.0
Release: 1%{?dist}
License:  LGPLv2+
Vendor: bww bitwise works GmbH
URL: https://github.com/komh/kai

%scm_source github http://github.com/komh/kai kai-%{version}

# DEF files to create forwarders for the legacy package
Source10:       kai0.def

# patch to have emxomfstrip running and create a nicer bldlevel
Patch1: Makefile.patch

BuildRequires: gcc make curl zip

BuildRequires: os2tk45-headers os2tk45-libs

%description
K Audio Interface is a frontend library that simplifies access to OS/2
audio hardware making it easier to write programs that play sounds.
Currently, it supports playing sounds through the standard OS/2
MMPM/DART subsystem and through the UNIAUD driver directly.


%package devel
Summary: K Audio Interface developer package
Requires: %{name} = %{version}-%{release}

%description devel
Contains headers and libraries necessary to compile audio-enabled
applications that use K Audio Interface.


%package static
Summary: K Audio Interface static library
Requires: %{name}-devel = %{version}-%{release}

%description static
Contains headers the static K Audio Interface library.


%debug_package


%prep
%scm_setup
%patch1 -p0 -b .Makefile

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done


%build
make PREFIX=%{_prefix} CC="gcc -idirafter %{_includedir}/os2tk45 -DOS2EMX_PLAIN_CHAR -g"


%install
make PREFIX=%{_prefix} INSTALL=%{_bindir}/install DESTDIR=%{buildroot} install

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib %{SOURCE10} -l$RPM_BUILD_ROOT/%{_libdir}/kai1.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/kai0.dll


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
%{_libdir}/*.a
%{_libdir}/*.lib


%changelog
* Mon Jul 19 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.1.0-1
- Update to version 2.1.0 from vendor

* Fri Nov 13 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.0.0-1
- Update to version 2.0.0 from vendor
- add a forwarder to the older kai0.dll

* Thu Jan 28 2016 Dmitriy Kuminov <coding@dmik.org> 1.2.0-1
- Update to version 1.2.0 from vendor:
+ uniaud: Fix device selection by index.
+ uniaud: Improve volume control.
- Add .a libraries (for use with ld, e.g. in non-Zomf mode).

* Wed Jul 1 2015 Dmitriy Kuminov <coding@dmik.org> 1.1.4-1
- Initial package for version 1.1.4.
