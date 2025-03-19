# Place rpm-macros into proper location
%global rpmmacrodir %(d=%{_rpmconfigdir}/macros.d; [ -d $d ] || d=%{_sysconfdir}/rpm; echo $d)

Name:           python-rpm-macros
Summary:        The common Python RPM macros

# Macros:
Source101:      macros.python
Source102:      macros.python-srpm
Source104:      macros.python3
Source105:      macros.pybytecompile

# Lua files
Source201:      python.lua

# Python code
%global compileall2_version 0.7.1
Source301:      https://github.com/fedora-python/compileall2/raw/v%{compileall2_version}/compileall2.py

# macros and lua: MIT, compileall2.py: PSFv2
License:        MIT and Python

# The package version MUST be always the same as %%{__default_python3_version}.
# To have only one source of truth, we load the macro and use it.
# The macro is defined in python-srpm-macros.
                %{?load:%{SOURCE102}}
Version:        %{__default_python3_version}
Release:        3%{?dist}

BuildArch:      noarch

# For %%__default_python3_pkgversion used in %%python_provide
# For python.lua
# For compileall2.py
Requires:       python-srpm-macros = %{version}-%{release}

%description
This package contains the unversioned Python RPM macros, that most
implementations should rely on.

You should not need to install this package manually as the various
python?-devel packages require it. So install a python-devel package instead.


%package -n python-srpm-macros
Summary:        RPM macros for building Python source packages

# For directory structure and flags macros
%if !0%{?os2_version}
Requires:       redhat-rpm-config
%endif

# We bundle our own software here :/
Provides:       bundled(python3dist(compileall2)) = %{compileall2_version}

%description -n python-srpm-macros
RPM macros for building Python source packages.


%package -n python3-rpm-macros
Summary:        RPM macros for building Python 3 packages

# For %%__python3 and %%python3
Requires:       python-srpm-macros = %{version}-%{release}

# For %%py_setup
Requires:       python-rpm-macros = %{version}-%{release}

%description -n python3-rpm-macros
RPM macros for building Python 3 packages.


%prep
%autosetup -c -T
cp -a %{sources} .


%install
mkdir -p %{buildroot}%{rpmmacrodir}
install -m 644 macros.* %{buildroot}%{rpmmacrodir}/

mkdir -p %{buildroot}%{_rpmluadir}/fedora/srpm
install -p -m 644 -t %{buildroot}%{_rpmluadir}/fedora/srpm python.lua

%if !0%{?os2_version}
mkdir -p %{buildroot}%{_rpmconfigdir}/redhat
install -m 644 compileall2.py %{buildroot}%{_rpmconfigdir}/redhat/
%else
mkdir -p %{buildroot}%{_rpmconfigdir_os2}
install -m 644 compileall2.py %{buildroot}%{_rpmconfigdir_os2}/
%endif


%files
%{rpmmacrodir}/macros.python
%{rpmmacrodir}/macros.pybytecompile

%files -n python-srpm-macros
%{rpmmacrodir}/macros.python-srpm
%if !0%{?os2_version}
%{_rpmconfigdir}/redhat/compileall2.py
%else
%{_rpmconfigdir_os2}/compileall2.py
%endif
%{_rpmluadir}/fedora/srpm/python.lua

%files -n python3-rpm-macros
%{rpmmacrodir}/macros.python3


%changelog
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
