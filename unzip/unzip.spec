Summary: A utility for unpacking zip files
Name: unzip
Version: 6.0
Release: 9%{?dist}
License: BSD
Vendor: bww bitwise works GmbH

%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-2

URL: http://www.info-zip.org/UnZip.html
BuildRequires:  bzip2-devel
Requires:  bzip2
Requires:  zip >= 3.0

BuildRequires: rexx_exe

%description
The unzip utility is used to list, test, or extract files from a zip
archive.  Zip archives are commonly found on MS-DOS systems.  The zip
utility, included in the zip package, creates zip archives.  Zip and
unzip are both compatible with archives created by PKWARE(R)'s PKZIP
for MS-DOS, but the programs' options and default behaviors do differ
in some respects.

Install the unzip package if you need to list, test or extract files from
a zip archive.


%debug_package


%prep
%scm_setup

%build
make -f os2/Makefile.os2 CFLAGS="$RPM_OPT_FLAGS" klibc %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make -f os2/Makefile.os2 prefix=$RPM_BUILD_ROOT%{_prefix} MANDIR=$RPM_BUILD_ROOT/%{_mandir}/man1 INSTALL="cp -p" install

# create a exe out of the cmd files
for f in $RPM_BUILD_ROOT%{_prefix}/bin/*.cmd ; do
  rexx2vio "$f" "${f%.cmd}.exe"
  rm -f "$f"
done

%files
%defattr(-,root,root)
%doc README BUGS LICENSE 
%{_bindir}/*.exe
%{_mandir}/*/*

%changelog
* Fri Jun 12 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 6.0-9
- better version to find zip.exe in zip2exe (Herwig Bauernfeind)
- use a nicer -v sting (ticket #1)

* Wed Jun 03 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 6.0-8
- fix zip ticket #1 done by Herwig Bauernfeind
- deliver *.cmd as *.exe

* Tue Jun 12 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 6.0-7
- fix ticket #184

* Thu Jan 19 2017 Herwig Bauernfeild <herwig.bauernfeind@bitwiseworks.com> 6.0-6
- fix wildcards ticket #136

* Fri Mar 29 2013 yd
- r616, enable symlink support also for OS/2 code. ticket:18.
