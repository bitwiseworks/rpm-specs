Name:		SDL2_ttf
Version:	2.0.15
Release:	2%{?dist}
Summary:	TrueType font rendering library for SDL2
License:	zlib
URL:		https://www.libsdl.org/projects/SDL_ttf/
%if !0%{?os2_version}
Source0:	%{url}release/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

%if !0%{?os2_version}
BuildRequires:  libGL-devel
%endif
BuildRequires:  gcc
BuildRequires:	SDL2-devel
BuildRequires:	freetype-devel
BuildRequires:	zlib-devel

%description
This library allows you to use TrueType fonts to render text in SDL2
applications.

%package devel
Summary:	Development files for %{name}
Requires:	%{name}%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:	SDL2-devel%{?_isa}

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%debug_package

%prep
%scm_setup
autoreconf -fiv
%if !0%{?os2_version}
%autosetup
rm -rf external
%endif
# Fix end-of-line encoding
sed -i 's/\r//' README.txt CHANGES.txt COPYING.txt

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%configure --disable-dependency-tracking --disable-static
sed -i -e 's! -shared ! -Wl,--as-needed\0!g' libtool
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -type f -name '*.la' -delete -print

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING.txt
%doc README.txt CHANGES.txt
%{_libdir}/*.dll

%files devel
%{_libdir}/*.a
%{_includedir}/SDL2/*
%{_libdir}/pkgconfig/%{name}.pc

%changelog
* Tue Oct 20 2020 Elbert Pol <elbert.pol@gmail.com> - 2.0.15-2
- Update cause i had a wrong macros.dist

* Tue Sep 08 2020 Elbert Pol <elbert.pol@gmail.com> - 2.0.15-1
- First rpm for OS2
