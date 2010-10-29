#disable lxlite strip (removes rexx code)
%define __os_install_post	%{nil}

Summary: REXX procedure used to modify a CONFIG.SYS-like ASCII file
Name: cube
Version: 2.6
Release: 1
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
rexx2exe cube.cmd $RPM_BUILD_ROOT/%{_bindir}/cube.exe

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/cube.exe
