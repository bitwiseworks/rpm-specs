%{!?python_sitelib: %define python_sitelib %(python -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
 
Summary: RPM installer/updater
Name: yum
Version: 3.2.27
Release: 1
License: GPLv2+
Group: System Environment/Base
Source0: http://yum.baseurl.org/download/3.2/%{name}-%{version}.tar.gz
#Source1: yum.conf.fedora
#Source2: yum-updatesd.conf.fedora

Patch0: yum-3.2.27-os2.diff

URL: http://yum.baseurl.org/

BuildArch: noarch
BuildRequires: python
#BuildRequires: gettext
#BuildRequires: intltool

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
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: python
Requires: python(abi) = 2.6

%description
Yum is a utility that can check for and automatically download and
install updated RPM packages. Dependencies are obtained and downloaded 
automatically, prompting the user for permission as necessary.

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

%prep
%setup -q
%patch0 -p1

%build
export MAKESHELL="/bin/sh"
make

%install
rm -rf $RPM_BUILD_ROOT
export MAKESHELL="/bin/sh"
make DESTDIR=$RPM_BUILD_ROOT install
#install -m 644 %{SOURCE1} $RPM_BUILD_ROOT/%{_sysconfdir}/yum.conf
#mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/pluginconf.d $RPM_BUILD_ROOT/usr/lib/yum-plugins

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

#%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%files
# -f %{name}.lang
%defattr(-, root, root, -)
%doc README AUTHORS COPYING TODO INSTALL ChangeLog
%config(noreplace) %{_sysconfdir}/yum/yum.conf
%dir %{_sysconfdir}/yum
%config(noreplace) %{_sysconfdir}/yum/version-groups.conf
#%dir %{_sysconfdir}/yum/protected.d
%dir %{_sysconfdir}/yum/repos.d
#%dir %{_sysconfdir}/yum/vars
%config(noreplace) %{_sysconfdir}/logrotate.d/yum
%{_sysconfdir}/bash_completion.d
%dir %{_datadir}/yum-cli
%{_datadir}/yum-cli/*
%{_bindir}/yum
#%{python_sitelib}/yum
#%{python_sitelib}/rpmUtils
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
#%dir %{_sysconfdir}/yum/pluginconf.d 
#%dir /usr/lib/yum-plugins
%{_usr}/share/locale/ca/LC_MESSAGES/yum.mo
%{_usr}/share/locale/cs/LC_MESSAGES/yum.mo
%{_usr}/share/locale/da/LC_MESSAGES/yum.mo
%{_usr}/share/locale/de/LC_MESSAGES/yum.mo
%{_usr}/share/locale/es/LC_MESSAGES/yum.mo
%{_usr}/share/locale/fi/LC_MESSAGES/yum.mo
%{_usr}/share/locale/fr/LC_MESSAGES/yum.mo
%{_usr}/share/locale/it/LC_MESSAGES/yum.mo
%{_usr}/share/locale/ja/LC_MESSAGES/yum.mo
%{_usr}/share/locale/ms/LC_MESSAGES/yum.mo
%{_usr}/share/locale/nb/LC_MESSAGES/yum.mo
%{_usr}/share/locale/pa/LC_MESSAGES/yum.mo
%{_usr}/share/locale/pl/LC_MESSAGES/yum.mo
%{_usr}/share/locale/pt/LC_MESSAGES/yum.mo
%{_usr}/share/locale/pt_BR/LC_MESSAGES/yum.mo
%{_usr}/share/locale/ru/LC_MESSAGES/yum.mo
%{_usr}/share/locale/sr/LC_MESSAGES/yum.mo
%{_usr}/share/locale/sr@latin/LC_MESSAGES/yum.mo
%{_usr}/share/locale/sv/LC_MESSAGES/yum.mo
%{_usr}/share/locale/zh_CN/LC_MESSAGES/yum.mo

%changelog
