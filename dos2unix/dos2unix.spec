Summary: Text file format converters
Name: dos2unix
Version: 7.5.2
Release: 1%{?dist}
License: BSD-3-Clause
URL: https://waterlan.home.xs4all.nl/dos2unix.html
%if !0%{?os2_version}
Source: https://waterlan.home.xs4all.nl/dos2unix/%{name}-%{version}.tar.gz
Source: https://waterlan.home.xs4all.nl/dos2unix/%{name}-%{version}.tar.gz.asc
Source: https://keyserver.ubuntu.com/pks/lookup?op=get&search=0x38C1F572B12725BE#./38C1F572B12725BE.asc
%else
%scm_source github https://github.com/TeLLie/%{name}-os2 master-os2
%endif

BuildRequires: gcc
BuildRequires: gettext
BuildRequires: make
# perl modules, required for tests
BuildRequires: perl-Test-Harness
BuildRequires: perl-Test-Simple
# for gpg signature verification
%if !0%{?os2_version}
BuildRequires: gnupg2
%endif

Provides: unix2dos = %{version}-%{release}
Obsoletes: unix2dos < 5.1-1

%description
Convert text files with DOS or Mac line endings to Unix line endings and
vice versa.

%debug_package

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%autosetup
%else
%scm_setup
%endif

%build
%if !0%{?os2_version}
%make_build LDFLAGS="%{build_ldflags}"
%else
make %{?_smp_mflags}
%endif

%install
%make_install

# We add doc files manually to %%doc
rm -rf %{buildroot}%{_docdir}

%find_lang %{name} --with-man --all-name

%check
%if !0%{?os2_version}
make test
%endif

%files -f %{name}.lang
%license COPYING.txt
%doc man/man1/dos2unix.htm ChangeLog.txt
%doc NEWS.txt README.txt TODO.txt
%if !0%{?os2_version}
%{_bindir}/dos2unix
%{_bindir}/mac2unix
%{_bindir}/unix2dos
%{_bindir}/unix2mac
%else
%{_bindir}/dos2unix.exe
%{_bindir}/mac2unix.exe
%{_bindir}/unix2dos.exe
%{_bindir}/unix2mac.exe
%endif
%{_mandir}/man1/*.1*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Jan 24 2024 Elbert Pol <elbert.pol@gmail.com> - 7.5.2-1
- Updated to latest version
- Add debug package

* Wed Aug 30 2023 Elbert Pol <elbert.pol@gmail.com> - 7.5.1-1
- Updated to latest version

* Fri May 19 2023 Elbert Pol <elbert.pol@gmail.com> - 7.5.0-1
- Updated to latest version

* Sun Feb 12 2023 Elbert Pol <elbert.pol@gmail.com> - 7.4.4-1
- Updated to latest version

* Sun Jun 05 2022 Elbert Pol <elbert.pol@gmail.com> - 7.4.3-1
- Updated to latest version

* Mon Oct 19 2020 Elbert Pol <elbert.pol@gmail.com> - 7.4.2-2
- Add changelog from previous version

* Mon Oct 12 2020 Elbert Pol <elbert.pol@gmail.com> - 7.4.2-1
- Update to latest source
- Add some OS2 definition to spec file

* Sat Apr 11 2020 Elbert Pol <elbert.pol@gmail.com> 7.4.1-1
- Updated to latest source

* Sat Feb 11 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 7.3.4-1
- initial port
