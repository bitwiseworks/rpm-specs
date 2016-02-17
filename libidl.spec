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
%define svn_rev     1205

Name:           libidl
%define         _name libIDL
Url:            http://www.gnome.org
Version:        0.8.14
Release:        1%{?dist}
#Release:        42.20
# NOTE: on upgrade to a new upstream version, change the Obsoletes from <= to < (here and in baselibs.conf)
Summary:        IDL Parsing Library
Vendor:         Andrew T. Veliath <andrewtv@usa.net>
License:        LGPL-2.1+
Group:          System/Libraries
Provides:       %{name} = %{version}
# Note: we keep <= (and a rpmlint warning...) until we get a version higher than 0.8.14 (when this provides/obsoletes was introduced)
Obsoletes:      %{name} <= %{version}
# bug437293
#%ifarch ppc64
#Obsoletes:      libidl-64bit
#%endif
#
Source:         %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
#Source:         http://ftp.gnome.org/pub/GNOME/sources/%{_name}/0.8/%{_name}-%{version}.tar.bz2
#Source99:       baselibs.conf
BuildRequires:  bison
BuildRequires:  flex
BuildRequires:  glib2-devel
BuildRequires:  urpo-devel
BuildRequires:  pkgconfig
BuildRoot:      %{_tmppath}/%{name}-%{version}-build

%description
LibIDL is a small library for creating parse trees of CORBA
v2.2-compliant Interface Definition Language (IDL) files. IDL is a
specification for defining interfaces that can be used between
different CORBA implementations.

%package devel
Summary:        Include Files and Libraries mandatory for Development
Group:          Development/Languages/Other
Requires:       libidl = %{version}
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

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -q -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

autoreconf -fi

%build
export \
	PATH=`echo $PATH | tr '\\\' '/'` \
	EXEEXT=".exe" IMPLIBPREF="" IMPLIBSUFF="_dll.lib" \
	LDFLAGS="-Zomf -Zhigh-mem -lurpo -lmmap -lpthread -lintl" CFLAGS="-Zomf -D__OS2__ -D__EMX__" \
	PATH_SEPARATOR=";" PATHSEP=";" AWK=gawk SED=sed GREP=grep \
	LD=gcc AR=emxomfar STRIP=strip RANLIB=echo \
	ECHO=echo PKG_CONFIG=pkg-config CC=gcc \
	LEX=flex YACC="bison -y" HAVE_YACC=yes \
	EMXOMFLD_TYPE="wlink" EMXOMFLD_LINKER="wl.exe"

%configure \
	--prefix=%{_prefix} \
	--enable-shared \
	--enable-static

# --with-pic

%{__make} %{?jobs:-j%jobs}

%install
%makeinstall
find %{buildroot} -type f -name "*.la" -exec %{__rm} -fv {} +
mkdir -p $RPM_BUILD_ROOT%{_datadir}
# mkdir $RPM_BUILD_ROOT%{_datadir}/idl
rm -f %{buildroot}%{_datadir}/info/dir
# rm -f %{buildroot}%{_libdir}/*.lib
# emxomf -o %{buildroot}%{_libdir}/IDL-2.lib %{buildroot}%{_libdir}/IDL-2.a
# emximp -o %{buildroot}%{_libdir}/IDL-2_dll.lib %{buildroot}%{_libdir}/IDL-20.dll
# emximp -o %{buildroot}%{_libdir}/IDL-20_dll.lib %{buildroot}%{_libdir}/IDL-20.dll

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
%{_libdir}/idl*.dbg
%{_libdir}/IDL-2.lib
%{_libdir}/IDL-2_dll.lib
%{_libdir}/IDL-20_dll.lib

%changelog
* Thu Dec 03 2015 Valery Sedletski - <_valerius@mail.ru> Initial OS/2 build
- Initial OS/2 port
