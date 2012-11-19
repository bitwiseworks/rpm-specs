Summary: The GNU version of the awk text processing utility
Name: gawk
Version: 4.0.0
Release: 2%{?dist}

# Most of source files are licensed under GPLv3+,
# several files are GPL or LGPLv2.1+ licensed,
# gettext.h is LGPL and random.c is BSD licensed
License: GPLv3+ and GPL and LGPLv3+ and LGPL and BSD
Group: Applications/Text
URL: http://www.gnu.org/software/gawk/gawk.html
Source0: http://ftp.gnu.org/gnu/gawk/gawk-%{version}.tar.xz

Patch0: gawk-os2.patch

#BuildRequires: byacc

%description
The gawk package contains the GNU version of awk, a text processing
utility. Awk interprets a special-purpose programming language to do
quick and easy text pattern matching and reformatting jobs.

Install the gawk package if you need a text processing utility. Gawk is
considered to be a standard Linux tool for processing text.

%prep
%setup -q
%patch0 -p1 -b .os2~

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zhigh-mem -Zomf"
export LIBS="-lurpo -lmmap"
%configure \
   "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

#%check
#make check diffout

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=${RPM_BUILD_ROOT}

#mkdir -p $RPM_BUILD_ROOT%{_bindir}

ln -sf gawk.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/awk.1.gz
ln -sf gawk.exe $RPM_BUILD_ROOT%{_bindir}/awk
ln -sf gawk.exe $RPM_BUILD_ROOT%{_bindir}/gawk
#mv $RPM_BUILD_ROOT/bin/{p,i}gawk $RPM_BUILD_ROOT%{_bindir}

# remove %{version}* , when we are building a snapshot...
rm -f $RPM_BUILD_ROOT/bin/{,p}gawk-%{version}* $RPM_BUILD_ROOT%{_infodir}/dir

#%find_lang %name

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc README COPYING FUTURES LIMITATIONS NEWS
%doc README_d/README.multibyte README_d/README.tests POSIX.STD
%{_bindir}/*
%{_mandir}/man1/*
%{_infodir}/gawk.info*
%{_infodir}/gawkinet.info*
%{_libexecdir}/awk
%{_datadir}/awk
%{_datadir}/locale

%changelog
* Mon Nov 19 2012 yd
- Fix CRLF translation to CRCRLF (removed -Zbin-files).

* Wed Mar 21 2012 yd
- initial unixroot build.
