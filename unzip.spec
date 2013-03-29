Summary: A utility for unpacking zip files
Name: unzip
Version: 6.0
Release: 5%{?dist}
License: BSD
Group: Applications/Archiving
Source: http://downloads.sourceforge.net/infozip/unzip60.tar.gz

Patch0: unzip-os2.diff

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

%prep
%setup -q -n unzip60
%patch0 -p1 -b .os2~

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
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Fri Mar 29 2013 yd
- r616, enable symlink support also for OS/2 code. ticket:18.
