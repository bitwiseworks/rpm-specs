%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
 
Summary: RPM installer/updater
Name: yum
Version: 3.4.3
Release: 11%{?dist}
License: GPLv2+
Group: System Environment/Base
Vendor: bww bitwise works GmbH

%scm_source svn http://svn.netlabs.org/repos/rpm/yum/trunk 1154

Source1: exec-py.c

URL: http://yum.baseurl.org/

BuildRequires: python
BuildRequires: gettext
BuildRequires: intltool

Conflicts: pirut < 1.1.4

Requires: python >= 2.4, rpm-python, rpm >= 0:4.4.2
#Requires: python-iniparse
Requires: python-sqlite
Requires: urlgrabber >= 3.1.0-0
Requires: yum-metadata-parser >= 1.1.0
#Requires: pygpgme
Obsoletes: yum-skip-broken <= 1.1.18
Obsoletes: yum-basearchonly <= 1.1.9
Obsoletes: yum-allow-downgrade < 1.1.20-0
Obsoletes: yum-plugin-allow-downgrade < 1.1.22-0
Obsoletes: yum-plugin-protect-packages < 1.1.27-0
Provides: yum-skip-broken
Provides: yum-basearchonly
Provides: yum-allow-downgrade
Provides: yum-plugin-allow-downgrade
Provides: yum-protect-packages
Provides: yum-plugin-protect-packages
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded 
automatically, prompting the user for permission as necessary.

%debug_package

%prep
%scm_setup

%build
export PERL_SH_DIR="/@unixroot/usr/bin"
make

#build exe wrapper
%{__cp} %SOURCE1 .
gcc -g -Zomf %optflags -DPYTHON_EXE=\"python%{python_version}.exe\" -o %{name}.exe exec-py.c

%install
rm -rf $RPM_BUILD_ROOT
export PERL_SH_DIR="%{_bindir}"
make DESTDIR=$RPM_BUILD_ROOT install
#install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/yum.conf
#mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d $RPM_BUILD_ROOT/usr/lib/yum-plugins

#install exe wrapper
%{__install} -m 755 %{name}.exe $RPM_BUILD_ROOT/%{_bindir}

# for now, move repodir/yum.conf back
#mv $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d
#rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum.conf

# yum-updatesd has moved to the separate source version
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum-updatesd.conf 
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/yum-updatesd
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/dbus-1/system.d/yum-updatesd.conf
rm -f $RPM_BUILD_ROOT/%{_sbindir}/yum-updatesd
rm -f $RPM_BUILD_ROOT/%{_mandir}/man*/yum-updatesd*
rm -f $RPM_BUILD_ROOT/%{_datadir}/yum-cli/yumupd.py*

# Ghost files:
mkdir -p $RPM_BUILD_ROOT/%{_var}/lib/yum/history
mkdir -p $RPM_BUILD_ROOT/%{_var}/lib/yum/plugins
mkdir -p $RPM_BUILD_ROOT/%{_var}/lib/yum/yumdb
touch $RPM_BUILD_ROOT/%{_var}/lib/yum/uuid

%find_lang %name


%clean
rm -rf $RPM_BUILD_ROOT


%files -f %{name}.lang
%defattr(-, root, root, -)
%doc README AUTHORS COPYING TODO INSTALL ChangeLog
%config(noreplace) %{_sysconfdir}/yum/yum.conf
%dir %{_sysconfdir}/yum
%config(noreplace) %{_sysconfdir}/yum/version-groups.conf
%{_sysconfdir}/yum/cron.daily
%dir %{_sysconfdir}/yum/protected.d
%{_sysconfdir}/yum/rc.d/init.d/*
%dir %{_sysconfdir}/yum/repos.d
%{_sysconfdir}/yum/sysconfig/*
%dir %{_sysconfdir}/yum/vars
%config(noreplace) %{_sysconfdir}/logrotate.d/yum
%{_sysconfdir}/yum/bash_completion.d/*
%dir %{_datadir}/yum-cli
%{_sysconfdir}/yum/yum-daily.yum
%{_sysconfdir}/yum/yum-weekly.yum
%{_datadir}/yum-cli/*
%{_bindir}/yum
%{_bindir}/yum.exe
#{python_sitelib}/yum
#{python_sitelib}/rpmUtils
%{_libdir}/*
%dir %{_var}/cache/yum
%dir %{_var}/lib/yum
%ghost %{_var}/lib/yum/uuid
%ghost %{_var}/lib/yum/history
%ghost %{_var}/lib/yum/plugins
%ghost %{_var}/lib/yum/yumdb
%{_mandir}/man*/yum.*
%{_mandir}/man*/yum-shell*
# plugin stuff
#dir {_sysconfdir}/yum/pluginconf.d 
#dir /usr/lib/yum-plugins


%changelog
* Mon Jun 5 2017 Dmitriy Kuminov <coding@dmik.org> 3.4.3-11
- Be nice and close transaction files before removing.
- Remove outdated sub-package leftovers from .spec.
- Use scm_source/scm_setup for downloading sources.

* Thu Jun 09 2016 yd <yd@os2power.com> 3.4.3-10
- r784, set bugtracker_url to Netlabs trac. ticket#184.

* Wed Feb 10 2016 yd <yd@os2power.com> 3.4.3-9
- r653, change default file path. fixes ticket#173.

* Tue Feb 10 2015 yd <yd@os2power.com> 3.4.3-8
- r527, do not rewrite paths starting with @unixroot.

* Tue Feb 03 2015 yd <yd@os2power.com> 3.4.3-7
- r516, update source code to version 3.4.3.

* Mon Apr 07 2014 yd
- build for python 2.7.

* Fri Mar 21 2014 yd
- build wrapper agains pythonX.Y.exe
- r396, makefiles updates for unixroot and python virtualenv changes.
- added debug package with symbolic info for exceptq.
