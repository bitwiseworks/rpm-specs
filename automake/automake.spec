%global api_version 1.16

# run "make check" by default
%bcond_with check
# Run optional test
%bcond_with automake_enables_optional_test

# remove once %%configure is used instead of ./configure
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Summary:    A GNU tool for automatically creating Makefiles
Name:       automake
Version:    %{api_version}.1
Release:    1%{?dist}

# docs ~> GFDL, sources ~> GPLv2+, mkinstalldirs ~> PD and install-sh ~> MIT
License:    GPLv2+ and GFDL and Public Domain and MIT
Vendor:     bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

URL:        http://www.gnu.org/software/automake/
Requires:   autoconf >= 2.65

# requirements not detected automatically (#919810)
Requires:   perl(Thread::Queue)
Requires:   perl(threads)

BuildRequires:  autoconf >= 2.65
BuildRequires:  coreutils
BuildRequires:  findutils
BuildRequires:  help2man
BuildRequires:  make
BuildRequires:  perl-generators
#BuildRequires:  perl-interpreter
BuildRequires:  perl(Thread::Queue)
BuildRequires:  perl(threads)

BuildArch:  noarch


# for better tests coverage:
%if %{with check}
%if %{with automake_enables_optional_test}
BuildRequires: automake
BuildRequires: bison
BuildRequires: cscope
BuildRequires: dejagnu
BuildRequires: emacs
BuildRequires: expect
BuildRequires: flex
BuildRequires: gcc-gfortran
BuildRequires: gettext-devel
BuildRequires: java-devel-openjdk
BuildRequires: libtool
BuildRequires: ncompress
BuildRequires: sharutils
BuildREquires: texlive-dvips
BuildRequires: texinfo-tex
BuildRequires: vala
%if !0%{?rhel:1}
BuildRequires: gcc-objc
BuildRequires: gcc-objc++
BuildRequires: imake
BuildRequires: lzip
%endif
%endif
%endif

# remove bogus Automake perl dependencies and provides
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}^perl\\(Automake::
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}^perl\\(Automake::

%description
Automake is a tool for automatically generating `Makefile.in'
files compliant with the GNU Coding Standards.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles.


%prep
%scm_setup

# make sure configure is updated to properly support OS/2
bootstrap


%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure --docdir=%{_pkgdocdir}
make V=0 %{?_smp_mflags}
cp m4/acdir/README README.aclocal
cp contrib/multilib/README README.multilib


%install
%make_install


%check
# %%global TESTS_FLAGS t/preproc-errmsg t/preproc-basics
%if %{with check}
make -k %{?_smp_mflags} check %{?TESTS_FLAGS: TESTS="%{TESTS_FLAGS}"} \
    || ( cat ./test-suite.log && false )
%endif


%files
%license COPYING*
%doc AUTHORS README THANKS NEWS README.aclocal README.multilib
%doc %{_pkgdocdir}/amhello-1.0.tar.gz
%exclude %{_infodir}/dir
%exclude %{_datadir}/aclocal
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/automake-%{api_version}
%{_datadir}/aclocal-%{api_version}
%{_mandir}/man1/*

%changelog
* Mon Dec 2 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.16.1-1
- update to version 1.16.1
- cleanup the spec and use scm_ macros and friends

* Thu Feb 5 2015 Dmitriy Kuminov <coding@dmik.org> 1.14.1-3
- aclocal: Work around 32K program arguments size limit on OS/2.

* Wed Sep 3 2014 Dmitriy Kuminov <coding@dmik.org> 1.14.1-2
- Rebuild with autoconf 2.69-2.

* Sat Aug 30 2014 Dmitriy Kuminov <coding@dmik.org> 1.14.1-1
- Initial package for version 1.14.1.
