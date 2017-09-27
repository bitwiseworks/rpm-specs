# *** to build lxLite you need a working VirtualPascal installation ***
# *** and the VPDIR env must be set                                 ***

Summary:       OS/2 LX executable packer
Name:          lxLite
Version:       1.3.9
Release:       2%{?dist}
License:       GPL
Group:         Applications/System
URL:           http://github.com/bitwiseworks/lxlite
Vendor:        bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/lxlite %{version}

%description
This package provides lxLite packer


%package tools
Summary:       lxLite utilities
Requires:      %{name} = %{version}-%{release}

%description tools
This package provides some tools from the lxLite package


%prep
%scm_setup


%build
cd src
make.cmd
cd ..


%install
# install exe
cd src
cd out
for f in *.exe ; do
  install -p -m0644 -D $f  $RPM_BUILD_ROOT%{_bindir}/$f
done
cd ..
cd ..

# install stub
cd contrib
for f in stub* ; do
  install -p -m0644 -D $f  $RPM_BUILD_ROOT%{_datadir}/%{name}/$f
done
cd ..

install -p -m0644 -D contrib/lxLite.cfg $RPM_BUILD_ROOT%{_sysconfdir}/%{name}/lxLite.cfg

%clean
rm -rf "$RPM_BUILD_ROOT"

%post


%postun


%files
%doc doc/lxLite_documentation.txt doc/gpl.txt doc/whatsnew.txt
%dir %{_sysconfdir}/%{name}
%config(noreplace) %{_sysconfdir}/%{name}/*.cfg
%{_bindir}/lxLite.exe
%{_datadir}/%{name}/stub*

%files tools
%doc doc/lxUtil.txt
%{_bindir}/*.exe
%exclude %{_bindir}/lxLite.exe

%changelog
* Tue Sep 26 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.3.9-2
- create the {_sysconfdir}/lxLite is not available

* Tue Sep 26 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.3.9-1
- first rpm release
