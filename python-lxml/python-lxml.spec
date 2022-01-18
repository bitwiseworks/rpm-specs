%global modname lxml

Name:           python-%{modname}
Version:        4.4.1
Release:        1%{?dist}
Summary:        XML processing library combining libxml2/libxslt with the ElementTree API

License:        BSD
URL:            https://github.com/lxml/lxml
Source0:        https://lxml.de/files/%{modname}-%{version}.tar
%if 0%{?os2_version}
Vendor:         bww bitwise works GmbH
%endif

BuildRequires:  gcc
BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel

%global _description \
lxml is a Pythonic, mature binding for the libxml2 and libxslt libraries. It\
provides safe and convenient access to these libraries using the ElementTree It\
extends the ElementTree API significantly to offer support for XPath, RelaxNG,\
XML Schema, XSLT, C14N and much more.To contact the project, go to the project\
home page < or see our bug tracker at case you want to use the current ...

%description %{_description}

%package -n     python2-%{modname}
Summary:        %{summary}
BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
Suggests:       python%{python2_version}dist(cssselect) >= 0.7
Suggests:       python%{python2_version}dist(html5lib)
Suggests:       python%{python2_version}dist(beautifulsoup4)
%{?python_provide:%python_provide python2-%{modname}}

%description -n python2-%{modname} %{_description}

Python 2 version.

%package -n     python3-%{modname}
Summary:        %{summary}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if !0%{?os2_version}
BuildRequires:  python3-Cython
%endif
Suggests:       python%{python3_version}dist(cssselect) >= 0.7
Suggests:       python%{python3_version}dist(html5lib)
Suggests:       python%{python3_version}dist(beautifulsoup4)
%{?python_provide:%python_provide python3-%{modname}}

%description -n python3-%{modname} %{_description}

Python 3 version.

%prep
%autosetup -n %{modname}-%{version}
%if !0%{?os2_version}
# Remove pregenerated Cython C sources
find -type f -name '*.c' -print -delete
%endif

%build
%if !0%{?os2_version}
env WITH_CYTHON=true %py3_build
%else
%py3_build
%endif
%py2_build

%install
%py2_install
%py3_install

%check
%if !0%{?os2_version}
%{__python2} setup.py test
%{__python3} setup.py test
%endif

%files -n python2-%{modname}
%license doc/licenses/ZopePublicLicense.txt LICENSES.txt
%doc README.rst src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/readme.txt
%{python2_sitearch}/%{modname}/
%{python2_sitearch}/%{modname}-*.egg-info/

%files -n python3-%{modname}
%license doc/licenses/ZopePublicLicense.txt LICENSES.txt
%doc README.rst src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/readme.txt
%{python3_sitearch}/%{modname}/
%{python3_sitearch}/%{modname}-*.egg-info/

%changelog
* Tue Jan 18 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 4.4.1-1
- update to version 4.4.1
- resync with fedora spec

* Fri Nov 25 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.6.4-2
- small spec cleanup
- rebuilt with latest libxslt and libxml2

* Wed Oct 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.6.4-1
- Update package to version 3.6.4.

* Sat Dec 12 2015 Dmitriy Kuminov <coding@dmik.org> 3.5.0-1
- Initial package for version 3.5.0.
