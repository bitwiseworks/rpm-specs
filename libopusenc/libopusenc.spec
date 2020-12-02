Name:     libopusenc
Version:  0.2.1
Release:  2%{?dist}
Summary:  A library that provides an easy way to encode Ogg Opus files
License:  BSD
URL:      https://opus-codec.org/
%if !0%{?os2_version}
Source0:  https://archive.mozilla.org/pub/opus/%{name}-%{version}.tar.gz
%else
Vendor:   bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

BuildRequires: gcc
BuildRequires: doxygen
BuildRequires: opus-devel

%description
A library that provides an easy way to encode Ogg Opus files.

%package  devel
Summary:  Development package for libopusenc
Requires: opus-devel
Requires: %{name} = %{version}-%{release}

%description devel
Files for development with libopusenc.

%debug_package

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
echo PACKAGE_VERSION="%{version}" > package_version
autoreconf -fvi
%endif

%build
%if 0%{?os2_version}
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lmmpm2"
export CFLAGS="-idirafter /@unixroot/usr/include/os2tk45"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure --disable-static

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install

# Remove libtool archives
find %{buildroot} -type f -name "*.la" -delete
rm -rf %{buildroot}%{_datadir}/doc/libopusenc/

%check
make check %{?_smp_mflags} V=1

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING
%if !0%{?os2_version}
%{_libdir}/libopusenc.so.*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc doc/html
%{_includedir}/opus/opusenc.h
%if !0%{?os2_version}
%{_libdir}/libopusenc.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/libopusenc.pc

%changelog
* Tue Dec 01 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.2.1-2
- fix spec file a bit
- add a nice buildlevel to the dll

* Thu Oct 01 2020 Elbert Pol <elbert.pol@gmail.com> - 0.2.1-1
- First rpm build for OS2
