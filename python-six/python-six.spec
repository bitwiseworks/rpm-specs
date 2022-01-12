%global modname six

Name:           python-%{modname}
Version:        1.10.0
Release:        2%{?dist}
Summary:        Python 2 and 3 compatibility utilities

License:        MIT
URL:            https://pypi.python.org/pypi/six
Vendor:		bww bitwise works GmbH
Source0:        https://files.pythonhosted.org/packages/source/%(n=%{modname}; echo ${n:0:1})/%{modname}/%{modname}-%{version}.tar.gz

BuildArch:	noarch

%global _description \
%%{name} provides simple utilities for wrapping over differences between\
Python 2 and Python 3.


%description %{_description}

%package -n python2-%{modname}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{modname}}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
# Testing
#BuildRequires:  python2-pytest
#BuildRequires:  tkinter

%description -n python2-%{modname} %{_description}

Python 2 version.

%package -n python3-%{modname}
Summary:        %{summary}
%{?system_python_abi}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
#BuildRequires:  python3-setuptools
# Testing
#BuildRequires:  python3-pytest
#BuildRequires:  python3-tkinter

%description -n python3-%{modname} %{_description}

Python 3 version.

%prep
%setup -q -n six-%{version}

%build
%py2_build
%py3_build

%install
%py2_install
%py3_install

%check
# @todo enable once we got python-unittest
#py.test-2 -rfsxX test_six.py
#py.test-3 -rfsxX test_six.py


%files -n python2-%{modname}
%license LICENSE
%doc README documentation/index.rst
%{python2_sitelib}/%{modname}-*.egg-info/
%{python2_sitelib}/%{modname}.py*

%files -n python3-%{modname}
%license LICENSE
%doc README documentation/index.rst
%{python3_sitelib}/%{modname}-*.egg-info
%{python3_sitelib}/%{modname}.py
%{python3_sitelib}/__pycache__/%{modname}.*

%changelog
* Tue Jan 11 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.10.0-2
- clean up spec a bit
- enable python3 version

* Thu Oct 27 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.10.0-1
- Initial package of version 1.10.0.
