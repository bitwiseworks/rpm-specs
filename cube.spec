#disable lxlite strip (removes rexx code)
%define __os_install_post	%{nil}

Summary: REXX procedure used to modify a CONFIG.SYS-like ASCII file
Name: cube
Version: 2.8
Release: 1%{?dist}
License: none
URL: http://www3.sympatico.ca/gjarviseng/cube/
Group: System Environment/Shells
Vendor: bww bitwise works GmbH

%scm_source svn http://svn.netlabs.org/repos/cube/trunk 4

BuildRequires: rexx_exe


%description
CUBE is a REXX procedure used to modify a CONFIG.SYS-like ASCII file
(the Target File), based on a set of CUBE's commands (the Procedure File).


%prep
%scm_setup


%build
rexx2vio cube.cmd cube.exe


%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
for f in *.exe ; do
  install -p -m 0755 -D $f  $RPM_BUILD_ROOT%{_bindir}/$f
done


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%doc cube.doc cube.ref
%{_bindir}/cube.exe


%changelog
* Fri Jun 15 2018 Silvan Scherrer <silvan.scherrer@aroa> 2.8-1
- gather all available sources together and join them
- install documentation
- use %scm_ and friends macros
