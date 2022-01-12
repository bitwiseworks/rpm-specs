%bcond_with tests

%global srcname setuptools_scm
%global with_python3 1

Name:           python-%{srcname}
Version:        3.3.3
Release:        2%{?dist}
Summary:        Blessed package to manage your versions by SCM tags

License:        MIT
URL:            https://pypi.python.org/pypi/setuptools_scm
Vendor:         bww bitwise works GmbH
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{srcname}; echo ${n:0:1})/%{srcname}/%{srcname}-%{version}.tar.gz

BuildArch:      noarch

%if %{with tests}
BuildRequires:  git-core
BuildRequires:  mercurial
%endif

%description
Setuptools_scm handles managing your python package versions in SCM metadata.
It also handles file finders for the supported SCMs.

%package -n python2-%{srcname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
%if %{with tests}
BuildRequires:  python2-pytest
%endif
%{?python_provide:%python_provide python2-%{srcname}}

%description -n python2-%{srcname}
Setuptools_scm handles managing your python package versions in SCM metadata.
It also handles file finders for the supported SCMs.

%if %{with_python3}
%package -n python%{python3_pkgversion}-%{srcname}
Summary:        %{summary}
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
%endif
%{?python_provide:%python_provide python%{python3_pkgversion}-%{srcname}}
Obsoletes:      platform-python-%{srcname} < %{version}-%{release}

%description -n python%{python3_pkgversion}-%{srcname}
Setuptools_scm handles managing your python package versions in SCM metadata.
It also handles file finders for the supported SCMs.
%endif

%prep
%autosetup -n %{srcname}-%{version}

%build
%py2_build
%if %{with_python3}
%py3_build
%endif

%install
%py2_install
%if %{with_python3}
%py3_install
%endif

%if %{with tests}
%check
PYTHONPATH=%{buildroot}%{python2_sitelib} py.test-%{python2_version} -v -k 'not (test_pip_download or test_old_setuptools_fails or test_old_setuptools_allows_with_warnings or test_distlib_setuptools_works)'
%if %{with_python3}
PYTHONPATH=%{buildroot}%{python3_sitelib} py.test-%{python3_version} -v -k 'not (test_pip_download or test_old_setuptools_fails or test_old_setuptools_allows_with_warnings or test_distlib_setuptools_works)'
%endif
%endif

%files -n python2-%{srcname}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{srcname}/
%{python2_sitelib}/%{srcname}-*.egg-info/

%if %{with_python3}
%files -n python%{python3_pkgversion}-%{srcname}
%license LICENSE
%doc README.rst
%{python3_sitelib}/%{srcname}/
%{python3_sitelib}/%{srcname}-*.egg-info/
%endif

%changelog
* Wed Jan 12 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.3.3-2
- enabled python3

* Fri Nov 22 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.3.3-1
- first rpm version
