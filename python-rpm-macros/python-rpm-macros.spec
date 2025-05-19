%global rpmmacrodir %{_rpmmacrodir}

Name:           python-rpm-macros
Summary:        The common Python RPM macros

URL:            https://src.fedoraproject.org/rpms/python-rpm-macros/

# Macros:
Source101:      macros.python
Source102:      macros.python-srpm
Source104:      macros.python3
Source105:      macros.pybytecompile

# Lua files
Source201:      python.lua

# Python code
%global compileall2_version 0.8.0
Source301:      https://github.com/fedora-python/compileall2/raw/v%{compileall2_version}/compileall2.py
Source302:      import_all_modules.py
%global pathfix_version 1.0.0
Source303:      https://github.com/fedora-python/pathfix/raw/v%{pathfix_version}/pathfix.py
Source304:      clamp_source_mtime.py

# BRP scripts
# This one is from redhat-rpm-config < 190
# A new upstream is forming in https://github.com/rpm-software-management/python-rpm-packaging/blob/main/scripts/brp-python-bytecompile
# But our version is riddled with Fedora-isms
# We might eventually move to upstream source + Fedora patches, but we are not there yet
Source401:      brp-python-bytecompile
# This one is from https://github.com/rpm-software-management/python-rpm-packaging/blob/main/scripts/brp-python-hardlink
# But we don't use a link in case it changes in upstream, there are no "versions" there yet
# This was removed from RPM 4.17+ so we maintain it here instead
Source402:      brp-python-hardlink
# This one is from redhat-rpm-config < 190
# It has no upstream yet
Source403:      brp-fix-pyc-reproducibility
# brp script to write "rpm" string into the .dist-info/INSTALLER file
Source404:      brp-python-rpm-in-distinfo

# macros and lua: MIT
# import_all_modules.py: MIT
# compileall2.py, clamp_source_mtime.py: PSF-2.0
# pathfix.py: PSF-2.0
# brp scripts: GPL-2.0-or-later
License:        MIT AND PSF-2.0 AND GPL-2.0-or-later

# The package version MUST be always the same as %%{__default_python3_version}.
# To have only one source of truth, we load the macro and use it.
# The macro is defined in python-srpm-macros.
%{lua:
if posix.stat(rpm.expand('%{SOURCE102}')) then
  rpm.load(rpm.expand('%{SOURCE102}'))
elseif posix.stat('macros.python-srpm') then
  -- something is parsing the spec without _sourcedir macro properly set
  rpm.load('macros.python-srpm')
end
}
Version:        %{__default_python3_version}
Release:        2%{?dist}

BuildArch:      noarch

# For %%__default_python3_pkgversion used in %%python_provide
# For python.lua
# For compileall2.py
Requires:       python-srpm-macros = %{version}-%{release}

# The packages are called python(3)-(s)rpm-macros
# We never want python3-rpm-macros to provide python-rpm-macros
# We opt out from all Python name-based automatic provides and obsoletes
%undefine __pythonname_provides
%undefine __pythonname_obsoletes

%description
This package contains the unversioned Python RPM macros, that most
implementations should rely on.

You should not need to install this package manually as the various
python?-devel packages require it. So install a python-devel package instead.


%package -n python-srpm-macros
Summary:        RPM macros for building Python source packages

# For directory structure and flags macros
%if !0%{?os2_version}
Requires:       redhat-rpm-config >= 190
%endif

# We bundle our own software here :/
Provides:       bundled(python3dist(compileall2)) = %{compileall2_version}

%description -n python-srpm-macros
RPM macros for building Python source packages.


%package -n python3-rpm-macros
Summary:        RPM macros for building Python 3 packages

# For %%__python3 and %%python3
Requires:       python-srpm-macros = %{version}-%{release}

# For %%py_setup and import_all_modules.py
Requires:       python-rpm-macros = %{version}-%{release}

%description -n python3-rpm-macros
RPM macros for building Python 3 packages.


%prep
%autosetup -c -T
cp -a %{sources} .

# We want to have shebang in the script upstream but not here so
# the package with macros does not depend on Python.
sed -i '1s=^#!/usr/bin/env python3==' pathfix.py


%install
mkdir -p %{buildroot}%{rpmmacrodir}
install -m 644 macros.* %{buildroot}%{rpmmacrodir}/

mkdir -p %{buildroot}%{_rpmluadir}/fedora/srpm
install -p -m 644 -t %{buildroot}%{_rpmluadir}/fedora/srpm python.lua

mkdir -p %{buildroot}%{_rpmconfigdir}/redhat
install -m 644 compileall2.py %{buildroot}%{_rpmconfigdir}/redhat/
install -m 644 clamp_source_mtime.py %{buildroot}%{_rpmconfigdir}/redhat/
install -m 644 import_all_modules.py %{buildroot}%{_rpmconfigdir}/redhat/
install -m 644 pathfix.py %{buildroot}%{_rpmconfigdir}/redhat/
install -m 755 brp-* %{buildroot}%{_rpmconfigdir}/redhat/


# We define our own BRPs here to use the ones from the %%{buildroot},
# that way, this package can be built when it includes them for the first time.
# It also ensures that:
#  - our BRPs can execute
#  - if our BRPs affect this package, we don't need to build it twice
%if !0%{?os2_version}
%define add_buildroot() %{lua:print((macros[macros[1]]:gsub(macros._rpmconfigdir, macros.buildroot .. macros._rpmconfigdir)))}
%global __brp_python_bytecompile %{add_buildroot __brp_python_bytecompile}
%global __brp_python_hardlink %{add_buildroot __brp_python_hardlink}
%global __brp_fix_pyc_reproducibility %{add_buildroot __brp_fix_pyc_reproducibility}
%global __brp_python_rpm_in_distinfo %{add_buildroot __brp_python_rpm_in_distinfo}
%endif

%check
# no macros in comments
grep -E '^#[^%%]*%%[^%%]' %{buildroot}%{rpmmacrodir}/macros.* && exit 1 || true


%files
%{rpmmacrodir}/macros.python
%{rpmmacrodir}/macros.pybytecompile
%{_rpmconfigdir}/redhat/import_all_modules.py
%{_rpmconfigdir}/redhat/pathfix.py

%files -n python-srpm-macros
%{rpmmacrodir}/macros.python-srpm
%{_rpmconfigdir}/redhat/compileall2.py
%{_rpmconfigdir}/redhat/clamp_source_mtime.py
%{_rpmconfigdir}/redhat/brp-python-bytecompile
%{_rpmconfigdir}/redhat/brp-python-hardlink
%{_rpmconfigdir}/redhat/brp-fix-pyc-reproducibility
%{_rpmconfigdir}/redhat/brp-python-rpm-in-distinfo
%{_rpmluadir}/fedora/srpm/python.lua

%files -n python3-rpm-macros
%{rpmmacrodir}/macros.python3


%changelog
* Mon May 05 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.13-2
- we can't use opt in lua scripts, as this was introduced in rpm >= 4.17

* Mon May 05 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.13-1
- update to latest version

* Fri Apr 29 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.9-3
- use the same location for the python.lua script as fedora

* Wed Sep 15 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.9-2
- use the right location for the python.lua script
- use new %%{_rpmluadir} macro instead of %%{_rpmconfigdir}/lua

* Fri Apr 09 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.9-1
- heavily reworked and adapted to latest fedora version

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1-3
- remove .exe from python2 and python3 path, as this is insane

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1-2
- add .exe to the python2 and python3 exe path

* Tue Feb 28 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1-1
- first rpm version
