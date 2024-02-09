Summary: An encoder/decoder for the Free Lossless Audio Codec
Name: flac
Version: 1.3.4
Release: 1%{?dist}
License: BSD and GPLv2+ and GFDL
%if !0%{?os2_version}
Source0: https://downloads.xiph.org/releases/flac/flac-%{version}.tar.xz
%else 
%scm_source github https://github.com/xiph/flac master
%endif
URL: https://www.xiph.org/flac/
Requires: %{name}-libs%{?_isa} = %{version}-%{release}
BuildRequires: libogg-devel
BuildRequires: gcc gcc-c++ automake autoconf libtool gettext-devel doxygen
%ifarch %{ix86}
# 2.0 supports symbol visibility
BuildRequires: nasm >= 2.0
%endif
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

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif

%build
# use our libtool to avoid problems with RPATH
./autogen.sh -V

# -funroll-loops makes encoding about 10% faster
export LDFLAGS="-Zomf -Zmap -Zhigh-mem -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export CFLAGS="%{optflags} -funroll-loops"
%configure \
    --htmldir=%{_docdir}/flac/html \
    --disable-xmms-plugin \
    --disable-silent-rules \
    --disable-thorough-tests
%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install

# split documentation
mv %{buildroot}%{_docdir}/flac* ./flac-doc
mkdir -p flac-doc-devel
%if !0%{?os2_version}
mv flac-doc{/html/api,-devel}
%else
mv flac-doc/html/api/* flac-doc-devel
%endif
rm flac-doc/FLAC.tag


rm %{buildroot}%{_libdir}/*.la

%check
%if !0%{?os2_version}
make check

%ldconfig_scriptlets libs
%endif

%files
%doc flac-doc/*
%if !0%{?os2_version}
%{_bindir}/flac
%{_bindir}/metaflac
%else
%{_bindir}/flac.exe
%{_bindir}/metaflac.exe
%{_mandir}/man1/*
%endif

%files libs
%doc AUTHORS COPYING* README
%if !0%{?os2_version}
%{_libdir}/libFLAC.so.8*
%{_libdir}/libFLAC++.so.6*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc flac-doc-devel/*
%{_includedir}/*
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*.a
%endif
%{_libdir}/pkgconfig/*
%{_datadir}/aclocal/*.m4

%changelog
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
