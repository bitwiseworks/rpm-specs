Summary: Locate a program file in the user's paths
Name: which
Version: 1.0
Release: 2%{?dist}
License: none
URL: http://sources.freebsd.org/releng/10.0/usr.bin/which/

Group: Applications/System

#%scm_source svn http://svn.netlabs.org/repos/ports/which/trunk 733

BuildRequires: gcc make

%description
The which utility takes a list of command names and searches the path for each executable file
that would be run had these commands actually been invoked.

%debug_package

%prep
%scm_setup

%build
export CFLAGS="$RPM_OPT_FLAGS"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
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
%{_bindir}/which.exe
%{_mandir}/man1/which.1*

%changelog
* Wed Feb 8 2017 Dmitriy Kuminov <coding@dmik.org> 1.0-2
- Build against LIBCx to enable EXCEPTQ trap report generation.
- Add debug info package.
- Use scm_source/scm_setup for downloading sources.

* Wed Jun 4 2014 Dmitriy Kuminov <coding@dmik.org> 1.0-1
- Initial port of BSD which (release 10.0).
