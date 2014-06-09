#
# How to prepare a new source ZIP from SVN:
# 1. svn export -r NNN SVN_URL NAME-rNNN
# 2. zip -SrX9 NAME-rNNN.zip which-rXXX
#

Summary: Locate a program file in the user's paths
Name: which
Version: 1.0
Release: 1%{?dist}
License: none
URL: http://sources.freebsd.org/releng/10.0/usr.bin/which/

Group: Applications/System

%define svn_url     http://svn.netlabs.org/repos/ports/which/trunk
%define svn_rev     733

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: gcc make subversion

%description
The which utility takes a list of command names and searches the path for each executable file
that would be run had these commands actually been invoked.

%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
make -f Makefile.os2

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
mkdir -p %{buildroot}/%{_mandir}/man1
cp which.exe %{buildroot}/%{_bindir}/
cp which.1 %{buildroot}/%{_mandir}/man1/

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/which.exe
%{_mandir}/man1/which.1*

%changelog

* Wed Jun 4 2014 Dmitriy Kuminov <coding@dmik.org> 1.0-1
- Initial port of BSD which (release 10.0).
