%global modname dateutil

Name:           python-%{modname}
Version:        2.8.1
Release:        3%{?dist}
Epoch:          1
Summary:        Powerful extensions to the standard datetime module

License:        BSD
URL:            https://github.com/dateutil/dateutil
Source:         %{pypi_source}
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif

# when bootstrapping dateutil-freezegun, we cannot run tests
%if !0%{?os2_version}
%bcond_without tests
%else
%bcond_with tests
%endif

BuildArch:      noarch
%if !0%{?os2_version}
BuildRequires:  python3-sphinx
BuildRequires:  python3-sphinx_rtd_theme
%endif

%global _description \
The dateutil module provides powerful extensions to the standard datetime\
module available in Python.

%description %_description

%package -n python2-%{modname}
Summary:        %summary
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-setuptools_scm
%if %{with tests} && 0%{?fedora} < 32
BuildRequires:  python2-freezegun
BuildRequires:  python2-pytest
BuildRequires:  python2-six
%endif
%if !0%{?os2_version}
Requires:       tzdata
%endif
Requires:       python2-six
%{?python_provide:%python_provide python2-%{modname}}

%description -n python2-%{modname}  %_description

%package -n python3-%{modname}
Summary:        %summary
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm
%if %{with tests}
BuildRequires:  python3-freezegun
BuildRequires:  python3-hypothesis
BuildRequires:  python3-pytest
BuildRequires:  python3-six
%endif
%if !0%{?os2_version}
Requires:       tzdata
%endif
Requires:       python3-six
%{?python_provide:%python_provide python3-%{modname}}

%description -n python3-%{modname}  %_description

%package doc
Summary: API documentation for python-dateutil
%description doc
This package contains %{summary}.

%prep
%autosetup
%if !0%{?os2_version}
iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
%else
iconv -f ISO-8859-1 -t UTF-8 NEWS > NEWS.new
%endif
mv NEWS.new NEWS

%build
%py2_build
%py3_build
%if !0%{?os2_version}
make -C docs html
%endif

%install
%py2_install
%py3_install

%if %{with tests}
%check
%{__python3} -m pytest -W ignore::pytest.PytestUnknownMarkWarning

%if 0%{?fedora} < 32
# Tests skipped on Python 2:
# dateutil/test/property: Tests using python2-hypothesis are skipped to break
#   up dependency loops as the Python 2 stack is being removed form Fedora.
# gettz_badzone_unicode: "os.path.isfile" raises the wrong error on non-UTF-8
#   locales. Probably not worth worrying about.
%{__python2} -m pytest \
    --ignore dateutil/test/property \
    -k 'not gettz_badzone_unicode'
%endif
%endif

%files -n python2-%{modname}
%license LICENSE
%doc NEWS README.rst
%{python2_sitelib}/%{modname}/
%{python2_sitelib}/*.egg-info

%files -n python3-%{modname}
%license LICENSE
%doc NEWS README.rst
%{python3_sitelib}/%{modname}/
%{python3_sitelib}/*.egg-info

%files doc
%license LICENSE
%if !0%{?os2_version}
%doc docs/_build/html
%endif

%changelog
* Thu Jan 20 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1:2.8.1-3
- enable python3
- resync spec with fedora

* Mon Nov 25 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.8.1-2
- remove tzdata req for now (needs to be ported once)

* Fri Nov 22 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.8.1-1
- update to version 2.8.1
- merge spec with latest fedora one

* Wed May 10 2017 yd <yd@os2power.com> 2.6.0-1
- first public build.
