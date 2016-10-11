#define svn_url     e:/trees/psutils/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/psutils/trunk
%define svn_rev     1725

Summary: PostScript Utilities
Name:    psutils
Version: 1.23
Release: 1%{?dist}
License: psutils
Group:   Development/Libraries

# We can't follow https://fedoraproject.org/wiki/Packaging:SourceURL#Github
# and use upstream tarball for building because ./bootstrap downloads gnulib.
# wget https://github.com/rrthomas/psutils/archive/master.zip && unzip master.zip && cd psutils-master/
# ./bootstrap && autoreconf -vfi && ./configure && make dist-xz
URL:     https://github.com/rrthomas/psutils
Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires:	autoconf
BuildRequires:	automake
#BuildRequires:  perl-generators
#BuildRequires:  perl(File::Basename)
#BuildRequires:  perl(Getopt::Long)
#BuildRequires:  perl(strict)
#BuildRequires:  perl(warnings)


%description
Utilities for manipulating PostScript documents.
Page selection and rearrangement are supported, including arrangement into
signatures for booklet printing, and page merging for n-up printing.


%package perl
Summary: psutils scripts requiring perl
BuildArch: noarch

%description perl
Various scripts from the psutils distribution that require perl.


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

autoreconf -fiv

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%doc README LICENSE
%{_bindir}/epsffit.exe
%{_bindir}/psbook.exe
%{_bindir}/psnup.exe
%{_bindir}/psresize.exe
%{_bindir}/psselect.exe
%{_bindir}/pstops.exe
%{_mandir}/man1/epsffit.1*
%{_mandir}/man1/psbook.1*
%{_mandir}/man1/psnup.1*
%{_mandir}/man1/psresize.1*
%{_mandir}/man1/psselect.1*
%{_mandir}/man1/pstops.1*
%{_mandir}/man1/psutils.1*


%files perl
%doc LICENSE
%{_bindir}/extractres
%{_bindir}/includeres
%{_bindir}/psjoin
%{_mandir}/man1/extractres.1*
%{_mandir}/man1/includeres.1*
%{_mandir}/man1/psjoin.1*


%changelog
* Tue Oct 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.23-1
- initial version
