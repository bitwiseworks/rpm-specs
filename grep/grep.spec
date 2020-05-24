Summary: Pattern matching utilities
Name: grep
Version: 3.4
Release: 1%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/grep/
Group: Applications/Text

Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: gcc
BuildRequires: pcre-devel >= 3.9-10, texinfo, gettext
BuildRequires: autoconf automake
BuildRequires: libc-devel, libcx-devel
Provides: /@unixroot/usr/bin/grep
Provides: /@unixroot/usr/bin/fgrep
Provides: /@unixtoor/usr/bin/egrep

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
autoreconf -vfi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"

%global BUILD_FLAGS $RPM_OPT_FLAGS
	
# Currently gcc on ppc uses double-double arithmetic for long double and it
# does not conform to the IEEE floating-point standard. Thus force
# long double to be double and conformant.
%ifarch ppc ppc64
%global BUILD_FLAGS %{BUILD_FLAGS} -mlong-double-64
%endif

%configure --without-included-regex --disable-silent-rules \
  CFLAGS="%{BUILD_FLAGS}"
make %{?_smp_mflags}

%install
make %{?_smp_mflags} DESTDIR=$RPM_BUILD_ROOT install
gzip $RPM_BUILD_ROOT%{_infodir}/grep*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%find_lang %name

%check
#make check


%files -f %{name}.lang
%doc AUTHORS THANKS TODO NEWS README
%{!?_licensedir:%global license %%doc}
%license COPYING

%{_bindir}/*
%exclude %{_bindir}/*.dbg
%{_infodir}/*.info*.gz
%{_mandir}/*/*

%changelog
* Sun May 25 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.4-1
- fix a issue where closing a pipe didn't work and spit an error
- update to version 3.4

* Mon May 13 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.3-1
- case insensitive search in --include/--exclude options (ticket #208)
- update to version 3.3
- move source to github
- merge fedora spec with our spec

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
