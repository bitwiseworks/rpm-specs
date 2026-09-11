Summary:    A GNU tool for automatically configuring source code
Name:       autoconf269
Version:    2.69
Release:    7%{?dist}
License:    GPLv2+ and GFDL
Group:      Development/Tools
URL:        http://www.gnu.org/software/autoconf/
BuildArch:  noarch
Vendor:     bww bitwise works GmbH

%if !0%{?os2_version}
Source:     http://ftpmirror.gnu.org/autoconf/autoconf-%{version}.tar.xz
%else
%scm_source github http://github.com/bitwiseworks/autoconf-os2 %{version}-os2-2
Patch0: autoconf269-1-texinfo-7.patch
%endif

# Define a private versioned prefix for this pinned downstream build
BuildRequires: rpm_macro(setup_alt_prefix)
%setup_alt_prefix %{name}

# Set Provides to satisfy autoconf = version-release dependencies
Provides:   autoconf = %{version}-%{release}

# m4 >= 1.4.6 is required, >= 1.4.13 is recommended:
BuildRequires:      m4 >= 1.4.13
Requires:           m4 >= 1.4.13
%if !0%{?os2_version}
BuildRequires:      emacs
%endif

%if 0%{?os2_version}
# for autoreconf & docs
BuildRequires: autoconf automake texinfo
%endif

%if !0%{?os2_version}
# for check only:
BuildRequires: automake libtool gcc-gfortran
%endif

%description
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
%setup -q
%else
%scm_setup
%patch0 -p1
%endif

%build
%if 0%{?os2_version}
# make sure configure is updated to properly support OS/2
autoreconf -fvi
%endif
%configure
# not parallel safe
make

%if !0%{?os2_version}
%check
# The following test is failing.
# 188: autotest.at:1195   parallel autotest and signal handling
# In test/autotest.at, under comment "Test PIPE", the exit code written
# to file "status" is 0.  Report mailed to bug-autoconf.
make check TESTSUITEFLAGS='-187 189-'
%endif

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=$RPM_BUILD_ROOT

rm -f $RPM_BUILD_ROOT%{_infodir}/dir

# Alternate autoconf needs PATH & INFOPATH overrides
%install_alt_prefix_activate PATH,INFOPATH
# Create _docdir since we need to own it because of doc entries in files
mkdir -p $RPM_BUILD_ROOT%{_docdir}

%clean
rm -rf ${RPM_BUILD_ROOT}

%files
%defattr(-,root,root,-)
%{_bindir}/*
%{_infodir}/autoconf.info*
# don't include standards.info, because it comes from binutils...
%exclude %{_infodir}/standards*
%{_datadir}/autoconf/
%if !0%{?os2_version}
%dir %{_datadir}/emacs/
%{_datadir}/emacs/site-lisp/
%endif
%{_mandir}/man1/*
%doc AUTHORS COPYING ChangeLog NEWS README THANKS TODO
# Alternate package activation script and ownership of used dirs (incl. _prefix)
%{_alt_prefix_activate}
%dir %{_prefix}
%dir %{_bindir}
%dir %{_infodir}
%dir %{_datadir}
%dir %{_mandir}
%dir %{_mandir}/man1
%dir %{_docdir}

%changelog
* Fri Sep 11 2026 Dmitrii Kuminov <coding@dmik.org> 2.69-7
- Provide pinned versioned package (/usr/alt/autoconf269) for compatibility.
- Add automake and texinfo to build requirements.
- Use /@unixroot/usr/bin/sh as [CONFIG_]SHELL by default if UNIXROOT is defined.

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
