# Note this .spec is borrowed from automake-1.14.1-4.fc21.src.rpm

%global api_version 1.14

%define pkg_docdir  %{_docdir}/%{name}-%{version}

Summary:    A GNU tool for automatically creating Makefiles
Name:       automake
Version:    %{api_version}.1
Release:    1%{?dist}

# docs ~> GFDL, sources ~> GPLv2+, mkinstalldirs ~> PD and install-sh ~> MIT
License:    GPLv2+ and GFDL and Public Domain and MIT

Group:      Development/Tools
#Source:     ftp://ftp.gnu.org/gnu/automake/automake-%{version}.tar.xz

%define svn_url     http://svn.netlabs.org/repos/ports/automake/trunk
%define svn_rev     755

Source: %{name}-%{version}-r%{svn_rev}.zip

URL:        http://www.gnu.org/software/automake/
Requires:   autoconf >= 2.65

BuildRequires:  autoconf >= 2.65
#BuildRequires:  automake <- needs to be reenabled on the next release
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
BuildArch:  noarch

# do not run "make check" by default
%bcond_with check

# for better tests coverage:
%if %{with check}
BuildRequires: libtool gettext-devel flex bison texinfo-tex texlive-dvips
BuildRequires: java-devel-openjdk gcc-gfortran
BuildRequires: dejagnu expect emacs imake python-docutils vala
BuildRequires: cscope ncompress sharutils help2man
BuildRequires: gcc-objc gcc-objc++
%if !0%{?rhel:1}
BuildRequires: python-virtualenv lzip
%endif
%endif

%description
Automake is a tool for automatically generating `Makefile.in'
files compliant with the GNU Coding Standards.

You should install Automake if you are developing software and would
like to use its ability to automatically generate GNU standard
Makefiles.

%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

# make sure configure is updated to properly support OS/2
bootstrap.sh

%build

# we don't have makeinfo yet; fake it (this will keep the old docs)
export MAKEINFO=:

%configure --docdir=%{pkg_docdir}

make V=0 %{?_smp_mflags}
cp m4/acdir/README README.aclocal
cp contrib/multilib/README README.multilib

%install
rm -rf ${RPM_BUILD_ROOT}
make install DESTDIR=%{buildroot}

# TODO: we use %docdir below instead of %doc because the latter will rm -f the doc directory
# before installing files into it which kills everything that was already installed there by
# make install (in this particular case - amhello-*.tar.gz. This was fixed in RPM 4.9.1
# so the workaround should be undone when we switch to it (currently we use 4.8.1).
cp -p AUTHORS README THANKS NEWS README.aclocal README.multilib COPYING* %{buildroot}/%{pkg_docdir}

%check
# %%global TESTS_FLAGS t/preproc-errmsg t/preproc-basics
%if %{with check}
make -k %{?_smp_mflags} check %{?TESTS_FLAGS: TESTS="%{TESTS_FLAGS}"} \
    || ( cat ./test-suite.log && false )
%endif

#%post
#/sbin/install-info %{_infodir}/automake.info.gz %{_infodir}/dir || :

#%preun
#if [ $1 = 0 ]; then
#    /sbin/install-info --delete %{_infodir}/automake.info.gz %{_infodir}/dir || :
#fi

%files
#%doc AUTHORS README THANKS NEWS README.aclocal README.multilib COPYING*
%docdir %{pkg_docdir}
%{pkg_docdir}/*
#%exclude %{_infodir}/dir
%exclude %{_datadir}/aclocal
%{_bindir}/*
%{_infodir}/*.info*
%{_datadir}/automake-%{api_version}
%{_datadir}/aclocal-%{api_version}
%{_mandir}/man1/*

%changelog
* Sat Aug 30 2014 Dmitriy Kuminov <coding@dmik.org> 1.14.1-1
- Initial package for version 1.14.1.
