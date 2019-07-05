Summary: A GNU collection of diff utilities
Name: diffutils
Version: 3.2
Release: 3%{?dist}
Group: Applications/Text
URL: http://www.gnu.org/software/diffutils/diffutils.html
Source: ftp://ftp.gnu.org/gnu/diffutils/diffutils-%{version}.tar.xz

Source1: cmp.1
Source2: diff.1
Source3: diff3.1
Source4: sdiff.1
Patch0: diffutils-os2.patch
Patch1: diffutils-cmp-s-empty.patch

License: GPLv2+
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Diffutils includes four utilities: diff, cmp, diff3 and sdiff. Diff
compares two files and shows the differences, line by line.  The cmp
command shows the offset and line numbers where two files differ, or
cmp can show the characters that differ between the two files.  The
diff3 command shows the differences between three files.  Diff3 can be
used when two people have made independent changes to a common
original; diff3 can produce a merged file that contains both sets of
changes and warnings about conflicts.  The sdiff command can be used
to merge two files interactively.

Install diffutils if you need to compare text files.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%setup -q
%patch0 -p1 -b .os2~
%patch1 -p1 -b .cmp-s

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
%configure \
   "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"
make PR_PROGRAM=%{_bindir}/pr %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

( cd $RPM_BUILD_ROOT
  gzip -9nf .%{_infodir}/diff*
  mkdir -p .%{_mandir}/man1
  for manpage in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4}
  do
    install -m 0644 ${manpage} .%{_mandir}/man1
  done
)

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/charset.alias

#%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT

%files
# -f %{name}.lang
%defattr(-,root,root)
%doc NEWS README
%{_bindir}/*.exe
%{_mandir}/*/*
%{_infodir}/diffutils.info*gz
%{_datadir}/locale/*

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg

%changelog
* Fri May 23 2014 yd
- r730, Force --binary and no --strip-trailing-cr on OS/2.
- r729, Fix broken --binary option on OS/2.

* Mon Jan 09 2012 yd
- do not build with -Zbin-files flag.

* Sun Jan 08 2012 yd
- initial unixroot build.
