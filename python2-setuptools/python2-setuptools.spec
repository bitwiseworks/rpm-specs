%global srcname setuptools

%bcond_with tests

Name:           python2-setuptools
# When updating, update the bundled libraries versions bellow!
Version:        41.2.0
Release:        1%{?dist}
Summary:        Easily build and distribute Python packages
# setuptools is MIT
# packaging is BSD or ASL 2.0
# pyparsing is MIT
# six is MIT
License:        MIT and (BSD or ASL 2.0)
URL:            https://pypi.python.org/pypi/%{srcname}
%if !0%{?os2_version}
Source0:        %{pypi_source %{srcname} %{version} zip}
%else
Vendor:         bww bitwise works GmbH
%scm_source github  https://github.com/bitwiseworks/%{srcname}-os2 v%{version}-os2
%endif

BuildArch:      noarch

BuildRequires:  gcc
BuildRequires:  python2-devel

%if %{with tests}
BuildRequires:  python2-futures
BuildRequires:  python2-pip
BuildRequires:  python2-pytest
BuildRequires:  python2-mock
BuildRequires:  python2-wheel
%endif

# Virtual provides for the packages bundled by setuptools.
# You can find the versions in setuptools/setuptools/_vendor/vendored.txt
Provides: bundled(python2dist(packaging)) = 16.8
Provides: bundled(python2dist(pyparsing)) = 2.2.1
Provides: bundled(python2dist(six)) = 1.10.0

%{?python_provide:%python_provide python2-setuptools}

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.


%prep
%if !0%{?os2_version}
%autosetup -p1 -n %{srcname}-%{version}
rm -r %{srcname}.egg-info
%else
%scm_setup
%endif

# Strip shbang
find setuptools pkg_resources -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled exes
rm -f setuptools/*.exe
# These tests require internet connection
rm setuptools/tests/test_integration.py 
# Spurious executable perm https://github.com/pypa/setuptools/pull/1441
chmod -x README.rst

%build
# Warning, different bootstrap meaning here, has nothing to do with our bcond
# This bootstraps .egg-info directory needed to build setuptools
%{__python2} bootstrap.py

%py2_build


%install
%py2_install

rm %{buildroot}%{_bindir}/easy_install
rm -rf %{buildroot}%{python2_sitelib}/setuptools/tests

find %{buildroot}%{python2_sitelib} -name '*.exe' | xargs rm -f

# Don't ship these
%if !0%{?os2_version}
rm -r docs/{Makefile,conf.py,_*}
%else
rm -r docs/Makefile
rm -r docs/conf.py
rm -r docs/_*
%endif


%if %{with tests}
%check
# see https://github.com/pypa/setuptools/issues/1170 for PYTHONDONTWRITEBYTECODE
# several tests are xfailed with POSIX locale, so we set C.utf-8 (not needed on py3)
# test_virtualenv is ignored to break dependency on python2-pytest-virtualenv
LANG=C.utf-8 PYTHONDONTWRITEBYTECODE=1 PYTHONPATH=$(pwd) pytest-%{python2_version} \
    --ignore setuptools/tests/test_virtualenv.py
%endif


%files -n python2-setuptools
%license LICENSE
%doc docs/* CHANGES.rst README.rst
%{python2_sitelib}/setuptools-%{version}-py%{python2_version}.egg-info/
%{python2_sitelib}/setuptools/
%{python2_sitelib}/easy_install*
%{python2_sitelib}/pkg_resources/
%{_bindir}/easy_install-2.*


%changelog
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
