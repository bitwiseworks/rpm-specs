%{?filter_setup:
%filter_provides_in %{python3_sitearch}/.*\.so$
%filter_setup
}

Summary:       Python bindings for CUPS
Name:          python-cups
Version:       2.0.4
Release:       1%{?dist}
# older URL, but still with useful information about pycups
#URL:           http://cyberelk.net/tim/software/pycups/
URL:           https://github.com/OpenPrinting/pycups/
%if !0%{?os2_version}
Source:        https://github.com/OpenPrinting/pycups/releases/download/v%{version}/pycups-%{version}.tar.gz
%else
Vendor:        bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/pycups-os2 v%{version}-os2
%endif
License:       GPL-2.0-or-later

# all taken from upstream
%if !0%{?os2_version}
Patch01: 0001-examples-cupstree.py-remove-shebang.patch
Patch02: 0001-postscriptdriver.prov-ignore-driverless-utilities.patch
Patch03: pycups-invalid-pointer.patch
Patch04: pycups-pyssizet_clean.patch
%endif

# gcc is no longer in buildroot by default
BuildRequires: gcc
# for autosetup
BuildRequires: git-core
# uses make
BuildRequires: make

BuildRequires: cups-devel
BuildRequires: python3-devel
# distutils are removed from python3 project, use the one
# from setuptools
BuildRequires: python3-setuptools

%description
This package provides Python bindings for CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

%package -n python3-cups
Summary:       Python3 bindings for CUPS API, known as pycups.
%{?python_provide:%python_provide python3-cups}

%description -n python3-cups
This package provides Python 3 bindings for CUPS API,
known as pycups. It was written for use with
system-config-printer, but can be put to other uses as well.

%package doc
Summary:       Documentation for python-cups

%description doc
Documentation for python-cups.

%prep
%if !0%{?os2_version}
%autosetup -S git -n pycups-%{version}
%else
%scm_setup
%endif

%build
%if 0%{?os2_version}
export VENDOR="%{vendor}"
export LDFLAGS="-Zomf -Zhigh-mem -lcx -lpthread"
%endif
%py3_build

%install
make install-rpmhook DESTDIR="%{buildroot}"
%py3_install
export PYTHONPATH=%{buildroot}%{python3_sitearch}
%{__python3} -m pydoc -w cups
%{_bindir}/mkdir html
%{_bindir}/mv cups.html html

%files -n python3-cups
%doc README NEWS TODO
%license COPYING
%if !0%{?os2_version}
%{python3_sitearch}/cups.cpython-3*.so
%else
%{python3_sitearch}/cups.pyd
%endif
%{python3_sitearch}/pycups*.egg-info
%{_rpmconfigdir}/fileattrs/psdriver.attr
%{_rpmconfigdir}/postscriptdriver.prov

%files doc
%doc examples html

%changelog
* Wed May 14 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.4-1
- rebuild with python 3.13
- update to latest version

* Wed Jan 24 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.0.1-1
- first OS/2 rpm

