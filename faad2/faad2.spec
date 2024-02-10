Summary:	Library and frontend for decoding MPEG2/4 AAC
Name:		faad2
Epoch:		1
Version:	2.11.1
Release:	1%{?dist}
License:	GPLv2+
URL:		http://www.audiocoding.com/faad2.html
%if 0%{os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{?os2_version}
Source:		https://github.com/knik0/faad2/archive/%{version}/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/tellie/%{name}-os2 %{version}-os2
%endif

BuildRequires:	gcc-c++
BuildRequires:  cmake
%if !0%{?os2_version}
BuildRequires:  libsysfs-devel
%endif

%if !0%{?os2_version}
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
%endif
Obsoletes:	%{name}-xmms < %{version}-%{release}

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder, completely
written from scratch.

%package libs
Summary:	Shared libraries of the FAAD 2 AAC decoder

%description libs
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder, completely
written from scratch.

This package contains libfaad.

%package devel
Summary:	Development libraries of the FAAD 2 AAC decoder
%if !0%{?os2_version}
Requires:	%{name}-libs%{?_isa} = %{epoch}:%{version}-%{release}
%else
Requires:       %{name}-libs = %{epoch}:%{version}-%{release}
%endif


%description devel
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder, completely
written from scratch.

This package contains development files and documentation for libfaad.

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif

%build
%cmake

%cmake_build

%install
%cmake_install
install -m 0755 -d %{buildroot}%{_mandir}/man3
install -D -m 644 docs/libfaad.3 -t %{buildroot}%{_mandir}/man3/

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%files
%doc AUTHORS ChangeLog README*
%license COPYING
%if !0%{?os2_version}
%{_bindir}/faad
%else
%{_bindir}/faad.exe
%endif
%{_mandir}/man1/faad.1*

%files libs
%if !0%{?os2_version}
%{_libdir}/libfaad*.so.*
%else
%{_libdir}/*.dll
%endif
%{_mandir}/man3/libfaad.3*

%files devel
%{_includedir}/faad.h
%{_includedir}/neaacdec.h
%{_libdir}/pkgconfig/faad2.pc
%if !0%{?os2_version}
%{_libdir}/libfaad*.so
%else
%{_libdir}/*_dll.a
%endif

%changelog
* Sat Feb 10 2024 Elbert Pol <elbert.pol@gmail.com> - 2.11.1-1
- Update to latest version
- resync with latest fedora spec
- Add bldlevel to the dll and exe file
- Based on os2 source from KO Myung-Hun

* Wed Oct 09 2019 Elbert Pol <elbert.pol@gmail.com> - 2.8.8-1
- First rpm for OS2
- Thankz KO Myung-Hun for the OS2 source
