# *** to build lxLite you need a working VirtualPascal installation ***
# *** and the VPDIR env must be set                                 ***

Summary:       OS/2 LX executable packer
Name:          lxlite
Version:       1.3.9
Release:       6%{?dist}
License:       GPL
Group:         Applications/System
URL:           http://github.com/bitwiseworks/lxlite
Vendor:        bww bitwise works GmbH
Obsoletes:     lxLite
Provides:      lxLite = %{version}-%{release}
%scm_source github https://github.com/bitwiseworks/lxlite %{version}


%description
This package provides lxLite packer


%package tools
Summary:       lxLite utilities
Requires:      %{name} = %{version}-%{release}
Obsoletes:     lxLite-tools
Provides:      lxLite-tools = %{version}-%{release}

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
  install -p -m0755 -D $f  $RPM_BUILD_ROOT%{_bindir}/$f
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
* Wed Feb 28 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.3.9-6
- add the executable flag to the exe

* Tue Oct 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.3.9-5
- added a provides/obsoletes for lxLite-tools as well

* Tue Oct 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.3.9-4
- renamed package from lxLite to lxlite
- added a provides/obsoletes for lxLite

* Fri Sep 29 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.3.9-3
- don't write the help screen to stderr

* Tue Sep 26 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.3.9-2
- create the {_sysconfdir}/lxLite directory if not available

* Tue Sep 26 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.3.9-1
- first rpm release
