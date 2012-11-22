Summary: Creates a common metadata repository
Name: createrepo
Version: 0.4.11
Release: 2
License: GPL
Group: System Environment/Base
Source: %{name}-%{version}.tar.gz
Patch0: createrepo-os2.patch
URL: http://linux.duke.edu/metadata/
BuildRoot: %{_tmppath}/%{name}-%{version}root
BuildArchitectures: noarch
Requires: python >= 2.1, rpm-python, rpm >= 0:4.1.1, libxml2-python
Requires: yum-metadata-parser

%description
This utility will generate a common metadata repository from a directory of
rpm packages

%prep
%setup -q
%patch0 -p1

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, root)
%dir %{_datadir}/%{name}
%doc ChangeLog README COPYING COPYING.lib
%{_datadir}/%{name}/*
%{_bindir}/%{name}
%{_bindir}/modifyrepo
%{_mandir}/man8/createrepo.8*

%changelog
* Thu Nov 22 2011 yd
- fixed /@unixroot access

* Fri Sep 03 2010 yd
- initial build
