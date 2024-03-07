Summary:	A voice compression format (codec)
Name:		speex
Version:	1.2.0
Release:	1%{?dist}
License:	BSD
Group:		System Environment/Libraries
URL:		https://www.speex.org/
%if !0%{?os2_version}
Source0:	https://downloads.xiph.org/releases/speex/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif
BuildRequires:	gcc
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(speexdsp)

%description
Speex is a patent-free compression format designed especially for
speech. It is specialized for voice communications at low bit-rates in
the 2-45 kbps range. Possible applications include Voice over IP
(VoIP), Internet audio streaming, audio books, and archiving of speech
data (e.g. voice mail).

%package devel
Summary: 	Development package for %{name}
Group: 		Development/Libraries
Requires: 	%{name}%{?_isa} = %{version}-%{release}

%description devel
Speex is a patent-free compression format designed especially for
speech. This package contains development files for %{name}

%package tools
Summary:	The tools package for %{name}
Group:		Applications/Multimedia
Requires:	%{name}%{?_isa} = %{version}-%{release}

%description tools
Speex is a patent-free compression format designed especially for
speech. This package contains tools files and user's manual for %{name}.

%debug_package

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
%endif

%build
autoreconf -vfi
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lmmpm2"
export CFLAGS="-idirafter /@unixroot/usr/include/os2tk45"

%configure --disable-static --enable-binaries
# Remove rpath from speexenc and speexdec
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install
rm -f $RPM_BUILD_ROOT%{_docdir}/speex/manual.pdf
rm -f ${RPM_BUILD_ROOT}%{_libdir}/*.la

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc AUTHORS TODO ChangeLog README NEWS
%if !0%{?os2_version}
%{_libdir}/libspeex.so.1*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc doc/manual.pdf
%{_includedir}/speex
%{_datadir}/aclocal/speex.m4
%{_libdir}/pkgconfig/speex.pc
%if !0%{?os2_version}
%{_libdir}/libspeex.so
%exclude %{_libdir}/libspeex.la
%else
%{_libdir}/*.a
%endif

%files tools
%if !0%{?os2_version}
%{_bindir}/speexenc
%{_bindir}/speexdec
%else
%{_bindir}/speexenc.exe
%{_bindir}/speexdec.exe
%endif
%{_mandir}/man1/speexenc.1*
%{_mandir}/man1/speexdec.1*


%changelog
* Wed Sep 30 2020 Elbert Pol <elbert.pol@gmail.com> - 1.2.0-1
- First RPM for OS2
