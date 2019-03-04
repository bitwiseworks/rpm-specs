%global ncftp_ico ncftp_os2.ico

Summary: Improved console FTP client
Name: ncftp
Version: 3.2.6
Release: 6%{?dist}
License: Artistic clarified
Group: Applications/Internet
URL: http://www.ncftp.com/ncftp/

Vendor:  bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/Ncftp/trunk 2341

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: autoconf, automake, libtool, ncurses-devel
BuildRequires: bww-resources-rpm-build
Requires: bww-resources-rpm
Requires: ncurses >= 5.9

%description
Ncftp is an improved FTP client. Ncftp's improvements include support
for command line editing, command histories, recursive gets, automatic
anonymous logins, and more.

%debug_package

%prep
%scm_setup

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
install -p -m0644 -D %{ncftp_ico} $RPM_BUILD_ROOT%{_datadir}/os2/icons/%{ncftp_ico}

%clean
rm -rf %{buildroot}

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi
# for the definition of the parameters see macros.bww
%global title %{summary}
%bww_folder -t %{title}
%bww_app -f %{_bindir}/%{name}.exe -t %{title} -i %{ncftp_ico}
%bww_app_shadow
%bww_app ncftpbookmarks -f %{_bindir}/ncftpbookmarks.exe -t bookmarks
%bww_readme -f %{_defaultdocdir}/%{name}-%{version}/README.txt

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi

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
%{_datadir}/os2/icons/%{ncftp_ico}

%changelog
* Mon Mar 04 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.2.6-6
- rebuild with latest macros.bww
- rebuild with latext libc and libcx
- better version to find sa_family

* Wed Jun 28 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.2.6-5
- rebuild with latest macro.bww

* Fri Mar 10 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.2.6-4
- change the way to add a icon
- adjust to latest bww res macro

* Fri Feb 17 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.2.6-3
- add icon to ncftp.exe
- use new scm_source and scm_setup macro
- add wps objects

* Sat Jan 14 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.2.6-2
- fixed lpage issue (ticket #216)
- fixed case sensitivity (ticket #218)
- fixed ncftpbookmarks flaw (ticket #217), needs ncurses >=5.9

* Thu Dec 29 2016 Elbert Pol <elbert.pol@gmail.com> 3.2.6-1
- Initial package for version 3.2.6