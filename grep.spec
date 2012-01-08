#%define _bindir /bin

Summary: Pattern matching utilities
Name: grep
Version: 2.10
Release: 1%{?dist}
License: GPLv3+
Group: Applications/Text
Source: ftp://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.xz
Patch0: grep-os2.patch

URL: http://www.gnu.org/software/grep/

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires: pcre-devel >= 3.9-10, gettext
#BuildRequires: texinfo
#BuildRequires: autoconf automake

%description
The GNU versions of commonly used grep utilities. Grep searches through
textual input for lines which contain a match to a specified pattern and then
prints the matching lines. GNU's grep utilities include grep, egrep and fgrep.

GNU grep is needed by many scripts, so it shall be installed on every system.

%prep
%setup -q
%patch0 -p1

%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
export CPPFLAGS="-I%{_includedir}/pcre"
%configure \
    --without-included-regex \
   "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install
gzip $RPM_BUILD_ROOT%{_infodir}/grep*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
rm -f $RPM_BUILD_ROOT/%{_libdir}/charset.alias

#%find_lang %name

#%check
#make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
# -f %{name}.lang
%defattr(-,root,root)
%doc ABOUT-NLS AUTHORS THANKS TODO NEWS README ChangeLog COPYING
%{_bindir}/*
%{_infodir}/*.info*.gz
%{_mandir}/*/*
%{_datadir}/locale/*

%changelog
* Sun Jan 08 2012 yd
- initial unixroot build.
