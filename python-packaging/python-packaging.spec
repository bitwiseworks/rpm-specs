%global pypi_name packaging

%global build_wheel 0
%global with_python3 1
%global with_sphinx 0
%global with_test 0

%global python2_wheelname %{pypi_name}-%{version}-py2.py3-none-any.whl
%global python3_wheelname %python2_wheelname

Name:           python-%{pypi_name}
Version:        16.8
Release:        3%{?dist}
Summary:        Core utilities for Python packages

License:        BSD or ASL 2.0
URL:            https://github.com/pypa/packaging
Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{pypi_name}-os2 %{version}-os2

BuildArch:      noarch
 
BuildRequires:  python2-setuptools
BuildRequires:  python2-devel
%if 0%{?with_test}
BuildRequires:  python2-pytest
%endif
#BuildRequires:  python-pretend
BuildRequires:  python2-pyparsing
BuildRequires:  python-six
 
%if 0%{?with_python3}
#BuildRequires:  python3-setuptools
BuildRequires:  python3-devel
%if 0%{?with_test}
BuildRequires:  python3-pytest
%endif
#BuildRequires:  python3-pretend
BuildRequires:  python3-pyparsing
#BuildRequires:  python3-six
#BuildRequires:  python3-sphinx
%endif

%if 0%{?build_wheel}
BuildRequires:  python2-pip
BuildRequires:  python-wheel
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif

%description
python-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%package -n python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}
 
Requires:       python2-pyparsing
Requires:       python2-six
%description -n python2-%{pypi_name}
python2-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.


%if 0%{?with_python3}
%package -n python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}
 
Requires:       python3-pyparsing
Requires:       python3-six
%description -n python3-%{pypi_name}
python3-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.
%endif

%package -n python-%{pypi_name}-doc
Summary:        python-packaging documentation
Suggests:       python2-%{pypi_name} = %{version}-%{release}
%description -n python-%{pypi_name}-doc
Documentation for python-packaging

%prep
%scm_setup
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

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
%endif
# generate html docs 
%if 0%{?with_sphinx}
sphinx-build-3 docs html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/

%install
%if 0%{?build_wheel}
%py2_install_wheel %{python2_wheelname}
%else
%py2_install
%endif
%if 0%{?with_python3}
%if 0%{?build_wheel}
%py3_install_wheel %{python3_wheelname}
%else
%py3_install
%endif
%endif

%check
%if 0%{?with_test}
%%{__python2} -m pytest tests/
%if 0%{?with_python3}
%{__python3} -m pytest tests/
%endif
%endif

%files -n python2-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python2_sitelib}/%{pypi_name}*

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-*.egg-info
%endif

%files -n python-%{pypi_name}-doc
%if 0%{?with_sphinx}
%doc html
%endif
%license LICENSE LICENSE.APACHE LICENSE.BSD

%changelog
* Tue Jan 11 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 16.8-3
- enabled python3

* Thu Apr 13 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 16.8-2
- moved source to github

* Mon Feb 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 16.8-1
- first rpm version (internal version only)
