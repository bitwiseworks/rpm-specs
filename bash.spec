%define patchleveltag .0
%define baseversion 3.2

Summary: The GNU Bourne Again shell
Name: bash
Version: %{baseversion}%{patchleveltag}
Release: 1
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
mkdir -p %{buildroot}/bin
mkdir -p %{buildroot}/usr/bin

cp usr/bin/bash.exe %{buildroot}/usr/bin/bash.exe
cp usr/bin/bash.exe %{buildroot}/bin/bash
#cp usr/bin/bash.exe %{buildroot}/bin/sh

#%post
#if [ ! -f /etc/shells ]; then
#	echo "/bin/ash" > /etc/shells
#	echo "/bin/bsh" >> /etc/shells
#else
#	if ! grep '^/bin/ash$' /etc/shells > /dev/null; then
#		echo "/bin/ash" >> /etc/shells
#	fi
#	if ! grep '^/bin/bsh$' /etc/shells > /dev/null; then
#		echo "/bin/bsh" >> /etc/shells
#	fi
#fi

#%postun
#if [ "$1" = "0" ]; then
#	grep -v '^/bin/ash' < /etc/shells | grep -v '^/bin/bsh' > /etc/shells.new
#	mv /etc/shells.new /etc/shells
#fi

%verifyscript
#
#for n in ash bsh; do
#    echo -n "Looking for $n in /etc/shells... "
#    if ! grep "^/bin/${n}\$" /etc/shells > /dev/null; then
#	echo "missing"
#	echo "${n} missing from /etc/shells" >&2
#    else
#	echo "found"
#    fi
#done

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
/bin/bash
/usr/bin/bash.exe
#/bin/bsh
#%{_mandir}/man1/*
