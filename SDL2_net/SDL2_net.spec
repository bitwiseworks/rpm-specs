Name:		SDL2_net
Version:	2.0.1
Release:	1%{?dist}
Summary:	SDL portable network library
License:	zlib
URL:		http://www.libsdl.org/projects/SDL_net/
%if !0%{?os2_version}
Source0:	http://www.libsdl.org/projects/SDL_net/release/%{name}-%{version}.tar.gz
%else
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires:  gcc
BuildRequires:	SDL2-devel >= 2.0

%description
This is a portable network library for use with SDL.

%package	devel
Summary:	Libraries and includes to develop SDL networked applications
Requires:	%{name}%{?_isa} = %{version}-%{release}
Requires:	SDL2-devel%{?_isa} >= 2.0

%description	devel
This is a portable network library for use with SDL.

This is the libraries and include files you can use to develop SDL
networked applications.

%debug_package

%prep
%scm_setup
autoreconf -fiv
%if !0%{?os2_version}
%autosetup
%endif
# Fix end-of-line encoding
sed -i 's/\r//' README.txt CHANGES.txt COPYING.txt

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%configure --disable-static --disable-gui
make %{?_smp_mflags}

%install
%make_install
find %{buildroot} -name '*.la' -exec rm -f {} ';'

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
%{_libdir}/pkgconfig/*.pc

%changelog
* Tue Sep 08 2020 Elbert Pol <elbert.pol@gmail.com> - 2.0.1-1
- First rpm for OS2

