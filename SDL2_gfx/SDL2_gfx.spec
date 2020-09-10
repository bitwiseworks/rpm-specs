Summary: SDL2 graphics drawing primitives and other support functions
Name: SDL2_gfx
Version: 1.0.4
Release: 3%{?dist}
License: zlib
URL: http://www.ferzkopp.net/Software/SDL2_gfx-2.0/
%if !0%{?os2_version}
Source: http://www.ferzkopp.net/Software/SDL2_gfx/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

# Requires --batch support not currently in SDL2_test
#Patch0: 0001-test-Add-batch-switch.patch
%if !0%{?os2_version}
Patch1: 0002-test-format-security.patch
%endif

BuildRequires: gcc libtool
BuildRequires: SDL2-devel
%if !0%{?os2_version}
# for -lSDL2_test
BuildRequires: SDL2-static
BuildRequires: doxygen
%endif

%description
Library providing graphics drawing primitives and other support functions
wrapped up in an addon library for the Simple Direct Media version 2 (SDL2)
cross-platform API layer.

%package devel
Summary: Development files for SDL2_gfx
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: SDL2-devel%{?_isa}

%description devel
This package contains the files required to develop programs which use SDL2_gfx.

%package docs
Summary: API Documentation for SDL2_gfx
BuildArch: noarch
Requires: %{name} = %{version}-%{release}

%description docs
This package contains the API documentation for SDL2_gfx library.

%debug_package

%prep
%if !0%{?os2_version}
%autosetup -p1
mv test/TestGfx.c test/testgfx.c
%endif
%scm_setup
autoreconf -ivf
find -name '*.[ch]' |xargs chmod -x
chmod -x NEWS README AUTHORS COPYING
sed -i 's/\r//' README

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%configure \
%if !0%{?os2_version}
%ifnarch %{ix86} x86_64
    --disable-mmx \
%endif
%endif
    --disable-static
make %{?_smp_mflags}

# API documentation
cd Docs
rm -rf html
doxygen html.doxyfile
cd ..

%if !0%{?os2_version}
# Examples & test suite
pushd test
  # test/Makefile.in does not respect LDFLAGS
  export CFLAGS='%{optflags} -I.. -L../.libs'
  %configure
  %make_build
popd
%endif

%install
%make_install

# Missing from Makefile.am
install -pm644 SDL2_gfxPrimitives_font.h %{buildroot}%{_includedir}/SDL2/

# API documentation
mkdir -p %{buildroot}%{_pkgdocdir}
cp -a Docs/html %{buildroot}%{_pkgdocdir}/

%if !0%{?os2_version}
# This might be useful for live tests; ship it in the devel package
install -d %{buildroot}%{_libdir}/%{name}
install test/testgfx %{buildroot}%{_libdir}/%{name}
install -Dpm0644 %{name}.pc %{buildroot}%{_libdir}/pkgconfig/%{name}.pc
%endif

find %{buildroot} -type f -name '*.la' -delete

%check
%if !0%{?os2_version}
export SDL_VIDEODRIVER=dummy
export LD_LIBRARY_PATH="$PWD/.libs"
cd test
#./testgfx --info all --log all --batch
#./testrotozoom --info all --log all --batch
./testimagefilter

%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc NEWS README AUTHORS
%{_libdir}/*.dll

%files devel
%{_includedir}/SDL2/*.h
%{_libdir}/*.a
%if !0%{?os2_version}
%{_libdir}/%{name}
%endif
%{_libdir}/pkgconfig/%{name}.pc

%files docs
%{_pkgdocdir}/html

%changelog
* Tue Sep 08 2020 Elbert Pol <elbert.pol@gmail.com> - 1.0.4-1
- First rpm for OS2

