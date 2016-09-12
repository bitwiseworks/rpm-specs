#define svn_url     e:/trees/grep/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/grep/trunk
%define svn_rev     1697

Summary: Pattern matching utilities
Name: grep
Version: 2.25
Release: 1%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/grep/
Group: Applications/Text

Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: pcre-devel >= 3.9-10, gettext
BuildRequires: texinfo
BuildRequires: autoconf automake

%description
The GNU versions of commonly used grep utilities. Grep searches through
textual input for lines which contain a match to a specified pattern and then
prints the matching lines. GNU's grep utilities include grep, egrep and fgrep.

GNU grep is needed by many scripts, so it shall be installed on every system.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
# we do autoreconf even fedora doesn't do it
autoreconf -fi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
%configure --without-included-regex --disable-silent-rules \
  CPPFLAGS="-I%{_includedir}/pcre"
make %{?_smp_mflags}

%install
rm -rf ${RPM_BUILD_ROOT}
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install
gzip $RPM_BUILD_ROOT%{_infodir}/grep*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %name

%check
#make check

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
#/sbin/install-info --quiet --info-dir=%{_infodir} %{_infodir}/grep.info.gz || :

%preun
#if [ $1 = 0 ]; then
#  /sbin/install-info --quiet --info-dir=%{_infodir} --delete %{_infodir}/grep.info.gz || :
#fi

%files -f %{name}.lang
%defattr(-,root,root)
%doc AUTHORS THANKS TODO NEWS
%{!?_licensedir:%global license %%doc}
%license COPYING

%{_bindir}/*
%exclude %{_bindir}/*.dbg
%{_infodir}/*.info*.gz
%{_mandir}/*/*

%changelog
* Mon Sep 12 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.25-1
- update to version 2.25

* Sun Jan 08 2012 yd
- initial unixroot build.
- fixed bindir value.
