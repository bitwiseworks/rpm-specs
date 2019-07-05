# debuginfo not needed
%define debug_package %{nil}

Name: intltool
Summary: Utility for internationalizing various kinds of data files
Version: 0.41.1
Release: 3%{?dist}
License: GPLv2 with exceptions
Group: Development/Tools
Source: http://edge.launchpad.net/intltool/trunk/0.41.0/+download/intltool-%{version}.tar.gz
URL: http://www.gnome.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
Requires: patch
# for /usr/share/aclocal
#Requires: automake
Requires: gettext-devel
Obsoletes: xml-i18n-tools
Provides: xml-i18n-tools = 0.11
#Requires: perl(XML::Parser)
#BuildRequires: perl(XML::Parser)
BuildRequires: gettext

Patch1: 	intltool-os2.diff

%description
This tool automatically extracts translatable strings from oaf, glade,
bonobo ui, nautilus theme, .desktop, and other data files and puts
them in the po files.

%prep
%setup -q
%patch001 -p1 -b .os2~

%build
export CONFIG_SHELL="/bin/sh" ; \
%configure \
        "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc AUTHORS COPYING README
%{_bindir}/*
%{_datadir}/intltool
%{_datadir}/aclocal/*
%{_mandir}/man*/*

%changelog
