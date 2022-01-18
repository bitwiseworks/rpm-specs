
%global with_check 0
%global build_wheel 0

%global with_python3 1

%global main_name setuptools
%if 0%{?build_wheel}
%global python2_wheelname %{main_name}-%{version}-py2.py3-none-any.whl
%global python2_record %{python2_sitelib}/%{main_name}-%{version}.dist-info/RECORD
%if 0%{?with_python3}
%global python3_wheelname %python2_wheelname
%global python3_record %{python3_sitelib}/%{main_name}-%{version}.dist-info/RECORD
%endif
%endif

Name:           python-setuptools
Version:        34.4.1
Release:        4%{?dist}
Summary:        Easily build and distribute Python packages

Group:          Applications/System
License:        MIT
URL:            https://pypi.python.org/pypi/%{main_name}
Vendor:         bww bitwise works GmbH
%scm_source github  https://github.com/bitwiseworks/%{main_name}-os2 v%{version}-os2-1


BuildArch:      noarch
BuildRequires:  python-rpm-macros >= 1-3
BuildRequires:  python2-devel
BuildRequires:  python2-packaging
BuildRequires:  python2-appdirs
%if 0%{?build_wheel}
BuildRequires:  python-pip
BuildRequires:  python-wheel
%endif
%if 0%{?with_check}
BuildRequires:  python2-pytest
BuildRequires:  python2-mock
BuildRequires:  python2-backports-unittest_mock
%endif # with_check

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-packaging
BuildRequires:  python3-appdirs
%if 0%{?with_check}
BuildRequires:  python3-pytest
BuildRequires:  python3-mock
%endif # with_check
%if 0%{?build_wheel}
BuildRequires:  python3-pip
BuildRequires:  python3-wheel
%endif # build_wheel
%endif # with_python3

# We're now back to setuptools as the package.
# Keep the python-distribute name active for a few releases.  Eventually we'll
# want to get rid of the Provides and just keep the Obsoletes
Provides: python-distribute = %{version}-%{release}
Obsoletes: python-distribute < 0.6.36-2


%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%package -n python2-setuptools
Summary:        Easily build and distribute Python packages
%{?python_provide:%python_provide python2-setuptools}
Requires: python2-packaging >= 16.8
Requires: python2-six >= 1.6.0
Requires: python2-appdirs >= 1.4.0
%description -n python2-setuptools
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%if 0%{?with_python3}
%package -n python3-setuptools
Summary:        Easily build and distribute Python 3 packages
Requires: python3-packaging >= 16.8
Requires: python3-six >= 1.6.0
Requires: python3-appdirs >= 1.4.0
Group:          Applications/System
%{?python_provide:%python_provide python3-setuptools}

# Note: Do not need to Require python3-backports-ssl_match_hostname because it
# has been present since python3-3.2.  We do not ship python3-3.0 or
# python3-3.1 anywhere

%description -n python3-setuptools
Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.py.

%endif # with_python3

%prep
%scm_setup
python2.7 bootstrap.py

# We can't remove .egg-info (but it doesn't matter, since it'll be rebuilt):
#  The problem is that to properly execute setuptools' setup.py,
#   it is needed for setuptools to be loaded as a Distribution
#   (with egg-info or .dist-info dir), it's not sufficient
#   to just have them on PYTHONPATH
#  Running "setup.py install" without having setuptools installed
#   as a distribution gives warnings such as
#    ... distutils/dist.py:267: UserWarning: Unknown distribution option: 'entry_points'
#   and doesn't create "easy_install" and .egg-info directory
# Note: this is only a problem if bootstrapping wheel or building on RHEL,
#  otherwise setuptools are installed as dependency into buildroot

# Strip shbang
find setuptools -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled exes
rm -f setuptools/*.exe
# These tests require internet connection
rm setuptools/tests/test_integration.py 


%build
%if 0%{?build_wheel}
%py2_build_wheel
%else
%py2_build
%endif

%if 0%{?with_python3}
%if 0%{?build_wheel}
%py3_build_wheel
%else
%py3_build
%endif
%endif # with_python3

%install
# Must do the python3 install first because the scripts in /usr/bin are
# overwritten with every setup.py install (and we want the python2 version
# to be the default for now).
%if 0%{?with_python3}
%if 0%{?build_wheel}
%py3_install_wheel %{python3_wheelname}

# TODO: we have to remove this by hand now, but it'd be nice if we wouldn't have to
# (pip install wheel doesn't overwrite)
rm %{buildroot}%{_bindir}/easy_install

sed -i '/\/usr\/bin\/easy_install,/d' %{buildroot}%{python3_record}
%else
%py3_install
%endif

rm -rf %{buildroot}%{python3_sitelib}/setuptools/tests
%if 0%{?build_wheel}
sed -i '/^setuptools\/tests\//d' %{buildroot}%{python3_record}
%endif

find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f
%endif # with_python3

%if 0%{?build_wheel}
%py2_install_wheel %{python2_wheelname}
%else
%py2_install
%endif

rm -rf %{buildroot}%{python2_sitelib}/setuptools/tests
%if 0%{?build_wheel}
sed -i '/^setuptools\/tests\//d' %{buildroot}%{python2_record}
%endif

find %{buildroot}%{python2_sitelib} -name '*.exe' | xargs rm -f

# Don't ship these
rm -r docs/Makefile
rm -r docs/conf.py
rm -r docs/_*

%if 0%{?with_check}
%check
#LANG=en_US.utf8 PYTHONPATH=$(pwd) py.test

%if 0%{?with_python3}
LANG=en_US.utf8 PYTHONPATH=$(pwd) py.test-%{python3_version}
%endif # with_python3
%endif # with_check

%files -n python2-setuptools
%license LICENSE
%doc docs/* CHANGES.rst README.rst
%{python2_sitelib}/*
%{_bindir}/easy_install
%{_bindir}/easy_install-2.*

%if 0%{?with_python3}
%files -n python3-setuptools
%license LICENSE CHANGES.rst README.rst
%doc docs/*
%{python3_sitelib}/easy_install.py
%{python3_sitelib}/pkg_resources/
%{python3_sitelib}/setuptools*/
%{python3_sitelib}/__pycache__/*
%{_bindir}/easy_install-3.*
%endif # with_python3

%changelog
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
