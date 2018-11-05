# -*- coding: utf-8 -*-

Summary: A GNU stream text editor
Name: sed
Version: 4.5
Release: 2%{?dist}
License: GPLv3+
Group: Applications/Text
URL: http://sed.sourceforge.net/
Vendor: bww bitwise works GmbH
#scm_source github http://github.com/bitwiseworks/%{name}-os2 master-os2
%scm_source git E:/Trees/%{name}/git master-os2
Source1: http://sed.sourceforge.net/sedfaq.txt
BuildRequires: libc-devel, libcx-devel, automake, autoconf, gcc
BuildRequires: gettext-devel, gettext-common-devel
#BuildRequires: glibc-devel, libacl-devel
#BuildRequires: perl-Getopt-Long

#Provides: /bin/sed

#copylib
#Provides: bundled(gnulib)

%description
The sed (Stream EDitor) editor is a stream or batch (non-interactive)
editor.  Sed takes text as input, performs an operation or set of
operations on the text and outputs the modified text.  The operations
that sed performs (substitutions, deletions, insertions, etc.) can be
specified in a script file or from the command line.

%debug_package

%prep
%scm_setup
autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure --without-included-regex
# we need that until we have a later texinfo :(
touch ./doc/sed.info

make %{_smp_mflags}
install -m 644 -p %{SOURCE1} sedfaq.txt
gzip -9 sedfaq.txt

%check
echo ====================TESTING=========================
#make check
echo ====================TESTING END=====================

%install
rm -rf ${RPM_BUILD_ROOT}
# we need that until we have a later texinfo :(
touch ./doc/sed.info
make DESTDIR=$RPM_BUILD_ROOT install
rm -f ${RPM_BUILD_ROOT}/%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/charset.alias

# create a symlink to fullfill requires w/o .exe
ln -s %{_bindir}/%{name}.exe %{buildroot}%{_bindir}/sed

%find_lang %{name}

%files -f %{name}.lang
%{!?_licensedir:%global license %%doc}
%license COPYING 
%doc BUGS NEWS THANKS README AUTHORS sedfaq.txt.gz
%{_bindir}/sed
%{_bindir}/sed.exe
%{_infodir}/sed.info*
%{_mandir}/man1/sed.1*

%changelog
* Mon Oct 29 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.5-2
- remove all binary stuff, as it broke too much

* Sat Oct 27 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.5-1
- updated to vendor version 4.5

* Sun Jan 08 2012 yd
- fixed requirements.

* Sat Jan 07 2012 yd
- initial unixroot build.
