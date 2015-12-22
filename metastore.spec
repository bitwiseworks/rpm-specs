%define svn_url     F:/rd/metastore/trunk

Name: metastore
Version: 0.0
Release: 2%{?dist}

Summary: Metastore stores metadata for git
License: GPL2
Group: Development/Other
Url: git://git.hardeman.nu/metastore.git
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Packager: Evgenii Terechkov <evg@altlinux.org>

# Automatically added by buildreq on Wed Jan 02 2008
#BuildRequires: libattr-devel

%description
Metastore stores metadata for git

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
echo %{svn_rev}
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
export RPM_CFLAGS="%{optflags}"
make prefix=%_prefix mandir=%_mandir

%install
mkdir -p %{RPM_BUILD_ROOT}/%{_mandir} %{RPM_BUILD_ROOT}/%{_bindir}
make install DESTDIR=${RPM_BUILD_ROOT} prefix=%_prefix mandir=%_mandir

%files
%_bindir/%name.exe
%_mandir/*

%doc README examples

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg

%changelog
