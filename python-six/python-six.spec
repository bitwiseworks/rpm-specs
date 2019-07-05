# Note: this .spec is borrowed from http://pkgs.fedoraproject.org/cgit/rpms/python-six.git/tree/python-six.spec
# and adapted to our needs

%global modname six

# remove the comment below, when we have python3 support
#global with_python3 1


%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-%{modname}
Version:        1.10.0
Release:        1%{?dist}
Summary:        Python 2 and 3 compatibility utilities

Group:          Development/Languages
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
BuildRequires:  python2-devel
#BuildRequires:  python2-setuptools
# Testing
#BuildRequires:  python2-pytest
#BuildRequires:  tkinter
Provides:       python-six = %{version}-%{release}

%description -n python2-%{modname} %{_description}

Python 2 version.

%if 0%{?with_python3}
%package -n python3-%{modname}
Summary:        %{summary}
%{?system_python_abi}
%{?python_provide:%python_provide python3-%{modname}}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
# Testing
BuildRequires:  python3-pytest
BuildRequires:  python3-tkinter

%description -n python3-%{modname} %{_description}

Python 3 version.
%endif

%prep
%setup -q -n six-%{version}

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%if 0%{?with_python3}
%py3_build
%endif

%install
%if 0%{?with_python3}
%py3_install
%endif
%{__python} setup.py install -O1 --skip-build --root $RPM_BUILD_ROOT


%check
# @todo enable once we got python-unittest
#py.test-2 -rfsxX test_six.py

%if 0%{?with_python3}
py.test-3 -rfsxX test_six.py
%endif


%files -n python2-%{modname}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README documentation/index.rst
%{python_sitearch}/%{modname}.py*
%{python_sitearch}/%{modname}-*.egg-info

%if 0%{?with_python3}
%files -n python3-%{modname}
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README documentation/index.rst
%{python3_sitelib}/%{modname}-*.egg-info/
%{python3_sitelib}/%{modname}.py
%{python3_sitelib}/__pycache__/%{modname}.*
%endif

%changelog
* Thu Oct 27 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.10.0-1
- Initial package of version 1.10.0.
