# Note: this .spec is borrowed from help2man-1.46.4-1.fc22.src.rpm

# Supported build option:
#
# --with nls ... build this package with --enable-nls 

Name:           help2man
Summary:        Create simple man pages from --help output
Version:        1.47.6
Release:        1%{?dist}
Group:          Development/Tools
License:        GPLv3+
URL:            http://www.gnu.org/software/help2man

%bcond_with nls

%{!?with_nls:BuildArch: noarch}

Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires:  perl-generators
BuildRequires:  perl(Getopt::Long)
BuildRequires:  perl(POSIX)
BuildRequires:  perl(Text::ParseWords)
BuildRequires:  perl(Text::Tabs)
BuildRequires:  perl(strict)
%{?with_nls:BuildRequires: perl(Locale::gettext) /@unixroot/usr/bin/msgfmt.exe}
%{?with_nls:BuildRequires: perl(Encode)}
%{?with_nls:BuildRequires: perl(I18N::Langinfo)}

Requires(post): %{_sbindir}/install-info.exe
Requires(preun): %{_sbindir}/install-info.exe

%description
help2man is a script to create simple man pages from the --help and
--version output of programs.

Since most GNU documentation is now in info format, this provides a
way to generate a placeholder man page pointing to that resource while
still providing some useful information.

%prep
%scm_setup

# Create files necessary for configure
autoreconf -fvi

%build
%configure --%{!?with_nls:disable}%{?with_nls:enable}-nls --libdir=%{_libdir}/help2man
make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
make install_l10n DESTDIR=$RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
%find_lang %name --with-man

%post
if [ -f %{_infodir}/help2man.info ]; then
    %{_sbindir}/install-info.exe %{_infodir}/help2man.info %{_infodir}/dir || :
fi

%preun
if [ $1 -eq 0 ]; then
    if [ -f %{_infodir}/help2man.info ]; then
        %{_sbindir}/install-info.exe --delete %{_infodir}/help2man.info %{_infodir}/dir || :
    fi
fi

%files -f %name.lang
%doc README NEWS THANKS
%license COPYING
%{_bindir}/help2man
%{_infodir}/*
%{_mandir}/man1/*

%if %{with nls}
%{_libdir}/help2man
%endif

%changelog
* Fri Dec 01 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.47.6-1
- update to vendor version 1.47.6
- use proper scm macros
- change the way we bootstrap

* Fri Feb 13 2015 Dmitriy Kuminov <coding@dmik.org> 1.46.4-2
- Enable proper info file and locale data installation.

* Tue Jan 20 2015 Dmitriy Kuminov <coding@dmik.org> 1.46.4-1
- Initial package for version 1.46.4.
