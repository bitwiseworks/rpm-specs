# Based on http://pkgs.fedoraproject.org/cgit/rpms/tig.git/tree/tig.spec?id=5d56685605a3a91f698586130cdd619652b49add

%global modname dateutil

Name:           python-%{modname}
Version:        2.6.0
Release:        1%{?dist}
Summary:        Powerful extensions to the standard datetime module

Group:          Development/Languages
License:        Python
URL:            https://github.com/dateutil/dateutil
Source0:        https://github.com/dateutil/dateutil/archive/%{version}/%{modname}-%{version}.tar.gz

BuildArch:      noarch
#BuildRequires:  python-sphinx

%description
The dateutil module provides powerful extensions to the standard datetime
module available in Python 2.3+.

This is the version for Python 2.

%package doc
Summary: API documentation for python-dateutil
%description doc
This package contains %{summary}.

%prep
%autosetup -p0 -n python-%{modname}-%{version}
#iconv --from=ISO-8859-1 --to=UTF-8 NEWS > NEWS.new
#mv NEWS.new NEWS

%build
%{__python} setup.py build
#make -C docs html

%install
%{__python} setup.py install --skip-build --root $RPM_BUILD_ROOT

%check
#%{__python} setup.py test

%files -n python-%{modname}
%license LICENSE
%doc NEWS README.rst
%{python_sitelib}/%{modname}/
%{python_sitelib}/*.egg-info

#%files doc
#%license LICENSE
#%doc docs/_build/html

%changelog
* Wed May 10 2017 yd <yd@os2power.com> 2.6.0-1
- first public build.
