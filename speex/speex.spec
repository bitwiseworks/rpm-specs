Summary:	A voice compression format (codec)
Name:		speex
Version:	1.2.1
Release:	1%{?dist}
License:	BSD-3-clause AND TU-Berlin-1.0
URL:		https://www.speex.org/
%if 0%{os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{?os2_version}
Source0:	https://downloads.xiph.org/releases/speex/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif
BuildRequires: make
BuildRequires:	gcc
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(speexdsp)
%if !0%{?os2_version}
Patch0:		speex-1.2.0-guard-against-invalid-channel-numbers.patch
%endif

%description
Speex is a patent-free compression format designed especially for
speech. It is specialized for voice communications at low bit-rates in
the 2-45 kbps range. Possible applications include Voice over IP
(VoIP), Internet audio streaming, audio books, and archiving of speech
data (e.g. voice mail).

%package devel
Summary: 	Development package for %{name}
%if !0%{?os2_version}
Requires: 	%{name}%{?_isa} = %{version}-%{release}
%else
Requires: 	%{name} = %{version}-%{release}
%endif

%description devel
Speex is a patent-free compression format designed especially for
speech. This package contains development files for %{name}

%package tools
Summary:	The tools package for %{name}
%if !0%{?os2_version}
Requires: 	%{name}%{?_isa} = %{version}-%{release}
%else
Requires: 	%{name} = %{version}-%{release}
%endif

%description tools
Speex is a patent-free compression format designed especially for
speech. This package contains tools files and user's manual for %{name}.

%prep
%if !0%{?os2_version}
%setup -q
%patch0 -p1 -b.CVE-2020-23903
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
autoreconf -ivf
%endif
%configure --disable-static --enable-binaries
# Remove rpath from speexenc and speexdec
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build

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
%{_libdir}/*_dll.a
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
* Thu Mar 07 2024 Elbert Pol <elbert.pol@gmail.com> -1.2.1-1
- Updated to latest version
- Add bldlevel to dll

* Wed Sep 30 2020 Elbert Pol <elbert.pol@gmail.com> - 1.2.0-1
- First RPM for OS2
