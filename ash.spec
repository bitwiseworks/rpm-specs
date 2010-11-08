Summary: A smaller version of the Bourne shell (sh).
Name: ash
Version: 0.0.0
Release: 3
License: BSD
Group: System Environment/Shells
Source: ash.zip
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

Requires: libc >= 0.6.3

%description
A shell is a basic system program that interprets keyboard and mouse
commands. The ash shell is a clone of Berkeley's Bourne shell
(sh). Ash supports all of the standard sh shell commands, but is
considerably smaller than sh. The ash shell lacks some Bourne shell
features (for example, command-line histories), but it uses a lot less
memory.

You should install ash if you need a lightweight shell with many of
the same capabilities as the sh shell.

%prep
%setup -q -n ash-%{version}
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
mkdir -p %{buildroot}/@unixroot/bin
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

cp bin/ash.exe %{buildroot}/@unixroot/bin/sh.exe
ln -s sh.exe %{buildroot}/@unixroot/bin/sh

cp usr/man/man1/ash.1.gz %{buildroot}%{_mandir}/man1/ash.1.gz

#ln -sf ash.1 %{buildroot}%{_mandir}/man1/bsh.1
#ln -sf ash %{buildroot}/bin/bsh
#install -m 755 sh.static %{buildroot}/bin/ash.static

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
/@unixroot/bin/sh
/@unixroot/bin/sh.exe
#/bin/bsh
%{_mandir}/man1/*
