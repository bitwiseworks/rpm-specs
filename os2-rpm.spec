Summary: OS/2 specific RPM macros and scripts
Name: os2-rpm
Version: 0
Release: 1%{?dist}
License: GPLv2+
Group: Development/System
Vendor: bww bitwise works GmbH

BuildArch: noarch

Requires: rpm >= 4.13.0-15
Provides: system-rpm-config = %{version}-%{release}

Source0: macros.os2
Source1: brp-strip-os2
Source2: find-legacy-runtime.sh

%description
OS/2 specific RPM macros and scripts neecessary to install RPM packages on
the OS/2 operating system.

%package build
Summary: OS/2 specific RPM macros and scripts to build RPM packages
Provides: %{name} = %{version}-%{release}
Requires: rpm-build >= 4.13.0-15

%description build
OS/2 specific RPM macros and scripts neecessary to build RPM packages for
the OS/2 operating system.

%global _rpmconfigdir_os2 %{_rpmconfigdir}/%{_vendor}

%prep
# Move all sources to build subdir to reference them by name instead of SOURCEx
%setup -c -T
cp -a %{sources} .

# Note: we put the value of _rpmconfigdir_os2 unexpanded.
sed -e 's|@RPMCONFIGDIR_OS2@|%%{_rpmconfigdir}/%%{_vendor}|' -i macros.os2

%install
mkdir -p %{buildroot}%{_rpmconfigdir_os2}
install -p -m 644 macros.os2 %{buildroot}%{_rpmconfigdir_os2}/macros
install -p -m 644 -t %{buildroot}%{_rpmconfigdir_os2} brp-strip-os2 find-legacy-runtime.sh

%files
# TODO WPS and WarpIn scripts will move here from rpm

%files build
%dir %{_rpmconfigdir_os2}
%{_rpmconfigdir_os2}/macros
%{_rpmconfigdir_os2}/brp-strip-os2
%{_rpmconfigdir_os2}/find-legacy-runtime.sh

%changelog
* Thu Apr 6 2017 Dmitriy Kuminov <coding@dmik.org> 0-1
- Initial release.
