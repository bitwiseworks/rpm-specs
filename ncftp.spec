#define svn_url     g:/ncftp/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/Ncftp/trunk
%define svn_rev     1918

Summary: Improved console FTP client
Name: ncftp
Version: 3.2.6
Release: 2%{?dist}
License: Artistic clarified
Group: Applications/Internet
URL: http://www.ncftp.com/ncftp/
Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: autoconf, automake, libtool, ncurses-devel
Requires: ncurses >= 5.9

%description
Ncftp is an improved FTP client. Ncftp's improvements include support
for command line editing, command histories, recursive gets, automatic
anonymous logins, and more.

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

autoreconf -ifv -I autoconf_local

%build

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -ltinfo"
%configure 
make 

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}{%{_bindir},%{_mandir}/man1}
make install DESTDIR=%{buildroot}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc README* doc/html/
%doc doc/CHANGELOG.txt doc/FIREWALLS_AND_PROXIES.txt doc/LICENSE.txt
%doc doc/READLINE.txt doc/what_changed_between_v2_v3.txt
%{_bindir}/ncftp.exe
%{_bindir}/ncftpget.exe
%{_bindir}/ncftpput.exe
%{_bindir}/ncftpbatch.exe
%{_bindir}/ncftpls.exe
%{_bindir}/ncftpbookmarks.exe
%{_bindir}/ncftpspooler.exe
%{_mandir}/man1/ncftp.1*
%{_mandir}/man1/ncftpget.1*
%{_mandir}/man1/ncftpput.1*
%{_mandir}/man1/ncftpbatch.1*
%{_mandir}/man1/ncftpls.1*
%{_mandir}/man1/ncftpspooler.1*

%changelog
* Sat Jan 14 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.2.6-2
- fixed lpage issue (ticket #216)
- fixed case sensitivity (ticket #218)
- fixed ncftpbookmarks flaw (ticket #217), needs ncurses >=5.9

* Thu Dec 29 2016 Elbert Pol <elbert.pol@gmail.com> 3.2.6-1
- Initial package for version 3.2.6