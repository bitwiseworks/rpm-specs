Name:       whois       
Version:    5.6.0
Release:    1%{?dist}
Summary:    Improved WHOIS client
Group:      Applications/Internet
License:    GPLv2+
URL:        http://www.linux.it/~md/software/
%if 0%{os2_version}
Vendor:         TeLLie OS2 forever
Distribution:   OS/2
Packager:       TeLLeRBoP
%endif
%if !0%{?os2_version}
%Source0:    https://ftp.debian.org/debian/pool/main/w/%{name}/%{name}_%{version}.tar.xz
%else
%scm_source github http://github.com/TeLLie/%{name}-os2 %{version}-os2
%endif

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Searches for an object in a RFC 3912 database.

This version of the WHOIS client tries to guess the right server to ask for
the specified object. If no guess can be made it will connect to
whois.networksolutions.com for NIC handles or whois.arin.net for IPv4
addresses and network names.

BuildRequires:  coreutils
BuildRequires:  gcc
BuildRequires:  gettext
BuildRequires:  libidn-devel
BuildRequires:  make
BuildRequires:  perl
BuildRequires:  perl(autodie)
BuildRequires:  perl(strict)
BuildRequires:  perl(warnings)
BuildRequires:  subversion zip

%define cfgfile %{name}.conf

%debug_package

%prep
%scm_setup

%build
export LDFLAGS=" -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lintl"
%make_build CONFIG_FILE="%{_sysconfdir}/%{cfgfile}" HAVE_ICONV=1 \
    CFLAGS="$RPM_OPT_FLAGS" %{?_smp_mflags}

%install
# Omit mkpasswd
make install-whois install-pos BASEDIR=$RPM_BUILD_ROOT prefix=%{_prefix}
install -p -m644 -D %{cfgfile} $RPM_BUILD_ROOT%{_sysconfdir}/%{cfgfile}
%find_lang %{name}

%post

%postun

%files -f %{name}.lang
%license COPYING debian/copyright
%doc README debian/changelog
%config(noreplace) %{_sysconfdir}/%{cfgfile}
%{_bindir}/%{name}.exe
%ghost %verify(not md5 size mtime) %{_bindir}/%{name}
%{_mandir}/man1/%{name}.*
%ghost %verify(not md5 size mtime) %{_mandir}/man1/%{name}.1
%{_mandir}/man5/%{cfgfile}.5.gz

%changelog
* Tue May 06 2025 Elbert Pol <elbert.pol@gmail.com> - 5.6.0-1
- Updated to latest version

* Mon May 13 2024 Elbert Pol <elbert.pol@gmail.com> - 5.5.23-1
- Updated to latest version

* Thu Apr 04 2024 Elbert Pol <elbert.pol@gmail.com> - 5.5.22-1
- Updated to latest version

* Sun Feb 25 2024 Elbert Pol <elbert.pol@gmail.com> - 5.5.21-1
- Updated to latest version

* Sun Nov 12 2023 Elbert Pol <elbert.pol@gmail.com> - 5.5.20-1
- Updated to latest version

* Thu Oct 12 2023 Elbert Pol <elbert.pol@gmail.com> - 5.5.19-1
- Updated to latest version
- Remove some export functions, as there now in makefile

* Mon Jul 24 2023 Elbert Pol <elbert.pol@gmail.com> - 5.5.18-1
- Updated to latest version

* Sun May 07 2023 Elbert Pol <elbert.pol@gmail.com> - 5.5.17-1
- Updated to latest version

* Sun Mar 05 2023 Elbert Pol <elbert.pol@gmail.com> - 5.5.16-1
- Updated to latest version

* Fri Dec 30 2022 Elbert Pol <elbert.pol@gmail.com> - 5.5.15-1
- Updated to latest version

* Tue Oct 18 2022 Elbert Pol <elbert.pol@gmail.com> - 5.5.14-1
- Updated to latest version

* Sun Apr 10 2022 Elbert Pol <elbert.pol@gmail.com> - 5.5.13-1
- Updated source to latest version

* Tue Mar 08 2022 Elbert Pol <elbert.pol@gmail.com> - 5.5.12-1
- Updated source to latest version

* Tue Jan 04 2022 Elbert Pol <elbert.pol@gmail.com> - 5.5.11-1
- Updated source to latest version

* Mon Jun 07 2021 Elbert Pol <elbert.pol@gmail.com> - 5.5.10-1
- Updated source to latest version

* Sun Mar 28 2021 Elbert Pol <elbert.pol@gmail.com> - 5.5.9-1
- Updated source to latest version

* Mon Feb 15 2021 Elbert Pol <elbert.pol@gmail.com> - 5.5.8-1
- Updated source to latest version

* Sun Nov 01 2020 Elbert Pol <elbert.pol@gmail.com> - 5.5.7-1
- Updated source to latest version

* Tue Sep 22 2020 Elbert Pol <elbert.pol@gmail.com> - 5.5.6-1
- Update to latest version

* Wed Jan 01 2020 Elbert Pol <elbert.pol@gmail.com> - 5.5.4-1
- Updated tp latest source

* Mon Nov 18 2019 Elbert Pol <elbert.pol@gmail.com> - 5.5.3-1
- Updated to latest source

* Thu Oct 03 2019 Elbert Pol <elbert.pol@gmail.com> - 5.5.2-1
- Updated to latest source

* Mon Jul 22 2019 Elbert Pol <elbert.pol@gmail.com> - 5.5.0-1
- Updated to latest source

* Wed Jun 12 2019 Elbert Pol <elbert.pol@gmail.com> - 5.4.3-1
- Updated to latest source

* Sun Jan 27 2019 Elbert Pol <elbert.pol@gmail.com> - 5.4.1-1
- Updated to v5.4.1

* Mon Nov 05 2018 Elbert Pol <elbert.pol@gmail.com> - 5.4.0-3
- Remove more bogus data in changelog

* Mon Oct 29 2018 Elbert Pol <elbert.pol@gmail.com> - 5.4.0-2
- Remove bogus data in changelog

* Sun Oct 28 2018 Elbert Pol <elbert.pol@gmail.com> - 5.4.0-1
- Updated to v5.4.0

* Mon Jul 16 2018 Elbert Pol <elbert.pol@gmail.com> - 5.3.2-1
- Updated to v5.3.2

* Tue May 22 2018 Elbert Pol <elbert.pol@gmail.com> - 5.3.1-1
- Updated to v5.3.1

* Wed Jan 24 2018 Elbert Pol <elbert.pol@gmail.com> - 5.2.30-1
- Updated to v5.2.30
- Remove HAVE_LIBIDN=1 from Config_File

* Wed Dec 27 2017 Elbert Pol <elbert.pol@gmail.com> - 5.2.20-1
- Updated to v5.2.20

* Mon Dec 11 2017 Elbert Pol <elbert.pol@gmail.com> - 5.2.19-1
- Updated to v5.2.19

* Wed Aug 23 2017 Elbert Pol <elbert.pol@gmail.com> - 5.2.18-1
- Updated to v5.2.18

* Sun Aug 20 2017 Elbert Pol <elbert.pol@gmail.com> - 5.2.17-1
- Updated to v5.2.17

* Wed Jun 14 2017 Elbert Pol <elbert.pol@gmail.com> - 5.2.16-1
- Updated to v5.2.16

* Wed Mar 01 2017 Elbert Pol <elbert.pol@gmail.com> - 5.2.15-1
- Update to v5.2.15
- use new scm_ macros

* Sat Feb 18 2017 Elbert Pol <elbert.pol@gmail.com> - 5.2.14-1
- 5.2.14 First OS2 rpm
