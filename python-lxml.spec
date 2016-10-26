# Note: this .spec is borrowed from http://pkgs.fedoraproject.org/cgit/rpms/python-lxml.git/tree/python-lxml.spec
# and adapted to our needs

%global pypi_name lxml

# remove the comment below, when we have python3 support
#global with_python3 1


%{!?python_sitearch: %global python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Name:           python-%{pypi_name}
Version:        3.6.4
Release:        1%{?dist}
Summary:        Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API

Group:          Development/Libraries
License:        BSD
URL:            http://lxml.de
Vendor:		bww bitwise works GmbH
Source0:        https://files.pythonhosted.org/packages/source/l/%{pypi_name}/%{pypi_name}-%{version}.tar.gz

BuildRequires:  libxml2-devel
BuildRequires:  libxslt-devel

BuildRequires:  python2-devel

%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%endif

%description
lxml is a Pythonic, mature binding for the libxml2 and libxslt libraries. It
provides safe and convenient access to these libraries using the ElementTree It
extends the ElementTree API significantly to offer support for XPath, RelaxNG,
XML Schema, XSLT, C14N and much more.To contact the project, go to the project
home page < or see our bug tracker at case you want to use the current ...

%package -n     python2-%{pypi_name}
Summary:        Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API
#Requires:       python-cssselect
#Requires:       python-html5lib
#Requires:       python-beautifulsoup4
Provides:	python-%{pypi_name}

%description -n python2-%{pypi_name}
lxml is a Pythonic, mature binding for the libxml2 and libxslt libraries. It
provides safe and convenient access to these libraries using the ElementTree It
extends the ElementTree API significantly to offer support for XPath, RelaxNG,
XML Schema, XSLT, C14N and much more.To contact the project, go to the project
home page < or see our bug tracker at case you want to use the current ...

%if 0%{?with_python3}
%package -n	python3-lxml
Summary:        Powerful and Pythonic XML processing library combining libxml2/libxslt with the ElementTree API
Requires:       python3-cssselect
Requires:       python3-html5lib
Requires:       python3-beautifulsoup4
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
lxml is a Pythonic, mature binding for the libxml2 and libxslt libraries. It
provides safe and convenient access to these libraries using the ElementTree It
extends the ElementTree API significantly to offer support for XPath, RelaxNG,
XML Schema, XSLT, C14N and much more.To contact the project, go to the project
home page < or see our bug tracker at case you want to use the current ...
%endif

%prep
%setup -q -n lxml-%{version}

%build
CFLAGS="%{optflags}" %{__python} setup.py build

%if 0%{?with_python3}
%py3_build
%endif

%install
%{__python} setup.py install --skip-build --no-compile --root %{buildroot}

%if 0%{?with_python3}
%py3_install
%endif

%check
# @todo enable once we got python-unittest
#{__python2} setup.py test

%if 0%{?with_python3}
%{__python3} setup.py test
%endif


%files -n python2-%{pypi_name}
%{!?_licensedir:%global license %%doc}
%license LICENSES.txt
%license doc/licenses/ZopePublicLicense.txt LICENSES.txt
%doc README.rst src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/readme.txt
%{python_sitearch}/%{pypi_name}
%{python_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license doc/licenses/ZopePublicLicense.txt LICENSES.txt
%doc README.rst src/lxml/isoschematron/resources/xsl/iso-schematron-xslt1/readme.txt
%{python3_sitearch}/%{pypi_name}
%{python3_sitearch}/%{pypi_name}-%{version}-py?.?.egg-info
%endif

%changelog
* Wed Oct 26 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> 3.6.4-1
- Update package to version 3.6.4.

* Sat Dec 12 2015 Dmitriy Kuminov <coding@dmik.org> 3.5.0-1
- Initial package for version 3.5.0.
