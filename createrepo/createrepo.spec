%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

# disable broken /usr/lib/rpm/brp-python-bytecompile
%define __os_install_post %{nil}
%define compdir %(pkg-config --variable=completionsdir bash-completion)
%if "%{compdir}" == ""
%define compdir "/@unixroot/etc/bash_completion.d"
%endif

Summary: Creates a common metadata repository
Name: createrepo
Version: 0.10.4
Release: 3%{?dist}
License: GPLv2
Group: System Environment/Base
URL: http://createrepo.baseurl.org/

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArchitectures: noarch
Requires: python >= 2.1, rpm-python, rpm >= 4.1.1, libxml2-python
Requires: yum-metadata-parser, yum >= 3.4.3, python-deltarpm, deltarpm, pyliblzma
BuildRequires: python

Vendor: bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/createrepo/trunk 2317

%description
This utility will generate a common metadata repository from a directory of rpm
packages.

%prep
%scm_setup

%build

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT sysconfdir=%{_sysconfdir} install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root,-)
%doc ChangeLog README
%license COPYING COPYING.lib
%(dirname %{compdir})
%{_datadir}/%{name}/
%{_bindir}/createrepo
%{_bindir}/modifyrepo
%{_bindir}/mergerepo
%{_mandir}/*/*
%{python_sitelib}/createrepo

%changelog
* Sun Dec 30 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.10.4-3
- fix verbose and messages output to stdout (rpm ticket #325)

* Fri Nov 09 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.10.4-2
- fix amount of workers
- fix select() issue on stdout/stderr

* Tue Dec 19 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.10.4-1
- update to vendor version 0.10.4

* Tue Nov 22 2011 yd
- fixed /@unixroot access

* Fri Sep 03 2010 yd
- initial build
