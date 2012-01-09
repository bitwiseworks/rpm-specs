Summary: Utility for modifying/upgrading files
Name: patch
Version: 2.6.1
Release: 3%{?dist}
License: GPLv2+
URL: http://www.gnu.org/software/patch/patch.html
Group: Development/Tools

Source: ftp://ftp.gnu.org/gnu/patch/patch-%{version}.tar.gz
Patch1: patch-2.6.1-os2.diff
#Patch2: patch-get-arg.patch
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires: libselinux-devel
#BuildRequires: ed

%description
The patch program applies diff files to originals.  The diff command
is used to compare an original to a changed file.  Diff lists the
changes made to the file.  A person who has the original file can then
use the patch command with the diff file to add the changes to their
original file (patching the file).

Patch should be installed because it is a common way of upgrading
applications.

%prep
%setup -q
# apply os2 patch
%patch1 -p1 -b .os2~

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE"
export LDFLAGS="-Zhigh-mem -Zomf -Zexe -Zargs-wild -Zargs-resp"
%configure \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING NEWS README
%{_bindir}/*
%{_mandir}/*/*

%changelog
* Mon Jan 09 2012 yd
- fixed binary/text access.
