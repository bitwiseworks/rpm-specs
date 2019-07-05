Summary: GNU's bc (a numeric processing language) and dc (a calculator)
Name: bc
Version: 1.07.1
Release: 1%{?dist}
License: GPL
URL: http://www.gnu.org/software/bc/
Group: Applications/Engineering

Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: readline-devel, flex, bison, texinfo, ed, dos2unix

%description
The bc package includes bc and dc. Bc is an arbitrary precision
numeric processing arithmetic language. Dc is an interactive
arbitrary precision stack based calculator, which can be used as a
text mode calculator.

Install the bc package if you need its number handling capabilities or
if you would like to use its text mode calculator.

%debug_package

%prep
%scm_setup

%build
autoreconf -fi

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%configure --with-readline
make %{?_smp_mflags}

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%files
%defattr(-,root,root,-)
%license COPYING COPYING.LIB
%doc FAQ AUTHORS NEWS README Examples/
%{_bindir}/dc.exe
%{_bindir}/bc.exe
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Wed May 22 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.07.1-1
- update to latest version
- moved source to github
- use scm_ macros

* Thu Mar 17 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.06-1
- first version
