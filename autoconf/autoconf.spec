# Run extended test
%bcond_without autoconf_enables_optional_test

# The design goal is to allow use of the same specfile on the original
# `autoconf` package and the `autoconf-latest` package by just changing the
# `Name` property.
# The `autoconf-latest` package aims to provide a versioned sub-package which
# enables the user to install different updates in parallel on long term
# releases. Hence, the versioned package installs its artifacts in
# `/opt/{namespace}/{versioned name}`.
Name:       autoconf
Version:    2.72
Release:    2%{?dist}

# To help future rebase, the following licenses were seen in the following files/folders:
# '*' is anything that was not explicitly listed earlier in the folder
# usr/bin/* - GPL-3.0-or-later
# usr/share/:
#  autoconf:
#    Autom4te:
#      {C4che.pm,General.pm,Getopt.pm,Request.pm}: GPL-3.0-or-later
#      * - GPL-2.0-or-later
#    autoconf:
#      * - GPL-3.0-or-later WITH Autoconf-exception-generic-3.0
#    autoscan/autoscan.list - GPL-3.0-or-later
#    autotest:
#      * - GPL-3.0-or-later WITH Autoconf-exception-3.0
#    build-aux:
#      config.{sub,guess} - GPL-3.0-or-later WITH Autoconf-exception-generic-3.0
#      install-sh - X11 AND LicenseRef-Fedora-Public-Domain
#    m4sugar:
#      {foreach.m4,m4sh.m4,m4sugar.m4} - GPL-3.0-or-later WITH Autoconf-exception-generic-3.0
#      * - None found
#    INSTALL - FSFAP
#    autom4te.cfg - GPL-3.0-or-later
#  doc/autoconf:
#    {AUTHORS,THANKS} - GPL-3.0-or-later
#    {README,TODO} - FSFAP
#    * - None found
#  emacs/site-lisp:
#    autoconf/*.el - GPL-3.0-or-later
#    * - None found
#  info/autoconf.info.gz/autoconf.info - GFDL-1.3-or-later
#  config.site - None found
# usr/share/man/man1/*: generated from usr/bin/* using help2man
#
# Note on Autoconf-exception{,-generic}-3.0, one is the license itself, the other is
# the text note that can be found in sources. That doesn't make sense to have 2 separate IDs
# but that's how it is.
License:    GPL-2.0-or-later AND GPL-3.0-or-later AND GPL-3.0-or-later WITH Autoconf-exception-generic-3.0 AND GFDL-1.3-or-later AND FSFAP AND X11 AND LicenseRef-Fedora-Public-Domain

%if !0%{?os2_version}
Source0:    https://ftp.gnu.org/gnu/autoconf/autoconf-%{version}.tar.xz
Source1:    config.site
Source2:    autoconf-init.el
%else
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2-1
Vendor:     bww bitwise works GmbH
%endif
URL:        https://www.gnu.org/software/autoconf/

%if !0%{?os2_version}
# From upstream 9ff9c567b1a7a7e66fa6523d4ceff142b86bddaa
Patch:      0001-Keep-lmingwex-and-lmoldname-in-linker-flags-for-MinG.patch
%endif

%if "%{name}" != "autoconf"
# Set this to the sub-package base name, for "autoconf-latest"
%global autoconf %(echo autoconf%{version} | tr -d .)
# Enforce use of system provided emacs support
%global autoconf_enables_emacs 0

%if 0%{?rhel} > 0
%global _prefix /opt/rh/%{autoconf}
%else
# We intentionally do not define a case for Fedora, as it should not
# need this functionality, and letting it error avoids accidents.
%{error:"Each downstream must specify its own /opt namespace"}
%endif
Summary:    Meta package to include latest version of autoconf
%else
#name == autoconf
# Enable Emacs support
%if !0%{?os2_version}
%bcond_without autoconf_enables_emacs
%else
%bcond_with autoconf_enables_emacs
%endif
%global autoconf %{name}
Summary:    A GNU tool for automatically configuring source code
Provides:   autoconf-latest = %{version}-%{release}
Provides:   %(echo autoconf%{version} | tr -d .) = %{version}-%{release}
%endif

BuildArch:  noarch


# run "make check" by default
%if !0%{?os2_version}
%bcond_without check
%else
%bcond_with check
%endif

# m4 >= 1.4.6 is required, >= 1.4.14 is recommended:
BuildRequires:      perl
Requires:           perl(File::Compare)
%if !0%{?os2_version}
Requires:           perl-interpreter
%else
Requires:           perl
%endif
BuildRequires:      m4 >= 1.4.14
Requires:           m4 >= 1.4.14
%if %{with autoconf_enables_emacs}
Requires:           emacs-filesystem
BuildRequires:      emacs
%endif
# the filtering macros are currently in /etc/rpm/macros.perl:
BuildRequires:      perl-generators
BuildRequires:      perl-macros
BuildRequires:      perl(Data::Dumper)
# from f19, Text::ParseWords is not the part of 'perl' package
BuildRequires:      perl(Text::ParseWords)

# %%configure replaces config.guess/config.sub for us, which confuses autoconf
# build system and it produces empty man pages for those scripts if help2man is
# not installed
BuildRequires:      help2man
BuildRequires:      make

%if %{with check}
%if %{with autoconf_enables_optional_test}
# For extended testsuite coverage
BuildRequires:      gcc-gfortran
%if 0%{?fedora} >= 15
BuildRequires:      erlang
%endif
%endif
%endif

%if 0%{?os2_version}
# for autoreconf
BuildRequires: autoconf
%endif

# filter out bogus perl(Autom4te*) dependencies
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Autom4te::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Autom4te::

%if "%{name}" != "autoconf"
# We're still on the autoconf-latest package
Requires: %{autoconf}
%description -n autoconf-latest
The latest GNU Autoconf, with a version-specific install
%files -n autoconf-latest

%package -n %{autoconf}
Summary: A GNU tool for automatically configuring source code
%endif

%description -n %{autoconf}
GNU's Autoconf is a tool for configuring source code and Makefiles.
Using Autoconf, programmers can create portable and configurable
packages, since the person building the package is allowed to
specify various configuration options.

You should install Autoconf if you are developing software and
would like to create shell scripts that configure your source code
packages. If you are installing Autoconf, you will also need to
install the GNU m4 package.

Note that the Autoconf package is not required for the end-user who
may be configuring software with an Autoconf-generated script;
Autoconf is only required for the generation of the scripts, not
their use.


%prep
%if !0%{?os2_version}
%autosetup -n autoconf-%{version} -p1
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
# make sure configure is updated to properly support OS/2
autoreconf -fvi
%endif

%if %{with autoconf_enables_emacs}
export EMACS=%{_bindir}/emacs
%else
export EMACS=%{_bindir}/false
%endif
%configure \
    %{?with_autoconf_enables_emacs:--with-lispdir=%{_emacs_sitelispdir}/autoconf}
%make_build


%check
%if %{with check}
# make check # TESTSUITEFLAGS='1-198 200-' # will disable nr. 199.
# make check TESTSUITEFLAGS="-k \!erlang"
case $(./build-aux/config.guess) in
  i?86-*-linux*)
    # Exclude test known to be failing on i686
    make check %{?_smp_mflags} TESTSUITEFLAGS="-k '!AC_SYS_LARGEFILE,!AC_SYS_YEAR2038,!AC_SYS_YEAR2038_RECOMMENDED'"
    # Execute these tests only, to keep record on the actual status
    make check TESTSUITEFLAGS="-k 'AC_SYS_LARGEFILE,AC_SYS_YEAR2038,AC_SYS_YEAR2038_RECOMMENDED'" %{?_smp_mflags} || true
    ;;
  *)
    make check %{?_smp_mflags}
    ;;
esac
%endif


%install
%make_install
mkdir -p %{buildroot}/share
%if !0%{?os2_version}
install -m 0644 %{SOURCE1} %{buildroot}%{_datadir}
%endif

%if %{with autoconf_enables_emacs}
# Create file to activate Emacs modes as required
mkdir -p %{buildroot}%{_emacs_sitestartdir}
install -p -m 0644 %{SOURCE2} %{buildroot}%{_emacs_sitestartdir}
%endif

%if "%{name}" != "autoconf"
install -d -m 755 ${RPM_BUILD_ROOT}/etc/scl/prefixes
dirname %{_prefix} > %{autoconf}.prefix
install -p -m 644 %{autoconf}.prefix ${RPM_BUILD_ROOT}/etc/scl/prefixes/%{autoconf}

echo "export PATH=%{_prefix}/bin:\$PATH" > enable.scl
install -p -m 755 enable.scl ${RPM_BUILD_ROOT}/%{_prefix}/enable
%endif

%files -n %{autoconf}
%license COPYING*
%{_bindir}/*
%{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
# don't include info's TOP directory
%exclude %{_infodir}/dir
%{_datadir}/autoconf/
%if !0%{?os2_version}
%{_datadir}/config.site
%endif
%if %{with autoconf_enables_emacs}
%{_datadir}/emacs/site-lisp/*
%endif
%{_mandir}/man1/*
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%if "%{name}" != "autoconf"
/etc/scl/prefixes/%{autoconf}
%{_prefix}/enable
%endif


%changelog
* Mon Feb 17 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.72-2
- fix some regressions

* Tue Feb 11 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.72-1
- update to version 2.72
- merge with fedora spec

* Wed Mar 24 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.69-6
- fix an annoying crash in print.com

* Fri May 12 2017 Dmitriy Kuminov <coding@dmik.org> 2.69-5
- Use scm_source and friends.
- Fix fatal failure in postun script (missing percent in macro).
- Support escaping and quoting in LDFLAGS and similar vars (#156).

* Wed Oct 19 2016 Dmitriy Kuminov <coding@dmik.org> 2.69-4
- Overcome 32k command line limit on OS/2 in autom4te.

* Tue Oct 18 2016 Dmitriy Kuminov <coding@dmik.org> 2.69-3
- Disable too strict MAP_FIXED test on OS/2. Note that in order to let autoconf
  detect mmap presense, LIBCx must be installed and used (LIBS="-lcx").
- Install documentation in INFO format.
- Rebuild against LIBC 0.6.6 and GCC 4.9.2.

* Wed Sep 3 2014 Dmitriy Kuminov <coding@dmik.org> 2.69-2
- Use /@unixroot in generated files instead of absolute paths to programs.

* Fri Aug 29 2014 Dmitriy Kuminov <coding@dmik.org> 2.69-1
- Update to version 2.69.
- Fix PATH_SEPARATOR misdetection.
- Remove annoying $ac_executable_extensions warning.
- Apply various fixes to improve OS/2 and kLIBC support.

* Wed Oct 26 2011 yd
- fixed m4 path
