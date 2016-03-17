#define svn_url     e:/trees/bc/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/bc/trunk
%define svn_rev     1402

Summary: GNU's bc (a numeric processing language) and dc (a calculator)
Name: bc
Version: 1.06
Release: 1%{?dist}
License: GPL
URL: http://www.gnu.org/software/bc/
Group: Applications/Engineering
Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Requires(post): %{_sbindir}/install-info.exe
Requires(preun): %{_sbindir}/install-info.exe
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: readline-devel, flex

%description
The bc package includes bc and dc. Bc is an arbitrary precision
numeric processing arithmetic language. Dc is an interactive
arbitrary precision stack based calculator, which can be used as a
text mode calculator.

Install the bc package if you need its number handling capabilities or
if you would like to use its text mode calculator.

%debug_package

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
autoreconf -fi

export LDFLAGS=" -Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure --with-readline
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%post
if [ -f %{_infodir}/bc.info ]; then
   %{_sbindir}/install-info %{_infodir}/bc.info %{_infodir}/dir --entry="* bc: (bc).                      The GNU RPN calculator language." || :
   %{_sbindir}/install-info %{_infodir}/dc.info %{_infodir}/dir --entry="* dc: (dc).                      The GNU RPN calculator."|| :
fi

%preun
if [ $1 = 0 ]; then
   if [ -f %{_infodir}/bc.info ]; then
     %{_sbindir}/install-info --delete %{_infodir}/bc.info %{_infodir}/dir --entry="* bc: (bc).                      The GNU RPN calculator language." || :
     %{_sbindir}/install-info --delete %{_infodir}/dc.info %{_infodir}/dir --entry="* dc: (dc).                      The GNU RPN calculator." || :
   fi
fi

%files
%defattr(-,root,root,-)
%doc COPYING COPYING.LIB FAQ AUTHORS NEWS README
%{_bindir}/dc.exe
%{_bindir}/bc.exe
%{_mandir}/*/*
%{_infodir}/*

%changelog
* Thu Mar 17 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.06-1
- first version