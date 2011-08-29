#disable lxlite strip (removes rexx code)
%define __os_install_post	%{nil}

Summary: REXX procedure used to modify a CONFIG.SYS-like ASCII file
Name: cube
Version: 2.6
Release: 4%{?dist}
License: none
URL: http://www3.sympatico.ca/gjarviseng/cube/

Group: System Environment/Shells

Source: cube.zip

%description
CUBE is a REXX procedure used to modify a CONFIG.SYS-like ASCII file (the Target File), based on a set of CUBE's commands (the Procedure File).

%prep
%setup -q -c

%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
mkdir -p $RPM_BUILD_ROOT/%{_libdir}/rpm
rexx2exe cube.cmd $RPM_BUILD_ROOT/%{_bindir}/cube.exe /K:0
rexx2exe wps-object.cmd $RPM_BUILD_ROOT/%{_libdir}/rpm/wps-object.exe /K:0

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/cube.exe
%{_libdir}/rpm/wps-object.exe
