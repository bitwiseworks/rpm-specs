%global out out123
%global fmt fmt123
%global syn syn123

Name: mpg123
Version: 1.32.10
Release: 1%{?dist}

Summary: Real time MPEG 1.0/2.0/2.5 audio player/decoder for layers 1, 2 and 3
License: GPL-2.0-or-later
URL: https://mpg123.org
%if 0%{?os2_version}
Vendor:        TeLLie OS2 forever
Distribution:  OS/2
Packager:      TeLLie
%endif 

%if !0%{?os2_version}
Source0: %{url}/download/%{name}-%{version}.tar.bz2
%else
%scm_source github https://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: libtool
BuildRequires: make
%if !0%{?os2_version}
BuildRequires: pkgconfig(alsa)
%endif

Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%if 0%{?fedora}
%global enable_jack 1
%global enable_portaudio 1
%endif

%global _summary %{summary}

%global _description \
Real time MPEG 1.0/2.0/2.5 audio player/decoder for layers 1, 2 and 3 (most \
commonly MPEG 1.0 layer 3 aka MP3), as well as re-usable decoding and output \
libraries.

%description %{_description}

%package plugins-pulseaudio
Summary: Pulseaudio output plug-in for %{name}
%if !0%{?os2_version}
BuildRequires: pkgconfig(libpulse-simple)
%endif
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Supplements: (mpg123%{?_isa} and pulseaudio%{?_isa})
%endif

%description plugins-pulseaudio %{_description}

Pulseaudio output plug-in.

%if 0%{?enable_jack}
%package plugins-jack
Summary: JACK output plug-in for %{name}
BuildRequires: pkgconfig(jack)
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Supplements: (mpg123%{?_isa} and jack-audio-connection-kit%{?_isa})
%endif
Obsoletes: %{name}-plugins-extras < 1.23.4-1

%description plugins-jack %{_description}

JACK output plug-in.
%endif

%if 0%{?enable_portaudio}
%package plugins-portaudio
Summary: PortAudio output plug-in for %{name}
BuildRequires: pkgconfig(portaudio-2.0)
Requires: %{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 8
Supplements: (mpg123%{?_isa} and portaudio%{?_isa})
%endif

%description plugins-portaudio %{_description}

PortAudio output plug-in.
%endif


%package libs
Summary: %{_summary}
Provides: lib%{name} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: lib%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: lib%{name} < 1.23.4-1

%description libs %{_description}

%package devel
Summary: %{_summary}
%if !0%{?os2_version}
BuildRequires: /usr/bin/doxygen
%else
BuildRequires: /@unixroot/usr/bin/doxygen.exe
%endif
Requires: %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: lib%{name}-devel = %{?epoch:%{epoch}:}%{version}-%{release}
Provides: lib%{name}-devel%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Obsoletes: lib%{name}-devel < 1.23.4-1
Obsoletes: %{name}-libs-devel < 1.23.8-3

%description devel %{_description}

Development files for decoding and output libraries.

%prep
%if !0%{?os2_version}
%autosetup
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
autoreconf -ivf
%endif
%if !0%{?os2_version}
%configure --enable-modules=yes --with-default-audio=alsa \
  --with-audio=alsa,%{?enable_jack:jack},pulse,oss,%{?enable_portaudio:portaudio}
%else
export LDFLAGS="-Zomf -Zmap -Zhigh-mem -Zargs-resp -Zbin-files"
export LIBS="-lcx"

%configure --with-cpu=x86 --enable-debug=no --enable-modules=no --with-network=auto --with-default-audio=os2 
%endif

%make_build

%if !0%{?os2_version}
pushd doc
  doxygen doxygen.conf
popd
%else
cd doc
   doxygen doxygen.conf
cd ..  
%endif
   
%install
%make_install
rm %{buildroot}%{_libdir}/*.la

%if !0%{?os2_version}
%ldconfig_scriptlets libs
%endif

%files
%doc doc/README.remote
%if !0%{?os2_version}
%{_bindir}/%{name}
%{_bindir}/%{name}-id3dump
%{_bindir}/%{name}-strip
%{_bindir}/%{out}
%else
%{_bindir}/%{name}.exe
%{_bindir}/%{name}-id3dump.exe
%{_bindir}/%{name}-strip.exe
%{_bindir}/%{out}.exe
%endif
%doc %{_mandir}/man1/%{name}.1*
%doc %{_mandir}/man1/%{out}.1*
%if !0%{?os2_version}
%dir %{_libdir}/%{name}/
%{_libdir}/%{name}/output_alsa.*
%{_libdir}/%{name}/output_dummy.*
%{_libdir}/%{name}/output_oss.*
%endif

%if !0%{?os2_version}
%files plugins-pulseaudio
%{_libdir}/%{name}/output_pulse.*
%endif

%if 0%{?enable_jack}
%files plugins-jack
%{_libdir}/%{name}/output_jack.*
%endif

%if 0%{?enable_portaudio}
%files plugins-portaudio
%{_libdir}/%{name}/output_portaudio.*
%endif

%files libs
%license COPYING
%doc NEWS
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so.0*
%{_libdir}/lib%{out}.so.0*
%{_libdir}/lib%{syn}.so.0*
%else
%{_libdir}/*.dll
%endif

%files devel
%doc NEWS.lib%{name} doc/html doc/examples doc/BENCHMARKING doc/README.gain
%{_includedir}/%{name}.h
%{_includedir}/%{out}.h
%{_includedir}/%{fmt}.h
%{_includedir}/%{syn}.h
%if !0%{?os2_version}
%{_libdir}/lib%{name}.so
%{_libdir}/lib%{out}.so
%{_libdir}/lib%{syn}.so
%else
%{_libdir}/*.a
%endif
%{_libdir}/pkgconfig/lib%{name}.pc
%{_libdir}/pkgconfig/lib%{out}.pc
%{_libdir}/pkgconfig/lib%{syn}.pc

%changelog
* Mon Dec 16 2024 Elbert Pol <elbert.pol@gmail.com> - 1.32.10-1
- Updated to latest version.

* Tue Oct 29 2024 Elbert Pol <elbert.pol@gmail.com> - 1.32.8-1
- Updated to latest version.

* Fri Apr 04 2024 Elbert Pol <elbert.pol@gmail.com> - 1.32.6-1
- Updated to latest version.
- Add bldlevel to dll

* Fri Feb 23 2024 Elbert Pol <elbert.pol@gmail.com> - 1.32.5-1
- Updated to latest version

* Fri Jan 26 2024 Elbert Pol <elbert.pol@gmail.com> - 1.32.4-1
- Update to latest version
- Sync with latest Fedora spec
 
* Sun Jan 15 2023 Elbert Pol <elbert.pol@gmail.com> - 1.31.2-1
- Updated to latest version
- Thankz to Dave Yeo for the fixes he made for OS2
 
* Sat Nov 05 2022 Elbert Pol <elbert.pol@gmail.com> - 1.31.1-1
- Updated to latest version

* Wed Oct 26 2022 Elbert Pol <elbert.pol@gmail.com> - 1.31.0-1
- Updated to latest version

* Fri Jul 22 2022 Elbert Pol <elbert.pol@gmail.com> - 1.30.1-1
- Updated to latest version

* Wed Jun 29 2022 Elbert Pol <elbert.pol@gmail.com> - 1.30.0-1
- First RPM for OS2
- Thankz Dave Yeo for fixing OS2 releated errors
