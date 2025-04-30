# When bootstrapping new Python we need to build flit in bootstrap mode.
# The Python RPM dependency generators and pip are not yet available.
%if !0%{?os2_version}
%bcond bootstrap 0
%else
%bcond_without bootstrap
%endif

# Tests are enabled by default, unless we bootstrap.
# Disable them to avoid a circular build dependency on testpath.
%if !0%{?os2_version}
%bcond tests %{without bootstrap}
%else
%bcond_with tests
%endif

Name:           python-flit-core
Version:        3.12.0
%if !0%{?os2_version}
Release:        %autorelease
%else
Release:        1%{?dist}
%endif
Summary:        PEP 517 build backend for packages using Flit

# flit-core is BSD-3-Clause
# flit_core/versionno.py contains a regex that is from packaging, BSD-2-Clause
License:        BSD-3-Clause AND BSD-2-Clause

URL:            https://flit.pypa.io/
%if !0%{?os2_version}
Source:         %{pypi_source flit_core}
%else
Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/flit-os2 master-os2
%endif

BuildArch:      noarch
BuildRequires:  python3-devel

%if %{with tests}
BuildRequires:  python3-pytest
# Test deps that require flit-core to build:
BuildRequires:  python3-testpath
%endif

%global _description %{expand:
This provides a PEP 517 build backend for packages using Flit.
The only public interface is the API specified by PEP 517,
at flit_core.buildapi.}

%description %_description


%package -n python3-flit-core
Summary:        %{summary}
Conflicts:      python3-flit < 2.1.0-2

# RPM generators are not yet available when we bootstrap
%if %{with bootstrap}
Provides:       python%{python3_pkgversion}dist(flit-core) = %{version}
Provides:       python%{python3_version}dist(flit-core) = %{version}
Requires:       python(abi) = %{python3_version}
%endif

%description -n python3-flit-core %_description


%prep
%if !0%{?os2_version}
%autosetup -p1 -n flit_core-%{version}
%else
%scm_setup
cd flit_core
%endif

# Remove vendored tomli that flit_core includes to solve the circular dependency on older Pythons
# (flit_core requires tomli, but flit_core is needed to build tomli).
# We don't use this, as tomllib is a part of standard library since Python 3.11.
# Remove the bits looking for the license files of the vendored tomli.
%if !0%{?os2_version}
rm -rf flit_core/vendor
sed -iE 's/, *"flit_core\/vendor\/\*\*\/LICENSE\*"//' pyproject.toml
%endif

%if %{without bootstrap}
%generate_buildrequires
%pyproject_buildrequires
%endif


%build
%if 0%{?os2_version}
cd flit_core
%endif
%if %{with bootstrap}
%{python3} -m flit_core.wheel
%else
%pyproject_wheel
%endif

%install
%if 0%{?os2_version}
cd flit_core
%endif
%if %{with bootstrap}
%{python3} bootstrap_install.py --installdir %{buildroot}%{python3_sitelib} dist/flit_core-%{version}-py3-none-any.whl
# for consistency with %%pyproject_install/brp-python-rpm-in-distinfo:
echo rpm > %{buildroot}%{python3_sitelib}/flit_core-%{version}.dist-info/INSTALLER
rm %{buildroot}%{python3_sitelib}/flit_core-%{version}.dist-info/RECORD
%else
%pyproject_install
%endif

%check
%if !0%{?os2_version}
%py3_check_import flit_core flit_core.buildapi
%if %{with tests}
%pytest
%endif
%endif


%files -n python3-flit-core
%doc README.rst
%{python3_sitelib}/flit_core-*.dist-info/
%license %{python3_sitelib}/flit_core-*.dist-info/licenses/LICENSE
%{python3_sitelib}/flit_core/


%changelog
* Wed Apr 30 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.12.0-1
- first rpm version
