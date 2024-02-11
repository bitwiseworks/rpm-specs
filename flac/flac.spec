Summary: An encoder/decoder for the Free Lossless Audio Codec
Name: flac
Version: 1.4.3
Release: 2%{?dist}
License: BSD-3-Clause AND GPL-2.0-or-later AND GFDL-1.1-or-later
%if 0%{os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{os2_version}
Source0: https://downloads.xiph.org/releases/flac/flac-%{version}.tar.xz
URL: https://www.xiph.org/flac/
%else
%scm_source github https://github.com/tellie/%{name}-os2 %{version}-os2
%endif

%if !0%{?os2_version}
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
%else
Requires: %{name}-libs = %{version}-%{release}
%endif

BuildRequires: libogg-devel
BuildRequires: gcc gcc-c++ automake autoconf libtool gettext-devel doxygen
BuildRequires: make

%description
FLAC stands for Free Lossless Audio Codec. Grossly oversimplified, FLAC
is similar to Ogg Vorbis, but lossless. The FLAC project consists of
the stream format, reference encoders and decoders in library form,
flac, a command-line program to encode and decode FLAC files, metaflac,
a command-line metadata editor for FLAC files and input plugins for
various music players.

This package contains the command-line tools and documentation.

%package libs
Summary: Libraries for the Free Lossless Audio Codec
Obsoletes: flac < 1.2.1-11
# xmms-flac dropped in 1.3.3-8
Obsoletes: xmms-flac < 1.3.3-8

%description libs
FLAC stands for Free Lossless Audio Codec. Grossly oversimplified, FLAC
is similar to Ogg Vorbis, but lossless. The FLAC project consists of
the stream format, reference encoders and decoders in library form,
flac, a command-line program to encode and decode FLAC files, metaflac,
a command-line metadata editor for FLAC files and input plugins for
various music players.
This package contains the FLAC libraries.

%package devel
Summary: Development libraries and header files from FLAC
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
Requires: pkgconfig

%description devel
This package contains all the files needed to develop applications that
will use the Free Lossless Audio Codec.

%if 0%{?os2_version}
%legacy_runtime_packages
%endif

%prep
%if !0%{os2_version}
%setup -q
%else
%scm_setup
%endif

%build
# use our libtool to avoid problems with RPATH
./autogen.sh -V

%if 0%{?os2_version}
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif

%configure \
    --htmldir=%{_docdir}/flac/html \
    --disable-silent-rules \
    --disable-thorough-tests

%make_build

%install
%make_install

rm -r %{buildroot}%{_docdir}/flac
rm %{buildroot}%{_libdir}/*.la

%check

%if !0%{?os2_version}
make check
%endif

%if !0%{os2_version}
%ldconfig_scriptlets libs
%endif

%files
%if !0%{?os2_version}
%{_bindir}/flac
%{_bindir}/metaflac
%else
%{_bindir}/flac.exe
%{_bindir}/metaflac.exe
%endif
%{_mandir}/man1/*

%files libs
%doc AUTHORS README.md CHANGELOG.md
%license COPYING.*
%if !0%{os2_version}
%{_libdir}/libFLAC.so.12*
%{_libdir}/libFLAC++.so.10*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc doc/api
%{_includedir}/*
%if !0%{os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*.m4

%changelog
* Sat Feb 10 2024 Elbert Pol <elbert.pol@gmail.com> 1.4.3-2
- Provide legacy packages with DLLs for old ABI.

* Fri Feb 09 2024 Elbert Pol <elbert.pol@gmail.com> 1.4.3-1
- Updated to latest version
- Make a bldlevel for dlls
- syncronized the spec with lated fedora spec

* Fri Mar 11 2022 Elbert Pol <elbert.pol@gmail.com> 1.3.4-1
- update to latest version

* Wed Oct 09 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3.3-1
- Update to latest source
- Clean up spec file

* Mon Mar 04 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3.2-2
- Change the dll place to only libs section
- Add debug to specfile

* Sun Mar 03 2019 Elbert Pol <elbert.pol@gmail.com> - 1.3.2-1
- First RPM built for OS2
