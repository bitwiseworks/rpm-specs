Summary: The GNU macro processor
Name: m4
Version: 1.4.17
Release: 1%{?dist}
License: GPLv3+
Group: Applications/Text
#Source: http://ftp.gnu.org/gnu/m4/m4-%{version}.tar.xz
URL: http://www.gnu.org/software/m4/

%define svn_url     http://svn.netlabs.org/repos/ports/m4/trunk
%define svn_rev     841

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: subversion autoconf
#BuildRequires: makeinfo html2man

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

%description
A GNU implementation of the traditional UNIX macro processor.  M4 is
useful for writing text files which can be logically parsed, and is used
by many programs as part of their build process.  M4 has built-in
functions for including files, running shell commands, doing arithmetic,
etc.  The autoconf program needs m4 for generating configure scripts, but
not for running configure scripts.

Install m4 if you need a macro processor.

%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

#chmod 644 COPYING

%build

export CFLAGS="$RPM_OPT_FLAGS"
# YD do not use -Zbin-files
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lintl -lurpo"
#export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
#export MAKESHELL="/@unixroot/usr/bin/sh.exe"

# We can't bootstrap at the moment as it requires gnulib-tool located in a separate repo;
# call autoreconf directly instead
#./bootstrap -f

autoreconf --verbose --install
# autoreconf changes some doc files; prevent docs re-generation since we don't have
# makeinfo/html2man yet
touch doc/*

#export PATH=`echo $PATH | sed -e 's@\\\\@/@g'`
#export PATH_SEPARATOR=';'
#export ac_executable_extensions='.exe'

%configure

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install INSTALL="%{__install} -p" DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT%{_libdir}/charset.alias

#%check
#make %{?_smp_mflags} check

%files
%defattr(-,root,root,-)
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
%{_bindir}/m4.exe
%{_infodir}/*
%{_mandir}/man1/m4.1*

#%post
#if [ -f %{_infodir}/m4.info ]; then # --excludedocs?
#    /sbin/install-info %{_infodir}/m4.info %{_infodir}/dir || :
#fi

#%preun
#if [ "$1" = 0 ]; then
#    if [ -f %{_infodir}/m4.info ]; then # --excludedocs?
#        /sbin/install-info --delete %{_infodir}/m4.info %{_infodir}/dir || :
#    fi
#fi

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Aug 29 2014 Dmitriy Kuminov <coding@dmik.org> 1.4.17-1
- Updated to version 1.4.17.
- Rebuilt with LIBC 0.6.5 and GCC 4.7.3 in attempt to fix some problems (see #28).

* Fri Jan 06 2012 yd
- update trunk to 1.4.16
