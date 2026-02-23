%define majorver 8.6
%define	vers %{majorver}.15
%if !0%{?os2_version}
%{!?sdt:%define sdt 1}
%else
%{!?sdt:%define sdt 0}
%define _without_check 1
%define major 8
%define minor 6
%endif

Summary: Tool Command Language, pronounced tickle
Name: tcl
Version: %{vers}
Release: 1%{?dist}
Epoch: 1
License: TCL AND GPL-3.0-or-later WITH bison-exception-2.2 AND BSD-3-Clause
URL: http://tcl.sourceforge.net/
%if !0%{?os2_version}
Source0: http://downloads.sourceforge.net/sourceforge/tcl/tcl-core%{version}-src.tar.gz
%else
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif
BuildRequires: make
Buildrequires: autoconf
BuildRequires:  gcc
BuildRequires: zlib-devel
Provides: tcl(abi) = %{majorver}
Obsoletes: tcl-tcldict <= %{vers}
Provides: tcl-tcldict = %{vers}
%if !0%{?os2_version}
Patch0: tcl-8.6.15-autopath.patch
Patch1: tcl-8.6.15-conf.patch
Patch3: tcl-8.6.13-tcltests-path-fix.patch
Patch4: tcl-8.6.13-configure-c99.patch
%endif

%if %sdt
BuildRequires: systemtap-sdt-devel
%endif

%description
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

%package doc
Summary: Tcl documentation
Requires: %{name} = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description doc
TCL documentation.

%package devel
Summary: Tcl scripting language development environment
Requires: %{name} = %{epoch}:%{version}-%{release}

%description devel
The Tcl (Tool Command Language) provides a powerful platform for
creating integration applications that tie together diverse
applications, protocols, devices, and frameworks. When paired with the
Tk toolkit, Tcl provides a fastest and powerful way to create
cross-platform GUI applications.  Tcl can also be used for a variety
of web-related tasks and for creating powerful command languages for
applications.

The package contains the development files and man pages for tcl.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1 -n %{name}%{version}
%else
%scm_setup
%endif
rm -r compat/zlib

%build
%if !0%{?os2_version}
pushd unix
autoconf
%else
cd unix
autoreconf -fvi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%endif
%configure \
%if %sdt
--enable-dtrace \
%endif
--enable-threads \
--enable-symbols \
%if !0%{?os2_version}
--enable-shared
%else
--disable-shared \
--enable-man-symlinks
%endif

%make_build CFLAGS="%{optflags}" TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

%check
%{?_without_check: %define _without_check 1}
%{!?_without_check: %define _without_check 0}

%if ! %{_without_check}
  cd unix
  make test
%endif

%install
make install -C unix INSTALL_ROOT=%{buildroot} TCL_LIBRARY=%{_datadir}/%{name}%{majorver}

%if !0%{?os2_version}
ln -s tclsh%{majorver} %{buildroot}%{_bindir}/tclsh
%else
cp %{buildroot}%{_bindir}/tclsh%{majorver}.exe %{buildroot}%{_bindir}/tclsh.exe
cp unix/tcl*.dll %{buildroot}%{_libdir}
cp unix/libtcl%{majorver}_dll.a %{buildroot}%{_libdir}
rm -f %{buildroot}%{_libdir}/lib%{name}%{majorver}.a 
%endif

%if !0%{?os2_version}
# for linking with -lib%%{name}
ln -s lib%{name}%{majorver}.so %{buildroot}%{_libdir}/lib%{name}.so
%endif

mkdir -p %{buildroot}/%{_libdir}/%{name}%{majorver}

# postgresql and maybe other packages too need tclConfig.sh
# paths don't look at /usr/lib for efficiency, so we symlink into tcl8.6 for now
ln -s %{_libdir}/%{name}Config.sh %{buildroot}/%{_libdir}/%{name}%{majorver}/%{name}Config.sh

%if !0%{?os2_version}
mkdir -p %{buildroot}/%{_includedir}/%{name}-private/{generic,unix}
find generic unix -name "*.h" -exec cp -p '{}' %{buildroot}/%{_includedir}/%{name}-private/'{}' ';'
( cd %{buildroot}/%{_includedir}
	for i in *.h ; do
		[ -f %{buildroot}/%{_includedir}/%{name}-private/generic/$i ] && ln -sf ../../$i %{buildroot}/%{_includedir}/%{name}-private/generic ;
	done
)
%endif

# remove buildroot traces
sed -i -e "s|$PWD/unix|%{_libdir}|; s|$PWD|%{_includedir}/%{name}-private|" %{buildroot}/%{_libdir}/%{name}Config.sh
rm -rf %{buildroot}/%{_datadir}/%{name}%{majorver}/ldAix

%if 0%{?flatpak}
mkdir -p %{buildroot}%{_usr}/bin
ln -s %{_bindir}/tclsh %{_bindir}/tclsh%{majorver} %{buildroot}%{_usr}/bin/
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%{_bindir}/tclsh*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%endif
%{_datadir}/%{name}%{majorver}
%exclude %{_datadir}/%{name}%{majorver}/tclAppInit.c
%{_datadir}/%{name}8
%if !0%{?os2_version}
%{_libdir}/lib%{name}%{majorver}.so
%else
%{_libdir}/%{name}%{major}%{minor}.dll
%endif
%{_mandir}/man1/*
%if 0%{?flatpak}
%{_usr}/bin/tclsh*
%endif
%dir %{_libdir}/%{name}%{majorver}
%doc README.md changes
%doc license.terms

%files doc
%{_mandir}/man3/*
%{_mandir}/mann/*

%files devel
%{_includedir}/*
%{_libdir}/lib%{name}stub%{majorver}.a
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so
%else
%{_libdir}/lib%{name}%{majorver}_dll.a
%endif
%{_libdir}/%{name}Config.sh
%{_libdir}/%{name}ooConfig.sh
%{_libdir}/%{name}%{majorver}/%{name}Config.sh
%{_libdir}/pkgconfig/tcl.pc
%{_datadir}/%{name}%{majorver}/tclAppInit.c

%changelog
* Fri Feb 20 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 8.6.15-1
- update to vendor version 8.6.15
- reworked the spec according to fedora spec

* Fri Mar 22 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 8.5.9-4
- reworked fd handling in the mkstemp() case, to make it work
- create a nice bldlevel
- rebuild with latest scm_macros
- remove the dll from the devel rpm
- add debug package

* Tue Jun 14 2016 yd <yd@os2power.com> 8.5.9-3
- rebuild package, fixes ticket#183.
