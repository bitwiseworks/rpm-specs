#define svn_url     F:/rd/ports/urpo/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/urpo/trunk
%define svn_rev     947

%define kmk_dist out/os2.x86/release/dist

Summary: unlink rename pending operation
Name: urpo
Version: 20141223
Release: 7%{?dist}
License: LGPL
Group: Development/Libraries

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Requires: libc >= 0.6.5

%description
unlink rename pending operation library.

%package devel
Summary: Header files developing apps which will use pthread
Group: Development/Libraries

%description devel
Header files and a library of pthread functions, for developing apps
which will use the library.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
export KCFLAGS="%{optflags}"
kmk -C src
kmk -C src install
kmk -C src build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp %{kmk_dist}/bin/urpo.dll %{buildroot}%{_libdir}
cp %{kmk_dist}/lib/urpo.a %{buildroot}%{_libdir}/urpo.a
cp %{kmk_dist}/lib/urpo_g.a %{buildroot}%{_libdir}/urpo_g.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.dll

%files devel
%defattr(-,root,root)
%{_libdir}/*.a

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Tue Dec 23 2014 yd
- r947, implemented rmdir() support, ticket#50.
- r945, r946, build updates, static debug library.

* Wed Nov 02 2011 yd
- improved build system
