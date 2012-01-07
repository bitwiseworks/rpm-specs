# -*- coding: utf-8 -*-
%ifos linux
%define _bindir /bin
%endif

Summary: A GNU stream text editor
Name: sed
Version: 4.2.1
Release: 1%{?dist}
License: GPLv3+
Group: Applications/Text
URL: http://sed.sourceforge.net/
Source0: ftp://ftp.gnu.org/pub/gnu/sed/sed-%{version}.tar.bz2
Source1: http://sed.sourceforge.net/sedfaq.txt
Patch0: sed-4.2.1-copy.patch
Patch1: sed-4.2.1-makecheck.patch
Patch2: sed-os2.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires: libc-devel
Requires(post): /sbin/install-info
Requires(preun): /sbin/install-info

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
%configure \
     --without-included-regex \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{_smp_mflags}
install -m 644 -p %{SOURCE1} sedfaq.txt
gzip -9 sedfaq.txt

#%check
#echo ====================TESTING=========================
#make check
#echo ====================TESTING END=====================

%install
rm -rf ${RPM_BUILD_ROOT}
make DESTDIR=$RPM_BUILD_ROOT install
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/charset.alias

#%find_lang %{name}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
# -f %{name}.lang
%defattr(-,root,root)
%doc BUGS NEWS THANKS README AUTHORS sedfaq.txt.gz COPYING COPYING.DOC
%{_bindir}/sed.exe
%{_infodir}/*.info*
%{_mandir}/man*/*
%{_datadir}/locale/*

%changelog
* Sat Jan 0 2012 yd
- initial unixroot build.
