Name:    libassuan
Summary: GnuPG IPC library
Version: 2.5.3
Release: 1%{?dist}

# The library is LGPLv2+, the documentation GPLv3+
License: LGPLv2+ and GPLv3+
%if !0%{?os2_version}
Source0: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2
Source1: https://gnupg.org/ftp/gcrypt/libassuan/libassuan-%{version}.tar.bz2.sig
%endif
URL:     http://www.gnupg.org/

%if !0%{?os2_version}
Patch1:  libassuan-2.5.2-multilib.patch
Patch2:  libassuan-2.5.3-includedir.patch
%else
Vendor:  bww bitwise works GmbH
%scm_source    github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2
%endif

BuildRequires: gcc
BuildRequires: gawk
BuildRequires: libgpg-error-devel >= 1.8

%description
This is the IPC library used by GnuPG 2, GPGME and a few other
packages.

%package devel 
Summary: GnuPG IPC library 
Provides: libassuan2-devel = %{version}-%{release}
Provides: libassuan2-devel = %{version}-%{release}
Requires: %{name} = %{version}-%{release}
Requires: pkgconfig
%description devel 
This is the IPC static library used by GnuPG 2, GPGME and a few other
packages.

This package contains files needed to develop applications using %{name}.

%debug_package

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif

%if !0%{?os2_version}
%patch1 -p1 -b .multilib
%patch2 -p1 -b .includedir
%else
autoreconf -fvi
%endif


%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure \
  --includedir=%{_includedir}/libassuan2

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif


%install
%make_install

## Unpackaged files
rm -fv %{buildroot}%{_infodir}/dir
rm -fv %{buildroot}%{_libdir}/lib*.la


%check
%if 0%{?os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/src/.libs
%endif
make check


%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING COPYING.LIB
%doc AUTHORS NEWS README
%if !0%{?os2_version}
%{_libdir}/libassuan.so.0*
%else
%{_libdir}/assuan*.dll
%endif

%files devel 
%{_bindir}/libassuan-config
%{_includedir}/libassuan2/
%if !0%{?os2_version}
%{_libdir}/libassuan.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/libassuan.pc
%{_datadir}/aclocal/libassuan.m4
%{_infodir}/assuan.info*


%changelog
* Mon Oct 26 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.5.3-1
- first OS/2 rpm
