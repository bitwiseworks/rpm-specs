Summary: A utility for unpacking zip files
Name: unzip
Version: 6.0
Release: 7%{?dist}
License: BSD
Group: Applications/Archiving
Vendor: bww bitwise works GmbH

%scm_source svn http://svn.netlabs.org/repos/ports/unzip/trunk 2285

URL: http://www.info-zip.org/UnZip.html
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  bzip2-devel
Requires:  bzip2

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

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README BUGS LICENSE 
%{_bindir}/*.exe
%{_bindir}/*.cmd
%{_mandir}/*/*

%changelog
* Tue Jun 12 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 6.0-7
- fix ticket #184

* Thu Jan 19 2017 Herwig Bauernfeild <herwig.bauernfeind@bitwiseworks.com> 6.0-6
- fix wildcards ticket #136

* Fri Mar 29 2013 yd
- r616, enable symlink support also for OS/2 code. ticket:18.
