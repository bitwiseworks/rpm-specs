%global modname appdirs
%global build_wheel 0
%global with_python3 1
%global with_test 0

%global python2_wheelname %{modname}-%{version}-py2.py3-none-any.whl
%global python3_wheelname %python2_wheelname

Name:          python-%{modname}
Version:       1.4.3
Release:       2%{?dist}
Summary:       Python module for determining platform-specific directories

License:       MIT
URL:           http://github.com/ActiveState/appdirs
Vendor:        bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{modname}-os2 %{version}-os2

BuildRequires: python2-devel
BuildRequires: python2-setuptools
%if 0%{?with_python3}
BuildRequires: python3-devel
#BuildRequires: python3-setuptools
%endif
BuildArch:     noarch

%if 0%{?build_wheel}
BuildRequires:  python2-pip
BuildRequires:  python-wheel
BuildRequires:  python%{python3_pkgversion}-pip
BuildRequires:  python%{python3_pkgversion}-wheel
%endif

%description
A small Python module for determining appropriate " + " platform-specific
directories, e.g. a "user data dir".

%package -n python2-%{modname}
Summary:       Python 2 module for determining platform-specific directoriess
%{?python_provide:%python_provide python2-%{modname}}

%description -n python2-%{modname}
A small Python 2 module for determining appropriate " + " platform-specific
directories, e.g. a "user data dir".

%if 0%{?with_python3}
%package -n python3-%{modname}
Summary:       Python 3 module for determining platform-specific directoriess
%{?python_provide:%python_provide python3-%{modname}}

%description -n python3-%{modname}
A small Python 3 module for determining appropriate " + " platform-specific
directories, e.g. a "user data dir".
%endif

%prep
%scm_setup
rm -rf %{modname}.egg-info

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

sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{python2_sitelib}/%{modname}.py
%if 0%{?with_python3}
sed -i -e '1{\@^#!/usr/bin/env python@d}' %{buildroot}%{python3_sitelib}/%{modname}.py
%endif

%check
%if 0%{?with_test}
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif
%endif

%files -n python2-%{modname}
%license LICENSE.txt
%doc README.rst CHANGES.rst
%{python2_sitelib}/%{modname}*

%if 0%{?with_python3}
%files -n python3-%{modname}
%license LICENSE.txt
%doc README.rst CHANGES.rst
%{python3_sitelib}/%{modname}*
%{python3_sitelib}/__pycache__/%{modname}.*
%endif

%changelog
* Tue Jan 11 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.3-2
- enabled python3

* Thu Apr 13 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.3-1
- update to version 1.4.3
- moved source to github

* Mon Feb 27 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.0-1
- first rpm version (internal version only)
