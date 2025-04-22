%global pypi_name packaging

%global with_sphinx 0
%global with_test 0

Name:           python2-%{pypi_name}
Version:        20.9
Release:        1%{?dist}
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
BuildRequires:  python2-pyparsing
BuildRequires:  python-six
Requires:       python2-pyparsing
Requires:       python2-six
 

%description
python2-packaging provides core utilities for Python packages like utilities for
dealing with versions, specifiers, markers etc.

%{?python_provide:%python_provide python2-%{pypi_name}}
 
%package -n python2-%{pypi_name}-doc
Summary:        python2-packaging documentation
Suggests:       python2-%{pypi_name} = %{version}-%{release}
%description -n python2-%{pypi_name}-doc
Documentation for python2-packaging

%prep
%scm_setup
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build

# generate html docs 
%if 0%{?with_sphinx}
sphinx-build-3 docs html
%endif
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}
# Do not bundle fonts
rm -rf html/_static/fonts/

%install
%py2_install

%check
%if 0%{?with_test}
%%{__python2} -m pytest tests/
%endif

%files -n python2-%{pypi_name}
%license LICENSE LICENSE.APACHE LICENSE.BSD
%doc README.rst CHANGELOG.rst CONTRIBUTING.rst
%{python2_sitelib}/%{pypi_name}*

%files -n python2-%{pypi_name}-doc
%if 0%{?with_sphinx}
%doc html
%endif
%license LICENSE LICENSE.APACHE LICENSE.BSD

%changelog
* Wed Apr 23 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 20.9-2
- splitt python2 package

* Wed Apr 16 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 20.9-1
- enabled python3

* Tue Jan 11 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 16.8-3
- enabled python3

* Thu Apr 13 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 16.8-2
- moved source to github

* Mon Feb 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 16.8-1
- first rpm version (internal version only)
