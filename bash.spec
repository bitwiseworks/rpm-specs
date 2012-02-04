%define patchleveltag .0
%define baseversion 3.2

Summary: The GNU Bourne Again shell
Name: bash
Version: %{baseversion}%{patchleveltag}
Release: 6%{?dist}
License: BSD
Group: System Environment/Shells
Source: bash.zip
#Source: ftp://ftp.debian.org/debian/dists/woody/main/source/shells/%{name}_%{version}.orig.tar.gz
#Patch0: ftp://ftp.debian.org/debian/dists/woody/main/source/shells/%{name}_%{version}-38.diff.gz
#Patch2: ash-0.3.8-tempfile.patch
#Patch1: ash-0.3.8-build.patch
#Patch3: ash-0.3.8-mannewline.patch
#Patch4: ash-0.3.8-segv.patch
#Prereq: fileutils grep
#BuildPrereq: pmake >= 1.45 byacc
#Buildroot: %{_tmppath}/%{name}-%{version}-root
#Conflicts: mkinitrd <= 1.7

Provides: /@unixroot/bin/bash

%description
The GNU Bourne Again shell (Bash) is a shell or command language
interpreter that is compatible with the Bourne shell (sh). Bash
incorporates useful features from the Korn shell (ksh) and the C shell
(csh). Most sh scripts can be run by bash without modification.

%prep
%setup -q -n bash-%{version}
#%patch0 -p1 -b .linux
#%patch2 -p1 -b .tempfile
#%ifarch alpha
#%patch1 -p1 -b .alpha
#%endif
#%patch3 -p1
#%patch4 -p0 -b .segv
#chmod -R a+rX .

%build
#chmod u+x debian/bsdyacc
#pmake CFLAGS="-g ${RPM_OPT_FLAGS} \
#    -DBSD=1 -DSMALL -D_GNU_SOURCE \
#    -DGLOB_BROKEN -D__COPYRIGHT\(x\)= \
#    -D__RCSID\(x\)= -D_DIAGASSERT\(x\)=" \
#    YACC=`pwd`/debian/bsdyacc
#mv sh sh.dynamic
#
#pmake CFLAGS="-g ${RPM_OPT_FLAGS} \
#    -DBSD=1 -DSMALL -D_GNU_SOURCE \
#    -DGLOB_BROKEN -D__COPYRIGHT\(x\)= \
#    -D__RCSID\(x\)= -D_DIAGASSERT\(x\)=" \
#    YACC=`pwd`/debian/bsdyacc LDFLAGS="-static"
#mv sh sh.static


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}

cp -p usr/bin/bash.exe %{buildroot}%{_bindir}/bash.exe

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/bash.exe
#%{_mandir}/man1/*

%changelog
* Sat Feb 04 2012 yd
- added Provides for virtual /@unixroot/bin/bash file.
- Remove symlinks from /bin.

* Wed Nov 16 2011 yd
- keep all executables to /usr/bin and place symlinks in /bin
