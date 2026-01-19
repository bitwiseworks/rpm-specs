# Note: this .spec is borrowed from http://pkgs.fedoraproject.org/cgit/rpms/git.git

# Pass --without docs to rpmbuild if you don't want the documentation
%bcond_without docs

# Pass --without tests to rpmbuild if you don't want to run the tests
%if !0%{?os2_version}
%bcond_without tests
%else
%bcond_with tests
%endif

%global gitexecdir          %{_libexecdir}/git-core

# Settings for Fedora
%if 0%{?fedora}
# linkchecker is not available on EL
%bcond_without              linkcheck
%else
%bcond_with                 linkcheck
%endif

# Settings for Fedora >= 38 and EL >= 10
%if 0%{?fedora} >= 38 || 0%{?rhel} >= 10 || 0%{?os2_version}
%bcond_with                 perl_modcompat
%else
%bcond_without              perl_modcompat
%endif

# Settings for Fedora and EL == 9
# In EL >= 10 docbook5-style-xsl, needed by asciidoctor, is unwanted package
%if 0%{?fedora} || 0%{?rhel} == 9
%bcond_without              asciidoctor
%else
%bcond_with                 asciidoctor
%endif

# Settings for Fedora and EL >= 8
%if 0%{?fedora} || 0%{?rhel} >= 8
%bcond_with                 python2
%bcond_without              python3
%global gitweb_httpd_conf   gitweb.conf
%global use_glibc_langpacks 1
%global use_perl_generators 1
%global use_perl_interpreter 1
%else
%bcond_without              python2
%bcond_with                 python3
%global build_cflags        %{build_cflags} -fPIC -std=gnu99
%global gitweb_httpd_conf   git.conf
%global use_glibc_langpacks 0
%global use_perl_generators 0
%global use_perl_interpreter 0
%endif

# Allow cvs subpackage to be toggled via --with/--without
# Disable cvs subpackage by default on EL >= 8
%if 0%{?rhel} >= 8
%bcond_with                 cvs
%else
%bcond_without              cvs
%endif

# Allow credential-libsecret subpackage to be toggled via --with/--without
%if !0%{?os2_version}
%bcond_without              libsecret
%else
%bcond_with                 libsecret
%endif

# Allow p4 subpackage to be toggled via --with/--without
# Disable p4 package by default on EL >= 10
%if 0%{?rhel} >= 10
%bcond_with                 p4
%else
%bcond_without              p4
%endif

# Hardening flags for EL-7
%if 0%{?rhel} == 7
%global _hardened_build     1
%endif

# Define %%bash_completions_dir for EL <= 9
%{?!bash_completions_dir:%global bash_completions_dir %{_datadir}/bash-completion/completions}

# Set path to the package-notes linker script
%global _package_note_file  %{_builddir}/%{name}-%{real_version}/.package_note-%{name}-%{version}-%{release}.%{_arch}.ld

Name:           git
Version:        2.50.1
Release:        1%{?dist}
Summary:        Fast Version Control System
License:        BSD-3-Clause AND GPL-2.0-only AND GPL-2.0-or-later AND LGPL-2.1-or-later AND MIT
URL:            https://git-scm.com/

%if !0%{?os2_version}
# Note: real_version must be defined _after_ Version
%global real_version %(echo %{version} | tr '~' '.')

# Adjust Source URL path for release candidates
%global rcpath  %(test "%{version}" = "%{real_version}" || echo testing/)

Source0:        https://www.kernel.org/pub/software/scm/git/%{rcpath}%{name}-%{real_version}.tar.xz
Source1:        https://www.kernel.org/pub/software/scm/git/%{rcpath}%{name}-%{real_version}.tar.sign

# Junio C Hamano's key is used to sign git releases, it can be found in the
# junio-gpg-pub tag within git.
#
# (Note that the tagged blob in git contains a version of the key with an
# expired signing subkey.  The subkey expiration has been extended on the
# public keyservers, but the blob in git has not been updated.)
#
# https://git.kernel.org/cgit/git/git.git/tag/?h=junio-gpg-pub
# https://git.kernel.org/cgit/git/git.git/blob/?h=junio-gpg-pub&id=7214aea37915ee2c4f6369eb9dea520aec7d855b
Source2:        gpgkey-junio.asc

# Local sources begin at 10 to allow for additional future upstream sources
Source11:       git.xinetd.in
Source12:       git-gui.desktop
Source13:       gitweb-httpd.conf
Source14:       gitweb.conf.in
Source15:       git@.service.in
Source16:       git.socket

# Script to print test failure output (used in %%check)
Source99:       print-failed-test-output

# https://bugzilla.redhat.com/490602
Patch0:         git-cvsimport-Ignore-cvsps-2.2b1-Branches-output.patch

# https://bugzilla.redhat.com/2114531
# tests: try harder to find open ports for apache, git, and svn
#
# https://github.com/tmzullinger/git/commit/aedeaaf788
Patch1:         0001-t-lib-httpd-try-harder-to-find-a-port-for-apache.patch
# https://github.com/tmzullinger/git/commit/16750d024c
Patch2:         0002-t-lib-git-daemon-try-harder-to-find-a-port.patch
# https://github.com/tmzullinger/git/commit/aa5105dc11
Patch3:         0003-t-lib-git-svn-try-harder-to-find-a-port.patch

# Configurates Apache test server to use `DavLockDBType sdbm`
# Prevents t5540 failures on i686, s390x and ppc64le
Patch5:         git-test-apache-davlockdbtype-config.patch

# Adds the option to sanitize sideband channel messages
# CVE-2024-52005 wasn't fixed by upstream. This patch adds the option to harden Git against it.
# The default behaviour of Git remains unchanged.
#
# https://github.com/gitgitgadget/git/pull/1853
Patch6:         git-2.49-sanitize-sideband-channel-messages.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
#scm_source     git e:/trees/git/git master
Requires:       libc >= 0.1.14
Requires:       libcx >= 0.7.5
%endif

%if %{with docs}
# pod2man is needed to build Git.3pm
BuildRequires:  %{_bindir}/pod2man
%if %{with asciidoctor}
BuildRequires:  docbook5-style-xsl
BuildRequires:  rubygem-asciidoctor
%else
BuildRequires:  asciidoc >= 8.4.1
%endif
# endif with asciidoctor
BuildRequires:  perl(File::Compare)
BuildRequires:  xmlto
%if %{with linkcheck}
BuildRequires:  linkchecker
%endif
# endif with linkcheck
%endif
# endif with docs
BuildRequires:  coreutils
%if !0%{?os2_version}
BuildRequires:  desktop-file-utils
%endif
BuildRequires:  diffutils
%if 0%{?rhel} && 0%{?rhel} < 9
# Require epel-rpm-macros for the %%gpgverify macro on EL-7/EL-8, and
# %%build_cflags & %%build_ldflags on EL-7.
BuildRequires:  epel-rpm-macros
%endif
# endif rhel < 9
BuildRequires:  expat-devel
BuildRequires:  findutils
BuildRequires:  gawk
BuildRequires:  gcc
BuildRequires:  gettext
%if !0%{?os2_version}
BuildRequires:  glibc-utils
BuildRequires:  gnupg2
%endif
BuildRequires:  libcurl-devel
BuildRequires:  make
BuildRequires:  openssl-devel
BuildRequires:  pcre2-devel
BuildRequires:  perl(Error)
BuildRequires:  perl(lib)
BuildRequires:  perl(Test)
%if %{use_perl_generators}
BuildRequires:  perl-generators
%endif
# endif use_perl_generators
%if %{use_perl_interpreter}
BuildRequires:  perl-interpreter
%else
BuildRequires:  perl
%endif
# endif use_perl_interpreter
%if !0%{?os2_version}
BuildRequires:  pkgconfig(bash-completion)
%endif
BuildRequires:  sed
%if !0%{?os2_version}
%if 0%{?fedora} || 0%{?rhel} >= 8
BuildRequires:  systemd-rpm-macros
%else
BuildRequires:  systemd
%endif
%endif
BuildRequires:  tcl
%if !0%{?os2_version}
BuildRequires:  tk
%endif
BuildRequires:  xz
BuildRequires:  zlib-devel >= 1.2

%if %{with tests}
# Test suite requirements
BuildRequires:  acl
%if (0%{?fedora} && 0%{?fedora} < 40) || (0%{?rhel} >= 8 && 0%{?rhel} < 10)
# Needed by t5540-http-push-webdav.sh; recent httpd obviates this
BuildRequires: apr-util-bdb
%endif
%if 0%{?fedora} || 0%{?rhel} >= 8
# Needed by t5559-http-fetch-smart-http2.sh
BuildRequires: mod_http2
%endif
# endif fedora or rhel >= 8
BuildRequires:  bash
%if %{with cvs}
BuildRequires:  cvs
BuildRequires:  cvsps
%endif
# endif with cvs
%if %{use_glibc_langpacks}
# glibc-all-langpacks and glibc-langpack-is are needed for GETTEXT_LOCALE and
# GETTEXT_ISO_LOCALE test prereq's, glibc-langpack-en ensures en_US.UTF-8.
BuildRequires:  glibc-all-langpacks
BuildRequires:  glibc-langpack-en
BuildRequires:  glibc-langpack-is
%endif
# endif use_glibc_langpacks
%if 0%{?fedora} || 0%{?rhel} >= 9
BuildRequires:  gnupg2-smime
%endif
# endif fedora or el >= 9
%if 0%{?fedora} || ( 0%{?rhel} >= 7 && ( "%{_arch}" == "ppc64le" || "%{_arch}" == "x86_64" ) )
BuildRequires:  highlight
%endif
# endif fedora or el7+ (ppc64le/x86_64)
%if 0%{?fedora} >= 37
BuildRequires:  httpd-core
%else
BuildRequires:  httpd
%endif
# endif fedora >= 37
%if 0%{?fedora} && ! ( 0%{?fedora} >= 35 || "%{_arch}" == "i386" || "%{_arch}" == "s390x" )
BuildRequires:  jgit
%endif
# endif fedora (except i386 and s390x)
BuildRequires:  mod_dav_svn
BuildRequires:  openssh-clients
BuildRequires:  perl(App::Prove)
BuildRequires:  perl(CGI)
BuildRequires:  perl(CGI::Carp)
BuildRequires:  perl(CGI::Util)
BuildRequires:  perl(DBD::SQLite)
BuildRequires:  perl(Digest::MD5)
BuildRequires:  perl(Fcntl)
BuildRequires:  perl(File::Basename)
BuildRequires:  perl(File::Copy)
BuildRequires:  perl(File::Find)
BuildRequires:  perl(filetest)
BuildRequires:  perl(HTTP::Date)
BuildRequires:  perl(IO::Pty)
BuildRequires:  perl(JSON)
BuildRequires:  perl(JSON::PP)
BuildRequires:  perl(Mail::Address)
BuildRequires:  perl(Memoize)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Term::ReadLine)
BuildRequires:  perl(Test::More)
BuildRequires:  perl(Time::HiRes)
%if %{with python3}
BuildRequires:  python3-devel
%else
%if %{with python2}
BuildRequires:  python2-devel
%endif
# endif with python2
%endif
# endif with python3
BuildRequires:  subversion
BuildRequires:  subversion-perl
BuildRequires:  tar
BuildRequires:  time
BuildRequires:  zip
BuildRequires:  zstd
%endif
# endif with tests

%if 0%{?os2_version}
BuildRequires:  libc-devel >= 0.1.14
BuildRequires:  libcx-devel >= 0.7.5
%endif

Requires:       git-core = %{version}-%{release}
Requires:       git-core-doc = %{version}-%{release}
%if ! %{defined perl_bootstrap}
%if !0%{?os2_version}
Requires:       perl(Term::ReadKey)
%endif
%endif
# endif ! defined perl_bootstrap
Requires:       perl-Git = %{version}-%{release}

# Obsolete git-cvs if it's disabled
%if %{without cvs}
Obsoletes:      git-cvs < %{?epoch:%{epoch}:}%{version}-%{release}
%endif
# endif without cvs

# Obsolete git-p4 if it's disabled
%if %{without p4}
Obsoletes:      git-p4 < %{?epoch:%{epoch}:}%{version}-%{release}
%endif
# endif without p4

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs common set of tools which are usually using with
small amount of dependencies. To install all git packages, including
tools for integrating with other SCMs, install the git-all meta-package.

%package all
Summary:        Meta-package to pull in all git tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}
%if %{with libsecret}
Requires:       git-credential-libsecret = %{version}-%{release}
%endif
# endif with libsecret
%if %{with cvs}
Requires:       git-cvs = %{version}-%{release}
%endif
# endif with cvs
Requires:       git-daemon = %{version}-%{release}
%if !0%{?os2_version}
Requires:       git-email = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
%endif
%if %{with p4}
Requires:       git-p4 = %{version}-%{release}
%endif
# endif with p4
Requires:       git-subtree = %{version}-%{release}
%if !0%{?os2_version}
Requires:       git-svn = %{version}-%{release}
Requires:       git-instaweb = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
%endif
Requires:       perl-Git = %{version}-%{release}
%if ! %{defined perl_bootstrap}
%if !0%{?os2_version}
Requires:       perl(Term::ReadKey)
%endif
%endif
# endif ! defined perl_bootstrap
%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package core
Summary:        Core package of git with minimal functionality
Requires:       less
%if !0%{?os2_version}
Requires:       openssh-clients
%endif
Requires:       zlib >= 1.2
%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-core rpm installs really the core tools with minimal
dependencies. Install git package for common set of tools.
To install all git packages, including tools for integrating with
other SCMs, install the git-all meta-package.

%package core-doc
Summary:        Documentation files for git-core
BuildArch:      noarch
Requires:       git-core = %{version}-%{release}
%description core-doc
Documentation files for git-core package including man pages.

%if %{with libsecret}
%package credential-libsecret
Summary:        Git helper for accessing credentials via libsecret
BuildRequires:  libsecret-devel
Requires:       git = %{version}-%{release}
%description credential-libsecret
%{summary}.
%endif
# endif with libsecret

%if %{with cvs}
%package cvs
Summary:        Git tools for importing CVS repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       cvs
Requires:       cvsps
Requires:       perl(DBD::SQLite)
%description cvs
%{summary}.
%endif
# endif with cvs

%package daemon
Summary:        Git protocol daemon
Requires:       git-core = %{version}-%{release}
%if !0%{?os2_version}
%{?systemd_requires}
%endif
%description daemon
The git daemon for supporting git:// access to git repositories

%if !0%{?os2_version}
%package email
Summary:        Git tools for sending patches via email
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(Authen::SASL)
Requires:       perl(Cwd)
%if ! 0%{?rhel}
# RHEL lacks perl-Email-Valid (rhbz#2166718)
Requires:       perl(Email::Valid)
%endif
Requires:       perl(File::Spec)
Requires:       perl(File::Spec::Functions)
Requires:       perl(File::Temp)
Requires:       perl(IO::Socket::SSL)
Requires:       perl(Mail::Address)
Requires:       perl(MIME::Base64)
Requires:       perl(MIME::QuotedPrint)
Requires:       perl(Net::Domain)
Requires:       perl(Net::SMTP)
Requires:       perl(Net::SMTP::SSL)
Requires:       perl(POSIX)
Requires:       perl(Sys::Hostname)
Requires:       perl(Term::ANSIColor)
Requires:       perl(Term::ReadLine)
Requires:       perl(Text::ParseWords)
%description email
%{summary}.
%endif

%if !0%{?os2_version}
%package -n gitk
Summary:        Git repository browser
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
# Keep gitk on tcl/tk 8.x until its ready for 9 (also see below in config.mk)
# https://github.com/j6t/gitk/issues/5
Requires:       tk8 >= 8.4
%description -n gitk
%{summary}.
%endif

%if !0%{?os2_version}
%package -n gitweb
Summary:        Simple web interface to git repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
%description -n gitweb
%{summary}.
%endif

%if !0%{?os2_version}
%package gui
Summary:        Graphical interface to Git
BuildArch:      noarch
Requires:       gitk = %{version}-%{release}
Requires:       tk >= 8.4
%description gui
%{summary}.
%endif

%if !0%{?os2_version}
%package instaweb
Summary:        Repository browser in gitweb
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       gitweb = %{version}-%{release}
%if 0%{?rhel} >= 9
Requires:       httpd
%else
Requires:       lighttpd
%endif

%description instaweb
A simple script to set up gitweb and a web server for browsing the local
repository.
%endif

%if %{with p4}
%package p4
Summary:        Git tools for working with Perforce depots
BuildArch:      noarch
%if %{with python3}
BuildRequires:  python3-devel
%else
%if %{with python2}
BuildRequires:  python2-devel
%endif
# endif with python2
%endif
# endif with python3
Requires:       git = %{version}-%{release}
%description p4
%{summary}.
%endif
# endif with p4

%package -n perl-Git
Summary:        Perl interface to Git
BuildArch:      noarch
Requires:       git = %{version}-%{release}
%if %{with perl_modcompat}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif
%description -n perl-Git
%{summary}.

%package -n perl-Git-SVN
Summary:        Perl interface to Git::SVN
BuildArch:      noarch
Requires:       git = %{version}-%{release}
%if %{with perl_modcompat}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
%endif
%description -n perl-Git-SVN
%{summary}.

%package subtree
Summary:        Git tools to merge and split repositories
BuildArch:      noarch
Requires:       git-core = %{version}-%{release}
%description subtree
Git subtrees allow subprojects to be included within a subdirectory
of the main project, optionally including the subproject's entire
history.

%if !0%{?os2_version}
%package svn
Summary:        Git tools for interacting with Subversion repositories
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(Digest::MD5)
%if ! %{defined perl_bootstrap}
Requires:       perl(Term::ReadKey)
%endif
# endif ! defined perl_bootstrap
Requires:       subversion
%description svn
%{summary}.
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
# Verify GPG signatures
xz -dc '%{SOURCE0}' | %{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data=-

%autosetup -p1 -n %{name}-%{real_version}

# Install print-failed-test-output script
install -p -m 755 %{SOURCE99} print-failed-test-output
%else
%scm_setup
%endif

# Remove git-archimport
sed -i '/^SCRIPT_PERL += git-archimport\.perl$/d' Makefile
sed -i '/^git-archimport/d' command-list.txt
rm git-archimport.perl Documentation/git-archimport.adoc

%if %{without cvs}
# Remove git-cvs* from command list
sed -i '/^git-cvs/d' command-list.txt
%endif
# endif without cvs

%if %{without p4}
# Remove git-p4 from command list
sed -i '/^git-p4/d' command-list.txt
%endif
# endif without p4

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
# Pipe to tee to aid confirmation/verification of settings.
cat << \EOF | tee config.mak
V = 1
%if !0%{?os2_version}
CFLAGS = %{build_cflags}
LDFLAGS = %{build_ldflags}
%else
CFLAGS = %{optflags}
#LDFLAGS = %{build_ldflags}
%endif
USE_LIBPCRE = 1
ETC_GITCONFIG = %{_sysconfdir}/gitconfig
INSTALL_SYMLINKS = 1
GITWEB_PROJECTROOT = %{_localstatedir}/lib/git
GNU_ROFF = 1
NO_PERL_CPAN_FALLBACKS = 1
%if 0%{?rhel} && 0%{?rhel} < 8
NO_UNCOMPRESS2 = 1
%endif
%if %{with python3}
PYTHON_PATH = %{__python3}
%else
%if %{with python2}
PYTHON_PATH = %{__python2}
%else
NO_PYTHON = 1
%endif
%endif
%if %{with asciidoctor}
USE_ASCIIDOCTOR = 1
%endif
htmldir = %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
prefix = %{_prefix}
%if 0%{?os2_version}
# TODO: %{perl_vendorlib} is missing, see https://github.com/bitwiseworks/rpm-specs/issues/17
%global perl_vendorlib %{_prefix}/share/perl5/vendor_perl
%endif
perllibdir = %{perl_vendorlib}
gitwebdir = %{_localstatedir}/www/git

# Test options
DEFAULT_TEST_TARGET = prove
GIT_PROVE_OPTS = --verbose --normalize %{?_smp_mflags} --formatter=TAP::Formatter::File
GIT_TEST_OPTS = -x --verbose-log

# Keep gitk on tcl/tk 8.x until its ready for 9 (see more above in gitk requires)
TCLTK_PATH = wish8
TCL_PATH = tclsh8
EOF

# Filter bogus perl requires
# packed-refs comes from a comment in contrib/hooks/update-paranoid
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(packed-refs\\)
%if ! %{defined perl_bootstrap}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Term::ReadKey\\)
%endif
# endif ! defined perl_bootstrap

# Remove Git::LoadCPAN to ensure we use only system perl modules.  This also
# allows the dependencies to be automatically processed by rpm.
%if !0%{?os2_version}
rm -rf perl/Git/LoadCPAN{.pm,/}
%else
rm -rf perl/Git/LoadCPAN.pm perl/Git/LoadCPAN/
%endif
grep -rlZ '^use Git::LoadCPAN::' | xargs -r0 sed -i 's/Git::LoadCPAN:://g'

# Update gitweb default home link string
sed -i 's@"++GITWEB_HOME_LINK_STR++"@$ENV{"SERVER_NAME"} ? "git://" . $ENV{"SERVER_NAME"} : "projects"@' \
    gitweb/gitweb.perl

# Move contrib/{contacts,subtree} docs to Documentation so they build with the
# proper asciidoc/docbook/xmlto options
%if !0%{?os2_version}
mv contrib/{contacts,subtree}/git-*.adoc Documentation/
%else
mv contrib/contacts/git-*.adoc contrib/subtree/git-*.adoc Documentation/
%endif

%build
# Improve build reproducibility
export TZ=UTC
export SOURCE_DATE_EPOCH=$(date -r version +%%s 2>/dev/null)

%if !0%{?os2_version}
%make_build all %{?with_docs:doc}

%make_build -C contrib/contacts/ all
%else
make %{?_smp_mflags} all %{?with_docs:doc}

make %{?_smp_mflags} -C contrib/contacts/ all
%endif

%if %{with libsecret}
%make_build -C contrib/credential/libsecret/
%endif
# endif with libsecret

%if !0%{?os2_version}
%make_build -C contrib/credential/netrc/

%make_build -C contrib/diff-highlight/

%make_build -C contrib/subtree/ all
%else
make %{?_smp_mflags} -C contrib/credential/netrc/

make %{?_smp_mflags} -C contrib/diff-highlight/

make %{?_smp_mflags} -C contrib/subtree/ all
%endif

# Fix shebang in a few places to silence rpmlint complaints
%if %{with python2}
%if !0%{?os2_version}
sed -i -e '1s@#! */usr/bin/env python$@#!%{__python2}@' \
    contrib/fast-import/import-zips.py
%else
sed -i -e '1s@#! */usr/bin/env python$@#!/\@unixroot/usr/bin/python2@' \
    contrib/fast-import/import-zips.py
%endif
%else
# Remove contrib/fast-import/import-zips.py which requires python2.
rm -rf contrib/fast-import/import-zips.py
%endif
# endif with python2

%install
%make_install %{?with_docs:install-doc}

%make_install -C contrib/contacts

%if %{with libsecret}
install -pm 755 contrib/credential/libsecret/git-credential-libsecret \
    %{buildroot}%{gitexecdir}
%endif
# endif with libsecret
install -pm 755 contrib/credential/netrc/git-credential-netrc \
    %{buildroot}%{gitexecdir}
# temporarily move contrib/credential/netrc aside to prevent it from being
# deleted in the docs preparation, so the tests can be run in %%check
mv contrib/credential/netrc .

%make_install -C contrib/subtree

%if !0%{?os2_version}
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -pm 0644 %{SOURCE13} %{buildroot}%{_sysconfdir}/httpd/conf.d/%{gitweb_httpd_conf}
sed "s|@PROJECTROOT@|%{_localstatedir}/lib/git|g" \
    %{SOURCE14} > %{buildroot}%{_sysconfdir}/gitweb.conf
%endif

# install contrib/diff-highlight and clean up to avoid cruft in git-core-doc
install -Dpm 0755 contrib/diff-highlight/diff-highlight \
    %{buildroot}%{_datadir}/git-core/contrib/diff-highlight
%if !0%{?os2_version}
rm -rf contrib/diff-highlight/{Makefile,diff-highlight,*.perl,t}
%else
rm -rf contrib/diff-highlight/Makefile contrib/diff-highlight/diff-highlight contrib/diff-highlight/*.perl contrib/diff-highlight/t
%endif

# Remove contrib/persistent-https; a) this code requires compilation; and b) it
# is licensed differently than git
rm -rf contrib/persistent-https

# Remove contrib/scalar to avoid cruft in the git-core-doc docdir
rm -rf contrib/scalar

# Clean up contrib/subtree to avoid cruft in the git-core-doc docdir
%if !0%{?os2_version}
rm -rf contrib/subtree/{INSTALL,Makefile,git-subtree*,t}
%else
rm -rf contrib/subtree/INSTALL
rm -rf contrib/subtree/Makefile
rm -rf contrib/subtree/git-subtree*
rm -rf contrib/subtree/t
%endif

%if %{without cvs}
# Remove git-cvs* and gitcvs*
find %{buildroot} Documentation \( -type f -o -type l \) \
    \( -name 'git-cvs*' -o -name 'gitcvs*' \) -exec rm -f {} ';'
%endif
# endif without cvs

%if %{without p4}
# Remove git-p4* and mergetools/p4merge
find %{buildroot} Documentation -type f -name 'git-p4*' -exec rm -f {} ';'
rm -f %{buildroot}%{gitexecdir}/mergetools/p4merge
%endif
# endif without p4

# Remove unneeded git-remote-testsvn so git-svn can be noarch
%if !0%{?os2_version}
rm -f %{buildroot}%{gitexecdir}/git-remote-testsvn
%else
rm -f %{buildroot}%{gitexecdir}/git-remote-testsvn.exe
%endif

exclude_re="email|git-(citool|credential-libsecret|cvs|daemon|gui|instaweb|p4|subtree|svn)|gitk|gitweb|p4merge"
%if !0%{?os2_version}
(find %{buildroot}{%{_bindir},%{_libexecdir}} -type f -o -type l | grep -vE "$exclude_re" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}{%{_bindir},%{_libexecdir}} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e 's@^%{buildroot}@%dir @') >> bin-man-doc-files
%else
(find %{buildroot}%{_bindir} %{buildroot}%{_libexecdir} -type f -o -type l | grep -vE "$exclude_re" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}%{_bindir} %{buildroot}%{_libexecdir} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e 's@^%{buildroot}@%dir @') >> bin-man-doc-files
%endif
(find %{buildroot}%{perl_vendorlib} -type f | sed -e s@^%{buildroot}@@) > perl-git-files
(find %{buildroot}%{perl_vendorlib} -mindepth 1 -type d | sed -e 's@^%{buildroot}@%dir @') >> perl-git-files
# Split out Git::SVN files
grep Git/SVN perl-git-files > perl-git-svn-files
sed -i "/Git\/SVN/ d" perl-git-files
%if %{with docs}
(find %{buildroot}%{_mandir} -type f | grep -vE "$exclude_re|Git" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf %{buildroot}%{_mandir}
%endif
# endif with docs

mkdir -p %{buildroot}%{_localstatedir}/lib/git
%if !0%{?os2_version}
install -Dp -m 0644 %{SOURCE16} %{buildroot}%{_unitdir}/git.socket
perl -p \
    -e "s|\@GITEXECDIR\@|%{gitexecdir}|g;" \
    -e "s|\@BASE_PATH\@|%{_localstatedir}/lib/git|g;" \
    %{SOURCE15} > %{buildroot}%{_unitdir}/git@.service
%endif

# Setup bash completion
%if !0%{?os2_version}
install -Dpm 644 contrib/completion/git-completion.bash %{buildroot}%{bash_completions_dir}/git
ln -s git %{buildroot}%{bash_completions_dir}/gitk
%endif

# Install tcsh completion
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-completion.tcsh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# Move contrib/hooks out of %%docdir
mkdir -p %{buildroot}%{_datadir}/git-core/contrib
mv contrib/hooks %{buildroot}%{_datadir}/git-core/contrib
%if !0%{?os2_version}
pushd contrib > /dev/null
%else
cd contrib
%endif
ln -s ../../../git-core/contrib/hooks
%if !0%{?os2_version}
popd > /dev/null
%else
cd ..
%endif

# Install git-prompt.sh
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-prompt.sh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

%if !0%{?os2_version}
# install git-gui .desktop file
desktop-file-install --dir=%{buildroot}%{_datadir}/applications %{SOURCE12}
%endif

%if !0%{?os2_version}
# symlink git-citool to git-gui if they are identical
pushd %{buildroot}%{gitexecdir} >/dev/null
if cmp -s git-gui git-citool 2>/dev/null; then
    ln -svf git-gui git-citool
fi
popd >/dev/null
%endif

# find translations
%find_lang %{name} %{name}.lang
cat %{name}.lang >> bin-man-doc-files

# quiet some rpmlint complaints
chmod -R g-w %{buildroot}
chmod a-x %{buildroot}%{gitexecdir}/git-mergetool--lib
# These files probably are not needed
find . -regex '.*/\.\(git\(attributes\|ignore\)\|perlcriticrc\)' -delete
chmod a-x Documentation/technical/api-index.sh
find contrib -type f -print0 | xargs -r0 chmod -x

# Split core files
not_core_re="git-(add--interactive|contacts|credential-netrc|filter-branch|instaweb|request-pull|send-mail)|gitweb"
grep -vE "$not_core_re|%{_mandir}" bin-man-doc-files > bin-files-core
touch man-doc-files-core
%if %{with docs}
grep -vE "$not_core_re" bin-man-doc-files | grep "%{_mandir}" > man-doc-files-core
%endif
# endif with docs
grep -E  "$not_core_re" bin-man-doc-files > bin-man-doc-git-files

##### DOC
# place doc files into %%{_pkgdocdir} and split them into expected packages
# contrib
not_core_doc_re="(git-(cvs|gui|citool|daemon|instaweb|subtree))|p4|svn|email|gitk|gitweb"
mkdir -p %{buildroot}%{_pkgdocdir}/
cp -pr CODE_OF_CONDUCT.md README.md Documentation/*.adoc Documentation/RelNotes contrib %{buildroot}%{_pkgdocdir}/
# Remove contrib/ files/dirs which have nothing useful for documentation
%if !0%{?os2_version}
rm -rf %{buildroot}%{_pkgdocdir}/contrib/{contacts,credential}/
%else
rm -rf %{buildroot}%{_pkgdocdir}/contrib/contacts/ %{buildroot}%{_pkgdocdir}/contrib/credential/
%endif
%if !0%{?os2_version}
cp -p gitweb/INSTALL %{buildroot}%{_pkgdocdir}/INSTALL.gitweb
cp -p gitweb/README %{buildroot}%{_pkgdocdir}/README.gitweb
%endif

%if %{with docs}
cp -pr Documentation/*.html Documentation/docbook-xsl.css %{buildroot}%{_pkgdocdir}/
%if !0%{?os2_version}
cp -pr Documentation/{howto,technical} %{buildroot}%{_pkgdocdir}/
find %{buildroot}%{_pkgdocdir}/{howto,technical} -type f \
    |grep -o "%{_pkgdocdir}.*$" >> man-doc-files-core
%else
cp -pr Documentation/howto Documentation/technical %{buildroot}%{_pkgdocdir}/
find %{buildroot}%{_pkgdocdir}/howto %{buildroot}%{_pkgdocdir}/technical -type f \
    |grep -o "%{_pkgdocdir}.*$" >> man-doc-files-core
%endif
%endif
# endif with docs

{
    find %{buildroot}%{_pkgdocdir} -type f -maxdepth 1 \
        | grep -o "%{_pkgdocdir}.*$" \
        | grep -vE "$not_core_doc_re"
%if !0%{?os2_version}
    find %{buildroot}%{_pkgdocdir}/{contrib,RelNotes} -type f \
        | grep -o "%{_pkgdocdir}.*$"
%else
    find %{buildroot}%{_pkgdocdir}/contrib %{buildroot}%{_pkgdocdir}/RelNotes -type f \
        | grep -o "%{_pkgdocdir}.*$"
%endif
    find %{buildroot}%{_pkgdocdir} -type d | grep -o "%{_pkgdocdir}.*$" \
        | sed "s/^/\%dir /"
} >> man-doc-files-core
##### #DOC

%if 0%{?os2_version}
# Remove non-packed stuff
rm -rf %{buildroot}%{gitexecdir}/git-svn
rm -rf %{buildroot}%{gitexecdir}/git-instaweb
rm -rf %{buildroot}%{gitexecdir}/git-send-email
rm -rf %{buildroot}%{_mandir}/man1/git-instaweb.1*
rm -rf %{buildroot}%{_mandir}/man1/git-svn.1*
rm -rf %{buildroot}%{_mandir}/man1/git-gui.1*
rm -rf %{buildroot}%{_mandir}/man1/git-citool.1*
rm -rf %{buildroot}%{_mandir}/man1/gitweb.1*
rm -rf %{buildroot}%{_mandir}/man5/gitweb.conf.5*
rm -rf %{buildroot}%{_mandir}/man1/gitk.1*
rm -rf %{buildroot}%{_mandir}/man1/git-send-email.1*
rm -rf %{buildroot}%{_pkgdocdir}/git-gui.adoc
rm -rf %{buildroot}%{_pkgdocdir}/git-gui.html
rm -rf %{buildroot}%{_pkgdocdir}/git-citool.adoc
rm -rf %{buildroot}%{_pkgdocdir}/git-citool.html
rm -rf %{buildroot}%{_pkgdocdir}/git-instaweb.adoc
rm -rf %{buildroot}%{_pkgdocdir}/git-instaweb.html
rm -rf %{buildroot}%{_pkgdocdir}/git-send-email.adoc
rm -rf %{buildroot}%{_pkgdocdir}/git-send-email.html
rm -rf %{buildroot}%{_pkgdocdir}/git-svn.adoc
rm -rf %{buildroot}%{_pkgdocdir}/git-svn.html
rm -rf %{buildroot}%{_pkgdocdir}/gitk.adoc
rm -rf %{buildroot}%{_pkgdocdir}/gitk.html
rm -rf %{buildroot}%{_pkgdocdir}/gitweb*.adoc
rm -rf %{buildroot}%{_pkgdocdir}/gitweb*.html
rm -rf %{buildroot}%{_localstatedir}/www/git
rm -rf %{buildroot}%{bash_completions_dir}/git
%endif

%check
%if %{without tests}
echo "*** Skipping tests"
exit 0
%endif
# endif without tests

%if %{with docs} && %{with linkcheck}
# Test links in HTML documentation
find %{buildroot}%{_pkgdocdir} -name "*.html" -print0 | xargs -r0 linkchecker
%endif
# endif with docs && with linkcheck

# Tests to skip on all releases and architectures
#
# t5559-http-fetch-smart-http2 runs t5551-http-fetch-smart with
# HTTP_PROTO=HTTP/2.  Unfortunately, it fails quite regularly.
# https://lore.kernel.org/git/Y4fUntdlc1mqwad5@pobox.com/
GIT_SKIP_TESTS="t5559"

%if 0%{?rhel} && 0%{?rhel} < 8
# Skip tests which require mod_http2 on el7
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t5559"
%endif
# endif rhel < 8

%ifarch aarch64 %{arm} %{power64}
# Skip tests which fail on aarch64, arm, and ppc
#
# The following 2 tests use run_with_limited_cmdline, which calls ulimit -s 128
# to limit the maximum stack size.
# t5541.36 'push 2000 tags over http'
# t5551.25 'clone the 2,000 tag repo to check OS command line overflow'
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t5541.37 t5551.25"
%endif
# endif aarch64 %%{arm} %%{power64}

%if 0%{?rhel} == 8 && "%{_arch}" == "s390x"
# Skip tests which fail on s390x on rhel-8
#
# The following tests fail on s390x & el8.  The cause should be investigated.
# However, it's a lower priority since the same tests work consistently on
# s390x with Fedora and RHEL-9.  The failures seem to originate in t5300.
#
# t5300.10 'unpack without delta'
# t5300.12 'unpack with REF_DELTA'
# t5300.13 'unpack with REF_DELTA'
# t5300.14 'unpack with OFS_DELTA'
# t5300.18 'compare delta flavors'
# t5300.20 'use packed deltified (REF_DELTA) objects'
# t5300.23 'verify pack'
# t5300.24 'verify pack -v'
# t5300.25 'verify-pack catches mismatched .idx and .pack files'
# t5300.29 'verify-pack catches a corrupted sum of the index file itself'
# t5300.30 'build pack index for an existing pack'
# t5300.45 'make sure index-pack detects the SHA1 collision'
# t5300.46 'make sure index-pack detects the SHA1 collision (large blobs)'
# t5303.5  'create corruption in data of first object'
# t5303.7  '... and loose copy of second object allows for partial recovery'
# t5303.11 'create corruption in data of first delta'
# t6300.35 'basic atom: head objectsize:disk'
# t6300.91 'basic atom: tag objectsize:disk'
# t6300.92 'basic atom: tag *objectsize:disk'
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t5300.1[02348] t5300.2[03459] t5300.30 t5300.4[56] t5303.[57] t5303.11 t6300.35 t6300.9[12]"
%endif
# endif rhel == 8 && arch == s390x

%if "%{_arch}" == "s390x"
# Skip tests which fail on s390x
#
# The following tests are failing on s390x.
# https://lore.kernel.org/git/Z8dIZmscTdi8dZAY@teonanacatl.net/
#
# t5620.4 'do partial clone 2, backfill min batch size'
GIT_SKIP_TESTS="$GIT_SKIP_TESTS t5620.4"
%endif
# endif "%{_arch}" == "s390x"
export GIT_SKIP_TESTS

# Set LANG so various UTF-8 tests are run
export LANG=en_US.UTF-8

# Explicitly enable tests which may be skipped opportunistically
# Check for variables set via test_bool_env in the test suite:
#   git grep 'test_bool_env GIT_' -- t/{lib-,t[0-9]}*.sh |
#       sed -r 's/.* (GIT_[^ ]+) .*/\1/g' | sort -u
export GIT_TEST_GIT_DAEMON=true
export GIT_TEST_HTTPD=true
export GIT_TEST_SVNSERVE=true
export GIT_TEST_SVN_HTTPD=true

# Create tmpdir for test output and update GIT_TEST_OPTS
# Also update GIT-BUILD-OPTIONS to keep make from any needless rebuilding
export testdir=$(mktemp -d -p /tmp git-t.XXXX)
sed -i "s@^GIT_TEST_OPTS = .*@& --root=$testdir@" config.mak
touch -r GIT-BUILD-OPTIONS ts
sed -i "s@\(GIT_TEST_OPTS='.*\)'@\1 --root=$testdir'@" GIT-BUILD-OPTIONS
touch -r ts GIT-BUILD-OPTIONS

# Run the tests
%__make -C t all || ./print-failed-test-output

# Run contrib/credential/netrc tests
mkdir -p contrib/credential
mv netrc contrib/credential/
%make_build -C contrib/credential/netrc/ test || \
%make_build -C contrib/credential/netrc/ testverbose

# Clean up test dir
rmdir --ignore-fail-on-non-empty "$testdir"

%if !0%{?os2_version}
%post daemon
%systemd_post git.socket
%endif

%if !0%{?os2_version}
%preun daemon
%systemd_preun git.socket
%endif

%if !0%{?os2_version}
%postun daemon
%systemd_postun_with_restart git.socket
%endif

%files -f bin-man-doc-git-files
%{_datadir}/git-core/contrib/diff-highlight
%{_datadir}/git-core/contrib/hooks/update-paranoid
%{_datadir}/git-core/contrib/hooks/setgitperms.perl
%{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%{_datadir}/git-core/templates/hooks/pre-rebase.sample
%{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample

%files all
# No files for you!

%files core -f bin-files-core
#NOTE: this is only use of the %%doc macro in this spec file and should not
#      be used elsewhere
%{!?_licensedir:%global license %doc}
%license COPYING
# exclude is best way here because of troubles with symlinks inside git-core/
%exclude %{_datadir}/git-core/contrib/diff-highlight
%exclude %{_datadir}/git-core/contrib/hooks/update-paranoid
%exclude %{_datadir}/git-core/contrib/hooks/setgitperms.perl
%exclude %{_datadir}/git-core/templates/hooks/fsmonitor-watchman.sample
%exclude %{_datadir}/git-core/templates/hooks/pre-rebase.sample
%exclude %{_datadir}/git-core/templates/hooks/prepare-commit-msg.sample
%if !0%{?os2_version}
%{bash_completions_dir}/git
%endif
%{_datadir}/git-core/

%files core-doc -f man-doc-files-core
%if 0%{?rhel} && 0%{?rhel} <= 7
# .py files are only bytecompiled on EL <= 7
%exclude %{_pkgdocdir}/contrib/*/*.py[co]
%endif
# endif rhel <= 7
%{_pkgdocdir}/contrib/hooks

%if %{with libsecret}
%files credential-libsecret
%{gitexecdir}/git-credential-libsecret
%endif
# endif with libsecret

%if %{with cvs}
%files cvs
%{_pkgdocdir}/*git-cvs*.adoc
%{_bindir}/git-cvsserver
%{gitexecdir}/*cvs*
%{?with_docs:%{_mandir}/man1/*cvs*.1*}
%{?with_docs:%{_pkgdocdir}/*git-cvs*.html}
%endif
# endif with cvs

%files daemon
%{_pkgdocdir}/git-daemon*.adoc
%if !0%{?os2_version}
%{_unitdir}/git.socket
%config(noreplace) %{_unitdir}/git@.service
%{gitexecdir}/git-daemon
%else
%{gitexecdir}/git-daemon.exe
%endif
%{_localstatedir}/lib/git
%{?with_docs:%{_mandir}/man1/git-daemon*.1*}
%{?with_docs:%{_pkgdocdir}/git-daemon*.html}

%if !0%{?os2_version}
%files email
%{_pkgdocdir}/*email*.adoc
%{gitexecdir}/*email*
%if 0%{?os2_version}
%exclude %{gitexecdir}/*.dbg
%endif
%{?with_docs:%{_mandir}/man1/*email*.1*}
%{?with_docs:%{_pkgdocdir}/*email*.html}
%endif

%if !0%{?os2_version}
%files -n gitk
%{_pkgdocdir}/*gitk*.adoc
%{_bindir}/*gitk*
%{_datadir}/gitk
%{?with_docs:%{_mandir}/man1/*gitk*.1*}
%{?with_docs:%{_pkgdocdir}/*gitk*.html}
%endif

%if !0%{?os2_version}
%files -n gitweb
%{_pkgdocdir}/*.gitweb
%{_pkgdocdir}/gitweb*.adoc
%{?with_docs:%{_mandir}/man1/gitweb.1*}
%{?with_docs:%{_mandir}/man5/gitweb.conf.5*}
%{?with_docs:%{_pkgdocdir}/gitweb*.html}
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/%{gitweb_httpd_conf}
%{_localstatedir}/www/git/
%endif

%if !0%{?os2_version}
%files gui
%{gitexecdir}/git-gui*
%{gitexecdir}/git-citool
%{_datadir}/applications/*git-gui.desktop
%{_datadir}/git-gui/
%{_pkgdocdir}/git-gui.adoc
%{_pkgdocdir}/git-citool.adoc
%{?with_docs:%{_mandir}/man1/git-gui.1*}
%{?with_docs:%{_pkgdocdir}/git-gui.html}
%{?with_docs:%{_mandir}/man1/git-citool.1*}
%{?with_docs:%{_pkgdocdir}/git-citool.html}
%endif

%if !0%{?os2_version}
%files instaweb
%{gitexecdir}/git-instaweb
%{_pkgdocdir}/git-instaweb.adoc
%{?with_docs:%{_mandir}/man1/git-instaweb.1*}
%{?with_docs:%{_pkgdocdir}/git-instaweb.html}
%endif

%if %{with p4}
%files p4
%{gitexecdir}/*p4*
%{gitexecdir}/mergetools/p4merge
%if !0%{?os2_version}
%exclude %{gitexecdir}/*.dbg
%endif
%{_pkgdocdir}/*p4*.adoc
%{?with_docs:%{_mandir}/man1/*p4*.1*}
%{?with_docs:%{_pkgdocdir}/*p4*.html}
%endif
# endif with p4

%files -n perl-Git -f perl-git-files
%{?with_docs:%{_mandir}/man3/Git.3pm*}

%files -n perl-Git-SVN -f perl-git-svn-files

%files subtree
%{gitexecdir}/git-subtree
%{_pkgdocdir}/git-subtree.adoc
%{?with_docs:%{_mandir}/man1/git-subtree.1*}
%{?with_docs:%{_pkgdocdir}/git-subtree.html}

%if !0%{?os2_version}
%files svn
%{gitexecdir}/git-svn
%{_pkgdocdir}/git-svn.adoc
%{?with_docs:%{_mandir}/man1/git-svn.1*}
%{?with_docs:%{_pkgdocdir}/git-svn.html}
%endif

%changelog
* Sun Jan 11 2026 Dmitrii Kuminov <coding@dmik.org> 2.50.1-1
- Update git to version 2.50.1.
- Synchronize spec with Fedora for git 2.50.1.
- Requilre LIBCn >= 0.1.14 due to arc4random_buf and new includes.
- Requilre LIBCx >= 0.7.5 due to spawn2 fixes.

* Wed Dec 01 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.30.2-2
- disable email, as we lack still some perl stuff

* Thu Oct 14 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.30.2-1
- update to version 2.32.2
- resync spec with fedora spec

* Mon Jan 14 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.11.0-4
- build with latest tools to overcome a dbg file creation issue (ticket #193)
- fix git-all rpm (rpm ticket #327)

* Mon Jun 4 2018 Dmitriy Kuminov <coding@dmik.org> 2.11.0-3
- Make updated file locking fully work on OS/2 (no more chmod errors).
- Forbid inheriting O_CLOEXEC (e.g. temporary) files on OS/2.

* Thu Apr 6 2017 Dmitriy Kuminov <coding@dmik.org> 2.11.0-2
- Make git add --interactive output use CRLFs on DOS-like platforms.
- Remove a lot of outdated OS/2-specific code.
- Make the .git directory truly hidden on OS/2.
- Enable mmap support on OS/2.
- Change vendor to bww bitwise works GmbH.

* Tue Dec 13 2016 Dmitriy Kuminov <coding@dmik.org> 2.11.0-1
- Update git to version 2.11.0.
- Increase stack size to 8 MB to fix crashes when cloning huge repos.
- Link against LIBCx 0.4 (this brings EXCEPTQ TRP report generator).
- Rebuild against LIBC 0.6.6 and GCC 4.9.2.
- Enable %lang definitions.

* Wed Sep 10 2014 yd
- added debug package with symbolic info for exceptq.

* Wed Sep 10 2014 Dmitriy Kuminov <coding@dmik.org> 2.0.0-1
- Update git to version 2.0.0.
- Fix cloning and pushing over HTTP(S).
- Remove many old unneeded patches to have less OS/2-dependent code.

* Sat Dec 17 2011 yd
- rebuild due to gcc 4.4.6 bug.

* Sun Nov 27 2011 yd
- use /@unixroot/usr/bin shell.

* Wed Sep 28 2011 yd
- fixed build patches.
- fixed expat support.

* Sat Sep 24 2011 yd
- symlink script files to exe, so execvp can find them.
- ignore CR while reading CRLF terminated text files.

* Tue Sep 20 2011 yd
- disable broken_path_fix macro.

* Mon Sep 19 2011 yd
- use bigger stack for threads; use socketpair instead of pipes.
