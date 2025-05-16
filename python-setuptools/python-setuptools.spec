%global srcname setuptools

# used when bootstrapping new Python versions
%if !0%{?os2_version}
%bcond bootstrap 0
%else
%bcond_without bootstrap
%endif

# Similar to what we have in pythonX.Y.spec files.
# If enabled, provides unversioned executables and other stuff.
# Disable it if you build this package in an alternative stack.
%if !0%{?os2_version}
%bcond main_python 1
%else
%bcond_without main_python
%endif

# The original RHEL N+1 content set is defined by (build)dependencies
# of the packages in Fedora ELN. Hence we disable tests and documentation here
# to prevent pulling many unwanted packages in.
# We intentionally keep this enabled on EPEL.
%if !0%{?os2_version}
%bcond tests %[%{without bootstrap} && (%{defined fedora} || %{defined epel})]
%else
%bcond_with tests
%endif

%global python_wheel_name %{srcname}-%{version}-py3-none-any.whl

Name:           python-setuptools
# When updating, update the bundled libraries versions bellow!
Version:        74.1.3
Release:        2%{?dist}
Summary:        Easily build and distribute Python packages
# setuptools is MIT
# autocommand is LGPL-3.0-only
# backports-tarfile is MIT
# importlib-metadata is Apache-2.0
# inflect is MIT
# jaraco-context is MIT
# jaraco-collections is MIT
# jaraco-functools is MIT
# jaraco-text is MIT
# more-itertools is MIT
# packaging is BSD-2-Clause OR Apache-2.0
# platformdirs is MIT
# tomli is MIT
# typeguard is MIT
# typing-extensions is Python-2.0.1
# wheel is MIT
# zipp is MIT
# the setuptools logo is MIT
License:        MIT AND Apache-2.0 AND (BSD-2-Clause OR Apache-2.0) AND Python-2.0.1 AND LGPL-3.0-only
URL:            https://pypi.python.org/pypi/%{srcname}
%if !0%{?os2_version}
Source0:        %{pypi_source %{srcname} %{version}}

# Some test deps are optional and either not desired or not available in Fedora, thus this patch removes them.
Patch:          Remove-optional-or-unpackaged-test-deps.patch

# The `setup.py install` deprecation notice might be confusing for RPM packagers
# adjust it, but only when $RPM_BUILD_ROOT is set
Patch:          Adjust-the-setup.py-install-deprecation-message.patch

# setuptools rewrites all shebangs to "#!python" which breaks workflows
# where no external installers (usually rewriting this) are involved.
# https://github.com/pypa/setuptools/issues/4883
# - Resolution: deprecated functionality won't be fixed.
# brp-mangle-shebang script cannot mangle this and fails for many pkgs.
Patch:          Revert-Always-rewrite-a-Python-shebang-to-python.patch
%else
Vendor:         bww bitwise works GmbH
%scm_source github  https://github.com/bitwiseworks/%{srcname}-os2 v%{version}-os2
%endif

BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel

%if %{with tests}
BuildRequires:  gcc
%endif

# python3 bootstrap: this is built before the final build of python3, which
# adds the dependency on python3-rpm-generators, so we require it manually
# The minimal version is for bundled provides verification script to accept multiple files as input
%if !0%{?os2_version}
BuildRequires:  python3-rpm-generators >= 12-8
%else
%dnl BuildRequires:  python3-rpm-generators
%endif

%if %{without bootstrap}
BuildRequires:  pyproject-rpm-macros >= 0-44
# Not to use the pre-generated egg-info, we use setuptools from previous build to generate it
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.

# Virtual provides for the packages bundled by setuptools.
# Bundled packages are defined in multiple files. Generate the list with:
# pip freeze --path setuptools/_vendor > vendored.txt
# %%{_rpmconfigdir}/pythonbundles.py --namespace 'python%%{python3_pkgversion}dist' vendored.txt
%global bundled %{expand:
Provides: bundled(python%{python3_pkgversion}dist(autocommand)) = 2.2.2
Provides: bundled(python%{python3_pkgversion}dist(backports-tarfile)) = 1.2
Provides: bundled(python%{python3_pkgversion}dist(importlib-metadata)) = 8
Provides: bundled(python%{python3_pkgversion}dist(inflect)) = 7.3.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-collections)) = 5.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-context)) = 5.3
Provides: bundled(python%{python3_pkgversion}dist(jaraco-functools)) = 4.0.1
Provides: bundled(python%{python3_pkgversion}dist(jaraco-text)) = 3.12.1
Provides: bundled(python%{python3_pkgversion}dist(more-itertools)) = 10.3
Provides: bundled(python%{python3_pkgversion}dist(packaging)) = 24.2
Provides: bundled(python%{python3_pkgversion}dist(platformdirs)) = 4.2.2
Provides: bundled(python%{python3_pkgversion}dist(tomli)) = 2.0.1
Provides: bundled(python%{python3_pkgversion}dist(typeguard)) = 4.3
Provides: bundled(python%{python3_pkgversion}dist(typing-extensions)) = 4.12.2
Provides: bundled(python%{python3_pkgversion}dist(wheel)) = 0.45.1
Provides: bundled(python%{python3_pkgversion}dist(zipp)) = 3.19.2
}

%package -n python%{python3_pkgversion}-setuptools
Summary:        Easily build and distribute Python 3 packages
%{bundled}

# For users who might see ModuleNotFoundError: No module named 'pkg_resoureces'
# NB: Those are two different provides: one contains underscore, the other hyphen
%py_provides    python%{python3_pkgversion}-pkg_resources
%py_provides    python%{python3_pkgversion}-pkg-resources

%description -n python%{python3_pkgversion}-setuptools
Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.

%if %{without bootstrap}
%package -n     %{python_wheel_pkg_prefix}-%{srcname}-wheel
Summary:        The setuptools wheel
%{bundled}

%description -n %{python_wheel_pkg_prefix}-%{srcname}-wheel
A Python wheel of setuptools to use with venv.
%endif


%prep
%if !0%{?os2_version}
%autosetup -p1 -n %{srcname}-%{version}
%else
%scm_setup
%endif
%if %{without bootstrap}
# If we don't have setuptools installed yet, we use the pre-generated .egg-info
# See https://github.com/pypa/setuptools/pull/2543
# And https://github.com/pypa/setuptools/issues/2550
# WARNING: We cannot remove this folder since Python 3.11.1,
#          see https://github.com/pypa/setuptools/issues/3761
#rm -r %%{srcname}.egg-info
%endif

# Strip shbang
find setuptools pkg_resources -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled exes
rm -f setuptools/*.exe
# Don't ship these
rm -r docs/conf.py

%if %{without bootstrap}
%generate_buildrequires
%pyproject_buildrequires -r %{?with_tests:-x test}
%endif

%build
%if %{with bootstrap}
%py3_build
%else
%pyproject_wheel
%endif


%install
%if %{with bootstrap}
# The setup.py install command tries to import distutils
# but the distutils-precedence.pth file is not yet respected
# and Python 3.12+ no longer has distutils in the standard library.
ln -s setuptools/_distutils distutils
PYTHONPATH=$PWD %py3_install
unlink distutils
%else
%pyproject_install
%pyproject_save_files setuptools pkg_resources _distutils_hack
%endif

# https://github.com/pypa/setuptools/issues/2709
find %{buildroot}%{python3_sitelib} -name tests -print0 | xargs -0 rm -r

%if %{without bootstrap}
sed -Ei '/\/tests\b/d' %{pyproject_files}

# Install the wheel for the python-setuptools-wheel package
mkdir -p %{buildroot}%{python_wheel_dir}
install -p %{_pyproject_wheeldir}/%{python_wheel_name} -t %{buildroot}%{python_wheel_dir}
%endif


%check
%if %{without bootstrap}
# Verify bundled provides are up to date
%{python3} -m pip freeze --path setuptools/_vendor > vendored.txt
%{_rpmconfigdir}/pythonbundles.py vendored.txt --namespace 'python%{python3_pkgversion}dist' --compare-with '%{bundled}'

# Regression test, the wheel should not be larger than 1300 kB
# https://bugzilla.redhat.com/show_bug.cgi?id=1914481#c3
test $(stat --format %%s %{_pyproject_wheeldir}/%{python_wheel_name}) -lt 1300000

%pyproject_check_import -e '*.tests' -e '*.tests.*'
%endif

# Regression test, the tests are not supposed to be installed
test ! -d %{buildroot}%{python3_sitelib}/pkg_resources/tests
test ! -d %{buildroot}%{python3_sitelib}/setuptools/tests
test ! -d %{buildroot}%{python3_sitelib}/setuptools/_distutils/tests

%if %{with tests}
# Upstream tests
# --ignore=setuptools/tests/integration/
# --ignore=setuptools/tests/config/test_apply_pyprojecttoml.py
# -k "not test_pip_upgrade_from_source and not test_equivalent_output"
#   the tests require internet connection
# --ignore=setuptools/tests/test_editable_install.py
#   the tests require pip-run which we don't have in Fedora
# -k "not test_wheel_includes_cli_scripts"
#   the test expects removed .exe files to be installed
# --ignore=tools
#   the tests test various upstream release tools we don't use/ship
PRE_BUILT_SETUPTOOLS_WHEEL=%{_pyproject_wheeldir}/%{python_wheel_name} \
PYTHONPATH=$(pwd) %pytest \
 --ignore=setuptools/tests/integration/ \
 --ignore=setuptools/tests/test_editable_install.py \
 --ignore=setuptools/tests/config/test_apply_pyprojecttoml.py \
 --ignore=tools \
 -k "not test_pip_upgrade_from_source and not test_wheel_includes_cli_scripts and not test_equivalent_output"
%endif


%files -n python%{python3_pkgversion}-setuptools %{?!with_bootstrap:-f %{pyproject_files}}
%license LICENSE
%doc docs/* NEWS.rst README.rst
%{python3_sitelib}/distutils-precedence.pth
%if %{with bootstrap}
%{python3_sitelib}/setuptools-%{version}-py%{python3_version}.egg-info/
%{python3_sitelib}/pkg_resources/
%{python3_sitelib}/setuptools/
%{python3_sitelib}/_distutils_hack/
%endif

%if %{without bootstrap}
%files -n %{python_wheel_pkg_prefix}-%{srcname}-wheel
%license LICENSE
# we own the dir for simplicity
%dir %{python_wheel_dir}/
%{python_wheel_dir}/%{python_wheel_name}
%endif


%changelog
* Fri May 16 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 74.1.3-2
- update to version 74.1.3

* Fri Apr 18 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 74.1.3-1
- update to version 74.1.3

* Wed Apr 16 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 41.2.0-1
- update to version 41.2.0
- Split python2-setuptools from python-setuptools
- resynced with fedora spec

* Tue Jan 18 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 34.4.1-4
- fix symlink creation

* Wed Jan 12 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 34.4.1-3
- enabled python3

* Mon Jan 21 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 34.4.1-2
- rebuilt with latest python macros

* Mon May 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 34.4.1-1
- moved source to github
- rebuilt with latest python macros

* Mon Feb 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 34.2-0
- first rpm version (internal version only)
