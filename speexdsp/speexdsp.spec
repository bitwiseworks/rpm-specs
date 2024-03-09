Name:           speexdsp
Version:        1.2.0
Release:        1%{?dist}
Summary:        A voice compression format (DSP)

Group:          System Environment/Libraries
License:        BSD
URL:            http://www.speex.org/
%if !0%{?os2_version}
Source0:        http://downloads.xiph.org/releases/speex/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif

BuildRequires:  gcc
# speexdsp was split from speex in 1.2rc2. As speexdsp does not depend on
# speex, a versioned conflict is required.
Conflicts: speex <= 1.2-0.21.rc1

%description
Speex is a patent-free compression format designed especially for
speech. It is specialized for voice communications at low bit-rates in
the 2-45 kbps range. Possible applications include Voice over IP
(VoIP), Internet audio streaming, audio books, and archiving of speech
data (e.g. voice mail).

This is the DSP package, see the speex package for the codec part.

%package devel
Summary: 	Development package for %{name}
Group: 		Development/Libraries
Requires: 	%{name}%{?_isa} = %{version}-%{release}
# speexdsp was split from speex in 1.2rc2. As speexdsp does not depend on
# speex, a versioned conflict is required.
Conflicts: speex-devel <= 1.2-0.21.rc1

%description devel
Speex is a patent-free compression format designed especially for
speech. This package contains development files for %{name}

This is the DSP package, see the speex package for the codec part.

%debug_package

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif

%build
autoreconf -vfi
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lmmpm2"
export CFLAGS="-idirafter /@unixroot/usr/include/os2tk45"

%configure \
%ifarch aarch64
	--disable-neon \
%endif
	--disable-static

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install

# Remove libtool archives
find %{buildroot} -type f -name "*.la" -delete

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%doc AUTHORS COPYING TODO ChangeLog README NEWS doc/manual.pdf
%doc %{_docdir}/speexdsp/manual.pdf
%if !0%{?os2_version}
%{_libdir}/libspeexdsp.so.*
%else
%{_libdir}/*.dll
%endif

%files devel
%{_includedir}/speex
%{_libdir}/pkgconfig/speexdsp.pc
%if !0%{?os2_version}
%{_libdir}/libspeexdsp.so
%else
%{_libdir}/*.a
%endif

%changelog
* Tue Sep 29 2020 Elbert Pol <elbert.pol@gmail.com> - 1.2.0-1
- First RPM for OS2

