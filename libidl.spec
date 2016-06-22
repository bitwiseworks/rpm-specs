#
# spec file for package libidl
#
# Copyright (c) 2013 SUSE LINUX Products GmbH, Nuernberg, Germany.
#
# All modifications and additions to the file contributed by third parties
# remain the property of their copyright owners, unless otherwise agreed
# upon. The license for this file, and modifications and additions to the
# file, is the same license as for the pristine package itself (unless the
# license for the pristine package is not an Open Source License, in which
# case the license is the MIT License). An "Open Source License" is a
# license that conforms to the Open Source Definition (Version 1.9)
# published by the Open Source Initiative.

# Please submit bugfixes or comments via http://bugs.opensuse.org/
#

#%define svn_url     n:/src/ports/libidl
%define svn_url     http://svn.netlabs.org/repos/ports/libidl/trunk
%define svn_rev     1330

Name:           libidl
%define         _name libIDL
Url:            http://www.gnome.org
Version:        0.8.14
Release:        6%{?dist}
#Release:        42.20
# NOTE: on upgrade to a new upstream version, change the Obsoletes from <= to < (here and in baselibs.conf)
Summary:        IDL Parsing Library
License:        LGPL-2.1+
Group:          System/Libraries
Vendor:         bww bitwise works GmbH

Source:         %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Provides:       %{name} = %{version}
# Note: we keep <= (and a rpmlint warning...) until we get a version higher than 0.8.14 (when this provides/obsoletes was introduced)
Obsoletes:      %{name} <= %{version}
# bug437293
#%ifarch ppc64
#Obsoletes:      libidl-64bit
#%endif
#
Requires:       glib2 libgcc1
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  glib2-devel
BuildRequires:  pkgconfig

%description
LibIDL is a small library for creating parse trees of CORBA
v2.2-compliant Interface Definition Language (IDL) files. IDL is a
specification for defining interfaces that can be used between
different CORBA implementations.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Languages/Other
Requires:       %{name} = %{version}-%{release}
#PreReq:         %install_info_prereq
# bug437293
#%ifarch ppc64
#Obsoletes:      libidl-devel-64bit
#%endif
#

%description devel
LibIDL is a small library for creating parse trees of CORBA v2.2
compliant Interface Definition Language (IDL) files, which is a
specification for defining interfaces which can be used between
different CORBA implementations.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -q -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
export \
        LDFLAGS="-Zhigh-mem" CFLAGS="-D__OS2__ -D__EMX__" RANLIB=echo

autoreconf -fiv

%configure \
        --enable-shared \
        --enable-static

# Work around ASH bug: change RANLIB="echo\n" to RANLIB="echo" in libtool
sed -e ':a;N;$!ba;s/RANLIB\=\"echo\n/RANLIB="echo/g' \
	<%{_builddir}/%{?buildsubdir}/libtool \
	>%{_builddir}/%{?buildsubdir}/libtool2
rm -rf %{_builddir}/%{?buildsubdir}/libtool
mv -f %{_builddir}/%{?buildsubdir}/libtool2 %{_builddir}/%{?buildsubdir}/libtool

%{__make} %{?jobs:-j%jobs}

%install
%makeinstall
find %{buildroot} -type f -name "*.la" -exec %{__rm} -fv {} +
mkdir -p $RPM_BUILD_ROOT%{_datadir}
# mkdir $RPM_BUILD_ROOT%{_datadir}/idl
rm -f %{buildroot}%{_datadir}/info/dir
# rm -f %{buildroot}%{_libdir}/*.lib
emxomf -o %{buildroot}%{_libdir}/IDL-2.lib %{buildroot}%{_libdir}/IDL-2.a
emximp -o %{buildroot}%{_libdir}/IDL-2_dll.lib %{buildroot}%{_libdir}/idl20.dll
emximp -o %{buildroot}%{_libdir}/IDL-20_dll.lib %{buildroot}%{_libdir}/idl20.dll
# change shell path in libIDL-config-2
sed -e 's-\#\! \/bin\/sh-#! /@unixroot/usr/bin/sh-g' \
	<%{buildroot}%{_bindir}/libIDL-config-2 \
	>%{buildroot}%{_bindir}/libIDL-config-1
rm -rf %{buildroot}%{_bindir}/libIDL-config-2
mv -f %{buildroot}%{_bindir}/libIDL-config-1 %{buildroot}%{_bindir}/libIDL-config-2
chmod 755 %{buildroot}%{_bindir}/libIDL-config-2

%clean
rm -rf $RPM_BUILD_ROOT

# %post -n libIDL-2-0 -p /sbin/ldconfig

# %postun -n libIDL-2-0 -p /sbin/ldconfig

%post devel
### @todo Replace with ``%%info_post %%{_name}2.info`` when its available.
if [ -f %{_infodir}/%{_name}2.info ]; then
    %{_sbindir}/install-info.exe %{_infodir}/%{_name}2.info %{_infodir}/dir
fi

%postun devel
### @todo Replace with ``%%info_postun %%{_name}2.info`` when its available.
if [ $1 -eq 0 ]; then
    if [ -f %{_infodir}/%{_name}2.info ]; then
        %{_sbindir}/install-info.exe --delete %{_infodir}/%{_name}2.info %{_infodir}/dir
    fi
fi

%files
%defattr(-,root,root)
%doc COPYING ChangeLog AUTHORS README* NEWS BUGS tstidl.c
%{_libdir}/idl*.dll
# generic directory for idl files
# %dir %{_datadir}/idl

%files devel
%defattr(-,root,root)
%{_bindir}/%{_name}-config-2
%{_includedir}/*
%doc %{_infodir}/%{_name}2.info
%{_libdir}/pkgconfig/*.pc
%{_libdir}/IDL-2.a
%{_libdir}/IDL-2_dll.a
%{_libdir}/IDL-20_dll.a
%{_libdir}/IDL-2.lib
%{_libdir}/IDL-2_dll.lib
%{_libdir}/IDL-20_dll.lib

%changelog
* Wed Jun 22 2016 yd <yd@os2power.com> 0.8.14-6
- use correct svn revision for building.

* Sat Jun 18 2016 yd <yd@os2power.com> 0.8.14-5
- rebuild for glib2 2.33.

* Thu Mar 10 2016 Valery Sedletski <_valerius@mail.ru> - 0.8.14-4
- fixed permissions for libIDL-config-2 to be 755
- fixed Requires directive for 'devel' package to depend on %{name} = %{version}-%{release}

* Mon Feb 29 2016 Valery Sedletski <_valerius@mail.ru> - 0.8.14-3
- Added needed Requires and BuildRequires directives

* Thu Feb 18 2016 Valery Sedletski - <_valerius@mail.ru> 0.8.14-2
- changed libs format to both a.out and OMF
- added debug package
- added OS/2 DLL shortname

* Thu Dec 03 2015 Valery Sedletski - <_valerius@mail.ru> Initial OS/2 build
- Initial OS/2 port
