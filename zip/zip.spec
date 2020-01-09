Summary: A file compression and packaging utility compatible with PKZIP
Name: zip
Version: 3.0
Release: 9%{?dist}
License: BSD
Group: Applications/Archiving
URL: http://www.info-zip.org/Zip.html
Vendor:  bww bitwise works GmbH

%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-9

%description
The zip program is a compression and file packaging utility.  Zip is
analogous to a combination of the UNIX tar and compress commands and
is compatible with PKZIP (a compression and file packaging utility for
MS-DOS systems).

Install the zip package if you need to compress files using the zip
program.

%debug_package

%prep
%scm_setup

%build
export CFLAGS="$RPM_OPT_FLAGS"
make -f os2/Makefile.os2 prefix=%{_prefix} klibc %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_bindir} 
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

make -f os2/Makefile.os2 prefix=$RPM_BUILD_ROOT%{_prefix} \
        MANDIR=$RPM_BUILD_ROOT%{_mandir}/man1 install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README CHANGES TODO WHATSNEW WHERE LICENSE README.CR
%doc proginfo/algorith.txt
%{_bindir}/zipnote.exe
%{_bindir}/zipsplit.exe
%{_bindir}/zip.exe
%{_bindir}/zipcloak.exe
%{_mandir}/man1/zip.1*
%{_mandir}/man1/zipcloak.1*
%{_mandir}/man1/zipnote.1*
%{_mandir}/man1/zipsplit.1*

%changelog
* Wed Jan 08 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.0-9
- fix a 4GB issue 

* Fri Sep 28 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.0-8
- fix volume label info rpm Ticket #319

* Mon Feb 19 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.0-7
- use new scm_source and scm_setup macro
- fix wildcard and current dir processing. Ticket #179

* Wed Jul 24 2013 yd
- r659, added support for archive bit clearing by Alex Taylor. Ticket:21.

* Fri Mar 29 2013 yd
- r614 r615, restore default behaviour for symlink storage. Ticket:18.
