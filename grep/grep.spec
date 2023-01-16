Summary: Pattern matching utilities
Name: grep
Version: 3.8
Release: 1%{?dist}
License: GPLv3+
URL: https://www.gnu.org/software/grep/

%if !0%{?os2_version}
Source: https://ftp.gnu.org/pub/gnu/grep/grep-%{version}.tar.xz
Source1: colorgrep.sh
Source2: colorgrep.csh
Source3: GREP_COLORS
Source4: grepconf.sh
# upstream ticket 39445
Patch0: grep-3.5-help-align.patch
Patch1: grep-configure-c99.patch
%else
Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires: gcc
BuildRequires: pcre2-devel
BuildRequires: texinfo
BuildRequires: gettext
BuildRequires: autoconf
BuildRequires: automake
%if !0%{?os2_version}
Buildrequires: glibc-all-langpacks
%else
BuildRequires: libc-devel
BuildRequires: libcx-devel
%endif
BuildRequires: perl(FileHandle)
BuildRequires: make
%if !0%{?os2_version}
BuildRequires: libsigsegv-devel
# https://fedorahosted.org/fpc/ticket/174
Provides: bundled(gnulib)
# for backward compatibility (rhbz#1540485)
Provides: /bin/grep
Provides: /bin/fgrep
Provides: /bin/egrep
%else
Provides: /@unixroot/usr/bin/grep
Provides: /@unixroot/usr/bin/fgrep
Provides: /@unixtoor/usr/bin/egrep
%endif

%description
The GNU versions of commonly used grep utilities. Grep searches through
textual input for lines which contain a match to a specified pattern and then
prints the matching lines. GNU's grep utilities include grep, egrep and fgrep.

GNU grep is needed by many scripts, so it shall be installed on every system.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif

%build
# we do autoreconf even fedora doesn't do it
%if 0%{?os2_version}
autoreconf -vfi
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%endif

%global BUILD_FLAGS $RPM_OPT_FLAGS

# Currently gcc on ppc uses double-double arithmetic for long double and it
# does not conform to the IEEE floating-point standard. Thus force
# long double to be double and conformant.
%ifarch ppc ppc64
%global BUILD_FLAGS %{BUILD_FLAGS} -mlong-double-64
%endif

# Temporarily switch to the included regex until glibc bug is fixed:
# https://sourceware.org/bugzilla/show_bug.cgi?id=11053
#%%configure --without-included-regex --disable-silent-rules \
%configure --disable-silent-rules \
  CPPFLAGS="-I%{_includedir}/pcre" CFLAGS="%{BUILD_FLAGS}"
%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install
gzip $RPM_BUILD_ROOT%{_infodir}/grep*
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%if !0%{?os2_version}
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE1} %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -pm 644 %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}
install -Dpm 755 %{SOURCE4} $RPM_BUILD_ROOT%{_libexecdir}/grepconf.sh
%endif

%find_lang %name

%check
%if !0%{?os2_version}
make check
%endif

%files -f %{name}.lang
%doc AUTHORS THANKS TODO NEWS README
%license COPYING

%{_bindir}/*
%if !0%{?os2_version}
%config(noreplace) %{_sysconfdir}/profile.d/colorgrep.*sh
%config(noreplace) %{_sysconfdir}/GREP_COLORS
%else
%exclude %{_bindir}/*.dbg
%endif
%{_infodir}/*.info*.gz
%{_mandir}/*/*
%if !0%{?os2_version}
%{_libexecdir}/grepconf.sh
%endif

%changelog
* Mon Jan 16 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.8-1
- update to version 3.8
- sync with latest fedora spec

* Mon May 25 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.4-1
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
