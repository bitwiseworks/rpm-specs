%global _version 1.31.1

Name:           faac
Version:        1.31.1
Release:        1%{?dist}
Summary:        Encoder and encoding library for MPEG2/4 AAC

License:        LGPLv2+
URL:            http://www.audiocoding.com/
%if 0%{os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{?os2_version}
Source0:        https://github.com/knik0/faac/archive/%{_version}/%{name}-%{_version}.tar.gz
%else
%scm_source github https://github.com/Tellie/%{name}-os2 %{version}-os2
%endif

BuildRequires:  gcc
BuildRequires:  automake
BuildRequires:  libtool
%if !0%{?os2_version}
Patch0:         faac-1.30-drm.patch
%endif

%description
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

%package devel
Summary:        Development libraries of the FAAC AAC encoder
%if !0%{?os2_version}
Requires: %{name}%{?_isa} = %{version}-%{release}
%else
Requires: %{name} = %{version}-%{release}
%endif

%description devel
FAAC is an AAC audio encoder. It currently supports MPEG-4 LTP, MAIN and LOW
COMPLEXITY object types and MAIN and LOW MPEG-2 object types. It also supports
multichannel and gapless encoding.

This package contains development files and documentation for libfaac.

%prep

%if !0%{?os2_version}
%setup -q -n %{name}-%{_version}
%patch0 -p1 -b .drm
#fix encoding
/usr/bin/iconv -f iso8859-1 -t utf-8 AUTHORS > AUTHORS.conv && touch -r AUTHORS AUTHORS.conv && /bin/mv -f AUTHORS.conv AUTHORS
%else
%scm_setup
%endif
./bootstrap

%build
%if 0%{?os2_version}
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
%configure --disable-static
sed -i 's|^hardcode_libdir_flag_spec=.*|hardcode_libdir_flag_spec=""|g' libtool
sed -i 's|^runpath_var=LD_RUN_PATH|runpath_var=DIE_RPATH_DIE|g' libtool
%make_build


%install
%make_install

#Remove libtool archives.
%if !0%{?os2_version}
find %buildroot -name '*.la' -or -name '*.a' | xargs rm -f
%else
find %buildroot -name '*.la' | xargs rm -f
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%doc AUTHORS ChangeLog NEWS README TODO docs/*
%license COPYING
%if !0%{?os2_version}
%{_bindir}/*
%{_libdir}/*.so.*
%else
%{_bindir}/%{name}.exe
%{_libdir}/%{name}*.dll
%endif
%{_mandir}/man1/%{name}*

%files devel
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/faac.pc
%{_includedir}/*.h

%changelog
* Mon Mar 03 2025 Elbert Pol <elbert.pol@gmail.com> - 1.31.1-1
- Updated to latest version

* Fri Feb 28 2025 Elbert Pol <elbert.pol@gmail.com> - 1.31-1
- Updated to latest version

* Fri Feb 09 2024 Elbert Pol <elbert.pol@gmail.com> - 1.30-1
- Update to latest version
- resync with latest fedora spec
- Add bldlevel to the dll
- Based on os2 source from KO Myung-Hun

* Wed Oct 09 2019 Elbert Pol <elbert.pol@gmail.com> - 1.29.9.2-1
- First rpm for OS2
- Thankz KO Myung-Hun for the OS2 source

