# Note: this .spec is borrowed from help2man-1.46.4-1.fc22.src.rpm

# Supported build option:
#
# --with nls ... build this package with --enable-nls 

Name:           help2man
Summary:        Create simple man pages from --help output
Version:        1.46.4
Release:        1%{?dist}
Group:          Development/Tools
License:        GPLv3+
URL:            http://www.gnu.org/software/help2man
#Source:         ftp://ftp.gnu.org/gnu/help2man/help2man-%{version}.tar.xz

%define svn_url     http://svn.netlabs.org/repos/ports/help2man/trunk
%define svn_rev     980

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: gcc make subversion zip

%bcond_with nls

%{!?with_nls:BuildArch: noarch}

#BuildRequires:  texinfo
#BuildRequires:  perl(Getopt::Long)
#BuildRequires:  perl(POSIX)
#BuildRequires:  perl(Text::ParseWords)
#BuildRequires:  perl(Text::Tabs)
#BuildRequires:  perl(strict)
%{?with_nls:BuildRequires: perl(Locale::gettext) /usr/bin/msgfmt}
%{?with_nls:BuildRequires: perl(Encode)}
%{?with_nls:BuildRequires: perl(I18N::Langinfo)}

#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

# Create files necessary for configure
bootstrap.sh

%build
%configure --%{!?with_nls:disable}%{?with_nls:enable}-nls --libdir=%{_libdir}/help2man
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
# Disable install_l10n for now since it depends on Perl(Locale:gettext) which is missing ATM
#make install_l10n DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
#%find_lang %name --with-man

#%post
#/sbin/install-info %{_infodir}/help2man.info %{_infodir}/dir 2>/dev/null || :

#%preun
#if [ $1 -eq 0 ]; then
#  /sbin/install-info --delete %{_infodir}/help2man.info \
#    %{_infodir}/dir 2>/dev/null || :
#fi

# See above
#%files -f %name.lang
%files
%doc README NEWS THANKS COPYING
%{_bindir}/help2man
%{_infodir}/*
%{_mandir}/man1/*

%if %{with nls}
%{_libdir}/help2man
%endif

%changelog
* Tue Jan 20 2015 Dmitriy Kuminov <coding@dmik.org> 1.46.4-1
- Initial package for version 1.46.4.
