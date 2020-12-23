Summary:       A library of functions for manipulating PNG image format files
Name:          libpng
%if !0%{?os2_version}
Epoch:         2
%endif
Version:       1.6.37
Release:       1%{?dist}
License:       zlib
URL:           http://www.libpng.org/pub/png/

%if !0%{?os2_version}
Source0:       https://github.com/glennrp/%{name}/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:       pngusr.dfa
Patch0:        libpng-multilib.patch
Patch1:        libpng-fix-arm-neon.patch
%else
Vendor:        bww bitwise works GmbH
%scm_source    github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

BuildRequires: gcc
BuildRequires: zlib-devel
BuildRequires: autoconf automake libtool

%description
The libpng package contains a library of functions for creating and
manipulating PNG (Portable Network Graphics) image format files.  PNG
is a bit-mapped graphics format similar to the GIF format.  PNG was
created to replace the GIF format, since GIF uses a patented data
compression algorithm.

Libpng should be installed if you need to manipulate PNG format image
files.

%package devel
Summary:       Development tools for programs to manipulate PNG image format files
Requires:      %{name} = %{version}-%{release}
Requires:      zlib-devel pkgconfig

%description devel
The libpng-devel package contains header files and documentation necessary
for developing programs using the PNG (Portable Network Graphics) library.

If you want to develop programs which will manipulate PNG image format
files, you should install libpng-devel.  You'll also need to install
the libpng package.

%package static
Summary:       Static PNG image format file library
Requires:      %{name}-devel = %{version}-%{release}

%description static
The libpng-static package contains the statically linkable version of libpng.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

%package tools
Summary:       Tools for PNG image format file library
Requires:      %{name} = %{version}-%{release}

%description tools
The libpng-tools package contains tools used by the authors of libpng.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q
# Provide pngusr.dfa for build.
cp -p %{SOURCE1} .

%patch0 -p1
%patch1 -p1 -b .arm
%else
%scm_setup
%endif


%build
autoreconf -vif
%if 0%{?os2_version}
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export VENDOR="%{vendor}"
%endif

%configure
%if !0%{?os2_version}
%make_build DFA_XTRA=pngusr.dfa
%else
make %{?_smp_mflags}
%endif

%install
%make_install

# We don't ship .la files.
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

%check
%if 0%{?os2_version}
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/.libs
%endif
#to run make check use "--with check"
%if %{?_with_check:1}%{!?_with_check:0}
make check
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%if !0%{?os2_version}
%{_libdir}/libpng16.so.*
%else
%{_libdir}/png*.dll
%endif
%{_mandir}/man5/*

%files devel
%doc libpng-manual.txt example.c TODO CHANGES
%{_bindir}/*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%exclude %{_bindir}/pngfix.exe
%endif
%{_includedir}/*
%if !0%{?os2_version}
%{_libdir}/libpng*.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/libpng*.pc
%{_mandir}/man3/*

%files static
%{_libdir}/libpng*.a
%if 0%{?os2_version}
%{_libdir}/png*.a
%exclude %{_libdir}/*_dll.a
%endif

%files tools
%if !0%{?os2_version}
%{_bindir}/pngfix
%else
%{_bindir}/pngfix.exe
%endif

%changelog
* Wed Dec 23 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.37-1
- updated libpng to 1.6.37
- resynced with latest fedora spec

* Wed Aug 09 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.31-1
- updated libpng to 1.6.31

* Mon Feb 06 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.28-1
- updated libpng to 1.6.28
- use new scm_source and scm_setup macro
- add bldlevel info to the dll

* Thu Apr 7 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.21-3
- added apng support
  used patch from https://sourceforge.net/projects/libpng-apng/files
- removed -Zbin-files, as not needed

* Fri Feb 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.21-2
- remove %{?_isa} macro

* Fri Feb 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.21-1
- updated libpng to 1.6.21
- adjusted debug package creation to latest rpm macros

* Tue Sep 15 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.18-1
- updated libpng to 1.6.18

* Mon Feb 16 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.16-1
- updated libpng to 1.6.16
- add symlink for libpng

* Tue Feb 10 2015 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.6.14-1
- updated libpng to 1.6.14
- added .dbg files

* Thu Apr 17 2014 yd
- first public build.
