# Yum is Python 2 only, force it
%global __python %{_bindir}/python2

%if !0%{?os2_version}
%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%else
# Require the RPM-provided value (derived from __python) to have /@unixroot
# instead of a drive letter
%{!?python_sitelib:%{error:python_sitelib is not defined}}
%endif

%if !0%{?os2_version}
# We always used /usr/lib here, even on 64bit ... so it's a bit meh.
%define yum_pluginslib   /usr/lib/yum-plugins
%define yum_pluginsshare /usr/share/yum-plugins
%else
%define yum_pluginslib   %{_libdir}/yum-plugins
%define yum_pluginsshare %{_datadir}/yum-plugins
%endif

Summary: RPM package installer/updater/manager
Name: yum
Version: 3.4.3
Release: 15%{?dist}
License: GPLv2+
Group: System Environment/Base
Vendor: bww bitwise works GmbH

%if !0%{?os2_version}
Source0: http://yum.baseurl.org/download/3.4/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2-1
Source1: exec-py.c
%endif

URL: http://yum.baseurl.org/

%if !0%{?os2_version}
BuildArch: noarch
%else
# On OS/2, we provide an .exe wrapper
%endif
BuildRequires: python
BuildRequires: gettext
BuildRequires: intltool
%if !0%{?os2_version}
# This is really CheckRequires ...
BuildRequires: python-nose
BuildRequires: python >= 2.4, rpm-python, rpm >= 0:4.4.2
BuildRequires: python-iniparse
BuildRequires: python-sqlite
BuildRequires: python-urlgrabber >= 3.9.0-8
BuildRequires: yum-metadata-parser >= 1.1.0
BuildRequires: pygpgme
# End of CheckRequires
%endif
Conflicts: pirut < 1.1.4
Requires: python >= 2.4, rpm-python, rpm >= 0:4.4.2
%if !0%{?os2_version}
Requires: python-iniparse
%endif
Requires: urlgrabber >= 3.1.0-0
Requires: yum-metadata-parser >= 1.1.0
%if !0%{?os2_version}
Requires: pygpgme
%endif

Conflicts: rpm >= 5-0

Obsoletes: yum-skip-broken <= 1.1.18
Provides: yum-skip-broken = 1.1.18.yum
Obsoletes: yum-basearchonly <= 1.1.9
Obsoletes: yum-plugin-basearchonly <= 1.1.9
Provides: yum-basearchonly = 1.1.9.yum
Provides: yum-plugin-basearchonly = 1.1.9.yum
Obsoletes: yum-allow-downgrade < 1.1.20-0
Obsoletes: yum-plugin-allow-downgrade < 1.1.22-0
Provides: yum-allow-downgrade = 1.1.20-0.yum
Provides: yum-plugin-allow-downgrade = 1.1.22-0.yum
Obsoletes: yum-plugin-protect-packages < 1.1.27-0
Provides: yum-protect-packages = 1.1.27-0.yum
Provides: yum-plugin-protect-packages = 1.1.27-0.yum
Obsoletes: yum-plugin-download-order <= 0.2-2
%if !0%{?os2_version}
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
%endif

%if 0%{?os2_version}
# for exe wrapper
BuildRequires: gcc
%endif

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded
automatically, prompting the user for permission as necessary.

%debug_package

%if !0%{?os2_version}
%package updatesd
Summary: Update notification daemon
Group: Applications/System
Requires: yum = %{version}-%{release}
Requires: dbus-python
Requires: pygobject2
Requires(preun): /sbin/chkconfig
Requires(post): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(post): /sbin/service

%description updatesd
yum-updatesd provides a daemon which checks for available updates and 
can notify you when they are available via email, syslog or dbus. 
%endif


%if !0%{?os2_version}
%package cron
Summary: Files needed to run yum updates as a cron job
Group: System Environment/Base
Requires: yum >= 3.0 vixie-cron crontabs yum-plugin-downloadonly findutils
Requires(post): /sbin/chkconfig
Requires(post): /sbin/service
Requires(preun): /sbin/chkconfig
Requires(preun): /sbin/service
Requires(postun): /sbin/service

%description cron
These are the files needed to run yum updates as a cron job.
Install this package if you want auto yum updates nightly via cron.
%endif


%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif

%build
%if !0%{?os2_version}
%global make_vars
%else
# Redefine some makefile vars with correct values
%global make_vars %{shrink:
  PYTHON=%{__python}
  PYVER=%{python_version}
  PYSYSDIR=%{_prefix}
  ROOTPREFIX=%{_root_prefix}
  PREFIX=%{_prefix}
  SYSCONFDIR=%{_sysconfdir}
  LOCALSTATEDIR=%{_localstatedir}
}
%endif
make %{make_vars}

%if 0%{?os2_version}
# build exe wrapper
%{__cp} %SOURCE1 .
gcc -g -Zomf %optflags -DPYTHON_EXE=\"python%{python_version}.exe\" -o %{name}.exe exec-py.c
%endif

%install
rm -rf $RPM_BUILD_ROOT
make %{make_vars} DESTDIR=$RPM_BUILD_ROOT install
%if !0%{?os2_version}
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/yum.conf
%endif
%if !0%{?os2_version}
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d $RPM_BUILD_ROOT/%{yum_pluginslib}
mkdir -p $RPM_BUILD_ROOT/%{yum_pluginsshare}
%else
# TODO: plugin dirs are provided by yum-utils.spec now but should belong here
%endif

%if 0%{?os2_version}
# install exe wrapper
%{__install} -m 755 %{name}.exe $RPM_BUILD_ROOT/%{_bindir}
%endif

%if !0%{?os2_version}
# for now, move repodir/yum.conf back
mv $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d $RPM_BUILD_ROOT/%{_sysconfdir}/yum.repos.d
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum.conf
%endif

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

# rpmlint bogus stuff...
chmod +x $RPM_BUILD_ROOT/%{_datadir}/yum-cli/*.py
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/yum/*.py
chmod +x $RPM_BUILD_ROOT/%{python_sitelib}/rpmUtils/*.py

%if 0%{?os2_version}
# Remove cron stuff (we don't have cron)
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/cron.daily/0yum.cron
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/sysconfig/yum-cron
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/rc.d/init.d/yum-cron
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum-daily.yum
rm -f $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum-weekly.yum
# Convert LF -> CRLF in yum.conf to avoid a warning and yum.conf.rpmnew creation
# if file contents is otherwise the same (CRLF is a result of bug-report URL
# rewrite with sed in post scriplet below)
sed -i 's/$//' $RPM_BUILD_ROOT/%{_sysconfdir}/yum/yum.conf
%endif

%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT


%if 0%{?os2_version}
# Update the bug-report URL for existing installs (yum.conf is not replaced)
%post
sed -i -e \
     "s|http://trac.netlabs.org/rpm/|https://github.com/bitwiseworks/rpm-issues|g" \
     %{_sysconfdir}/yum/yum.conf

%posttrans
# Try to remove directories wrongly created inside /etc/yum by previous RPMs
rm -rf %{_sysconfdir}/yum/bash_completion.d 2>/dev/null || :
rm -rf %{_sysconfdir}/yum/rc.d 2>/dev/null || :
rm -rf %{_sysconfdir}/yum/sysconfig 2>/dev/null || :
%endif


%if !0%{?os2_version}
%post cron
# Make sure chkconfig knows about the service
/sbin/chkconfig --add yum-cron
# if an upgrade:
if [ "$1" -ge "1" ]; then
# if there's a /etc/rc.d/init.d/yum file left, assume that there was an
# older instance of yum-cron which used this naming convention.  Clean 
# it up, do a conditional restart
 if [ -f /etc/init.d/yum ]; then 
# was it on?
  /sbin/chkconfig yum
  RETVAL=$?
  if [ $RETVAL = 0 ]; then
# if it was, stop it, then turn on new yum-cron
   /sbin/service yum stop 1> /dev/null 2>&1
   /sbin/service yum-cron start 1> /dev/null 2>&1
   /sbin/chkconfig yum-cron on
  fi
# remove it from the service list
  /sbin/chkconfig --del yum
 fi
fi 
exit 0
 
%preun cron
# if this will be a complete removeal of yum-cron rather than an upgrade,
# remove the service from chkconfig control
if [ $1 = 0 ]; then
 /sbin/chkconfig --del yum-cron
 /sbin/service yum-cron stop 1> /dev/null 2>&1
fi
exit 0
 
%postun cron
# If there's a yum-cron package left after uninstalling one, do a
# conditional restart of the service
if [ "$1" -ge "1" ]; then
 /sbin/service yum-cron condrestart 1> /dev/null 2>&1
fi
exit 0
%endif



%files -f %{name}.lang
%defattr(-, root, root, -)
%doc README AUTHORS COPYING TODO INSTALL ChangeLog
%config(noreplace) %{_sysconfdir}/yum/yum.conf
%dir %{_sysconfdir}/yum
%config(noreplace) %{_sysconfdir}/yum/version-groups.conf
%dir %{_sysconfdir}/yum/protected.d
%dir %{_sysconfdir}/yum/repos.d
%dir %{_sysconfdir}/yum/vars
%config(noreplace) %{_sysconfdir}/logrotate.d/yum
%{_sysconfdir}/bash_completion.d
%dir %{_datadir}/yum-cli
%{_datadir}/yum-cli/*
%{_bindir}/yum
%if 0%{?os2_version}
%{_bindir}/yum.exe
%endif
%{python_sitelib}/yum
%{python_sitelib}/rpmUtils
%dir %{_var}/cache/yum
%dir %{_var}/lib/yum
%ghost %{_var}/lib/yum/uuid
%ghost %{_var}/lib/yum/history
%ghost %{_var}/lib/yum/plugins
%ghost %{_var}/lib/yum/yumdb
%{_mandir}/man*/yum.*
%{_mandir}/man*/yum-shell*
# plugin stuff
%if !0%{?os2_version}
%dir {_sysconfdir}/yum/pluginconf.d
%dir %{yum_pluginslib}
%dir %{yum_pluginsshare}
%else
# TODO: plugin dirs are provided by yum-utils.spec now but should belong here
%endif

%if !0%{?os2_version}
%files cron
%defattr(-,root,root)
%doc COPYING
%{_sysconfdir}/cron.daily/0yum.cron
%config(noreplace) %{_sysconfdir}/yum/yum-daily.yum
%config(noreplace) %{_sysconfdir}/yum/yum-weekly.yum
%{_sysconfdir}/rc.d/init.d/yum-cron
%config(noreplace) %{_sysconfdir}/sysconfig/yum-cron
%endif

%changelog
* Wed Sep 16 2026 Dmitrii Kuminov <coding@dmik.org> 3.4.3-15
- Build from v3.4.3-os2-1 tag
- Synchronize with Fedora spec (commit 45dfa35)
- Remove cron files (not used yet)

* Fri Feb 18 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.4.3-14
- change yum.conf to new rpm issue location in post section
- moved source to github

* Mon Jun 07 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.4.3-13
- use github as rpm issue location instead of netlabs

* Tue May 25 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.4.3-12
- Remove python-sqlite requires

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
