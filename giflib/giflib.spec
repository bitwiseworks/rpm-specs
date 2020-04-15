Name:          giflib
Summary:       A library and utilities for processing GIFs
Version:       5.2.1
Release:       2%{?dist}

License:       MIT
URL:           http://www.sourceforge.net/projects/%{name}/
Vendor:        bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
                   
BuildRequires: gcc
BuildRequires: make
BuildRequires: xmlto


%description
giflib is a library for reading and writing gif images.


%package devel
Summary:       Development files for programs using the giflib library
Requires:      %{name} = %{version}-%{release}

%description devel
The giflib-devel package includes header files, libraries necessary for
developing programs which use the giflib library.


%package utils
Summary:       Programs for manipulating GIF format image files
Requires:      %{name} = %{version}-%{release}

%description utils
The giflib-utils package contains various programs for manipulating GIF
format image files.

%debug_package

%prep
%scm_setup

%build
make CFLAGS="%{optflags} -fPIC" LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"


%install
%make_install PREFIX="%{_prefix}" LIBDIR="%{_libdir}"

# Drop static library
rm -f %{buildroot}%{_libdir}/libgif.a


#%ldconfig_scriptlets


%files 
%doc ChangeLog NEWS README
%license COPYING
%{_libdir}/gif7.dll

%files devel
%doc doc/*
%{_libdir}/libgif_dll.a
%{_includedir}/gif_lib.h

%files utils
%{_bindir}/gif*.exe
%{_mandir}/man1/*.1*


%changelog
* Wed Apr 15 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 5.2.1-2
- moved source to github
- synchronised with latest fedora spec
- removed double files in devel
- used original source and adjusted the Makefiles

* Sun Jul 07 2019 Elbert Pol <elbert.pol@gmail.com> - 5.2.1-1
- Updated to latest source
- Add debug package

* Mon Nov 19 2018 Elbert Pol <elbert.pol@gmail.com> - 5.1.4-2
- Some spec changes 

* Sun Nov 18 2018 Elbert Pol <elbert.pol@gmail.com> - 5.1.4-1
- First os2 rpm build
