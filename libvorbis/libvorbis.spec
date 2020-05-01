%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary:	The Vorbis General Audio Compression Codec
Name:		libvorbis
Version:	1.3.6
Release:	4%{?dist}
Epoch:		1
License:	BSD
URL:		https://www.xiph.org/
%scm_source github https://github.com/bitwiseworks/vorbis-os2 %{version}-os2
Vendor:		bww bitwise works GmbH
BuildRequires:  gcc
BuildRequires:	pkgconfig(ogg) >= 1.0

# sync with git as of
#
# commit 46e70fa6573e206c2555cd99a53204ffd6bf58fd
# Author: Minmin Gong <gongminmin@msn.com>
# Date:   Wed Jul 4 21:37:54 2018 -0700
#
#     Fix the compiling errors on msvc ARM64 configuration.
#
# Fixes:
# CVE-2017-14160
# CVE-2018-10392
# CVE-2018-10393
#Patch0: libvorbis-1.3.6-git.patch

%description
Ogg Vorbis is a fully open, non-proprietary, patent- and royalty-free,
general-purpose compressed audio format for audio and music at fixed
and variable bitrates.

The libvorbis package contains runtime libraries for use in programs
that support Ogg Vorbis.

%package devel
Summary: Development tools for Vorbis applications
Requires:	%{name}%{?_isa} = %{epoch}:%{version}-%{release}

%description devel
The libvorbis-devel package contains the header files and documentation
needed to develop applications with Ogg Vorbis.

%package devel-docs
Summary: Documentation for developing Vorbis applications
Requires: %{name}-devel = %{epoch}:%{version}-%{release}
BuildArch: noarch

%description devel-docs
Documentation for developing applications with libvorbis.

%debug_package

%prep
%scm_setup
autoreconf -fiv

sed -i "s|-O20|$RPM_OPT_FLAGS|" configure
sed -i "s/-ffast-math//" configure
sed -i "s/-mcpu=750//" configure

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%configure --disable-static

# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"

make %{?_smp_mflags}

%install
%make_install docdir=%{_pkgdocdir}
# remove unpackaged files from the buildroot
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/lib/.libs
make check

%files
%doc AUTHORS
%license COPYING
%{_libdir}/vorbis*.dll

%files devel
%{_includedir}/vorbis
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/*.pc
%{_datadir}/aclocal/vorbis.m4

%files devel-docs
%{_pkgdocdir}/*
%exclude %{_pkgdocdir}/AUTHORS
%exclude %{_pkgdocdir}/doxygen-build.stamp

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%changelog
* Fri May 01 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.3.6-4
- moved the source to github.com/bitwiseworks
- added a debug package
- added a buildlevel to the dll

* Mon Mar 04 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3.6-3
- Put dll in right section
- Put back some deleted lines

* Sun Mar 03 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3.6-2
- Cleanup some lines

* Sun Mar 03 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3.6-1
- First Rpm build for OS2
- Change some .spec lines

* Tue Mar 15 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.3.5-1
- Initial OS/2 packaging
