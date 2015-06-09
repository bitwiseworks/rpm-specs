#define svn_url     F:/rd/ports/urpo/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/urpo/trunk
%define svn_rev     1149

%define kmk_dist out/os2.x86/release/dist

Summary: unlink rename pending operation
Name: urpo
Version: 20150513
Release: 11%{?dist}
License: LGPL
Group: Development/Libraries

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Requires: libc >= 0.6.6

%description
unlink rename pending operation library, allows programs to rename/unlink
opened files.

%package devel
Summary: Header files developing apps which will use urpo
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Header files and a library of urpo functions, for developing apps
which will use the library.

%package debug
Summary: HLL debug data for exception handling support.
Requires: %{name} = %{version}-%{release}

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
cp src/urpo.h %{buildroot}%{_includedir}/urpo.h
cp %{kmk_dist}/lib/urpo_g.a %{buildroot}%{_libdir}/urpo_g.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.dll

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/*.h

%files debug
%defattr(-,root,root)
%{_libdir}/*.dbg

%changelog
* Tue Jun 09 2015 yd <yd@os2power.com> 20150513-11
- force -devel and -debug to depend on main package, see ticket:138.

* Wed May 13 2015 yd <yd@os2power.com> 20150513-10
- r1149, Add renameForce() to headers and docs. ticket#68.

* Thu Jan 01 2015 yd
- r949, Add a new renameForce() update to resolve RPM issue#99. ticket#50.
- r948, remove file from pending list if missing.

* Tue Dec 23 2014 yd
- r947, implemented rmdir() support, ticket#50.
- r945, r946, build updates, static debug library.

* Wed Nov 02 2011 yd
- improved build system
