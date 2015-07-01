# The default OS/2 Toolkit path, use --define to override on the command line
%if %{undefined os2_toolkit_path}
%define os2_toolkit_path D:/Tools/OS2TK45
%endif

Summary: K Audio Interface library for OS/2 multimedia subsystem
Name: libkai
Version: 1.1.4
Release: 1%{?dist}
License:  LGPLv2+
Group: System Environment/Libraries

%define github_name kai
%define github_url  https://github.com/komh/%{github_name}/archive
%define github_rev  kai-%{version}

Source: %{github_name}-%{github_rev}.zip

BuildRequires: gcc make curl zip

%description
K Audio Interface is a frontend library that simplifies access to OS/2
audio hardware making it easier to write programs that play sounds.
Currently, it supports playing sounds through the standard OS/2
MMPM/DART subsystem and through the UNIAUD driver directly.

%package devel
Summary: K Audio Interface developer package
Group: Development/Libraries
Requires: libkai = %{version}-%{release}

%description devel
Contains headers and libraries necessary to compile audio-enabled
applications that use K Audio Interface.

%package static
Summary: K Audio Interface static library
Group: Development/Libraries
Requires: libkai-devel = %{version}-%{release}

%description static
Contains headers the static K Audio Interface library.

%package debug
Summary: HLL debug data for libkai
Requires: libkai = %{version}-%{release}

%description debug
Contains symbol files necessary to generate proper crash reports
in applications using the libkai package.

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
make PREFIX=%{_prefix} CC="gcc -idirafter %{os2_toolkit_path}/h -DOS2EMX_PLAIN_CHAR"

%install
make PREFIX=%{_prefix} INSTALL=%{_bindir}/install DESTDIR=%{buildroot} install
# No need in .a once we have .lib
rm -f %{buildroot}/%{_libdir}/*.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.dll

%files devel
%defattr(-,root,root)
%{_includedir}/*.h
%{_libdir}/*_dll.lib

%files static
%defattr(-,root,root)
%exclude %{_libdir}/*_dll.lib
%{_libdir}/*.lib

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Wed Jul 1 2015 Dmitriy Kuminov <coding@dmik.org> 1.1.4-1
- Initial package for version 1.1.4.
