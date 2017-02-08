Summary: Pattern matching utilities
Name: grep
Version: 2.28
Release: 1%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/grep/
Group: Applications/Text

Vendor:  bww bitwise works GmbH
%scm_source  svn http://svn.netlabs.org/repos/ports/grep/trunk 1992

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
%scm_setup

%build
# we do autoreconf even fedora doesn't do it
autoreconf -fi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
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
if [ -f %{_infodir}/grep.info.gz ]; then
  %{_sbindir}/install-info.exe --quiet --info-dir=%{_infodir} %{_infodir}/grep.info.gz || :
fi

%preun
if [ $1 = 0 ]; then
  if [ -f %{_infodir}/grep.info.gz ]; then
    %{_sbindir}/install-info.exe --quiet --info-dir=%{_infodir} --delete %{_infodir}/grep.info.gz || :
  fi
fi

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
* Wed Feb 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.28-1
- update to version 2.28
- use new scm_source and scm_setup macros

* Tue Sep 13 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.25-2
- fix a sigabrt due to blindely source copy :(

* Mon Sep 12 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.25-1
- update to version 2.25

* Sun Jan 08 2012 yd
- initial unixroot build.
- fixed bindir value.
