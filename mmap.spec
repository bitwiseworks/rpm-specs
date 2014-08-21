Summary: Memory mapped file emulation library for OS/2
Name: mmap
Epoch: 2
Version: 0.5
Release: 1%{?dist}
License: unknown
Group: Development/Libraries

%define svn_url     http://svn.netlabs.org/repos/ports/mmap/trunk
%define svn_rev     824

%define wpstk_svn_url     http://svn.netlabs.org/repos/wpstk/trunk
%define wpstk_svn_rev     953

Source0: %{name}-%{version}-r%{svn_rev}.zip
Source1: wpstk-svn-r%{wpstk_svn_rev}.zip

BuildRequires: gcc make subversion

Requires: libc >= 0.6.3

%description
This library implements the mmap() API for C that is used to manipulate
memory mapped files. The API tries to emulate the mmap() functionality according
to Linux manual but some limitations currently exist. In particular, the MAP_FIXED
and MAP_SHARED flags are not yet supported.

%prep

%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

%if %(sh -c 'if test -f "%{_sourcedir}/wpstk-svn-r%{wpstk_svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q -TD -a 1
mv wpstk src/
%else
cd src
mkdir wpstk
svn export -r %{wpstk_svn_rev} %{wpstk_svn_url} wpstk --force
rm -f "%{_sourcedir}/wpstk-svn-r%{wpstk_svn_rev}.zip"
zip -SrX9 "%{_sourcedir}/wpstk-svn-r%{wpstk_svn_rev}.zip" "wpstk"
%endif

%build

cd src/wpstk
export MAKESHELL=cmd.exe
make -f GNUMakefile lib
make -f GNUMakefile lib DEBUG=1
export MAKESHELL=
cd ../..

export KCFLAGS="%{optflags}"
kmk -C src install
kmk -C src build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp mmap.dll %{buildroot}%{_libdir}
cp mmap_dll.a %{buildroot}%{_libdir}/mmap.a
cp mmap_s.lib %{buildroot}%{_libdir}
cp mmap_g.lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*

%changelog
* Thu Aug 21 2014 Dmitriy Kuminov <coding@dmik.org> 0.5-1
- Add support for offset parameter in mmap().
- Change versioning scheme (caused Epoch change).

* Wed Nov 02 2011 yd
- added -Zdll to build system
- improved build system
- included wpstk source code
