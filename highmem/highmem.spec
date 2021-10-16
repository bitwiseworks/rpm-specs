Summary:    HighMem, a LX format 32bit DLL module 'loading above 512MB' marking utility,
Name:       highmem
Version:    1.0.3
Release:    1%{?dist}
License:    proprietary
URL:        http://www.bitwiseworks.com
Vendor:     bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/highmem b02a84f5a21e27b2479def365546b57c041d1d41

BuildRequires: gcc kbuild git zip
BuildRequires: os2tk45-headers

Source1:    macros.%{name}

%description
The purpose of this utility is to mark DLLs as high loadable.
Partially based on ABOVE512 (C) 2004 Takayuki 'January June' Suwa.

%debug_package

%prep

%scm_setup

cp %{SOURCE1} .

%build

%define kmk_env \\\
  CFLAGS="%{optflags}" \\\
  CXXFLAGS="%{optflags}" \\\
  LDFLAGS="-Zomf -Zbin-files -Zhigh-mem -Zargs-wild -Zargs-resp" \\\
  KBUILD_VERBOSE=2 \\\
  PATH_INS="%{buildroot}%{_prefix}"

kmk %{?_smp_mflags} %{kmk_env}

%install

%{__rm} -rf %{buildroot}

kmk %{kmk_env} install

%{__install} -p -m 0644 -D macros.%{name} $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.%{name}

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%doc readme.txt
%{_bindir}/*.exe
%{_rpmconfigdir}/macros.d/macros.%{name}

%changelog
* Fri Oct 15 2021 Yuri Dario <yd@os2power.com> 1.0.3-1
- Always skip marking of libc runtime dlls.

* Thu Nov 12 2020 Dmitriy Kuminov <coding@dmik.org> 1.0.2-1
- Use scm_source and friends.
- Fix system hangs when processing huge DLLs (hundreds of megabytes).

* Fri Jun 29 2018 herwig Bauernfeind <herwig.bauernfeind@bitwiseworks.com> 1.0.1-1
- add rpm macro

* Fri Jun 15 2018 herwig Bauernfeind <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- first public rpm version

