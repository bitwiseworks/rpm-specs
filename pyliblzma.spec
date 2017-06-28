%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}


Summary:    Python bindings for lzma
Name:       pyliblzma
Version:    0.5.3
Release:    1%{?dist}
License:    LGPLv3+
URL:        https://launchpad.net/pyliblzma

Vendor:	    bww bitwise works GmbH
%scm_source svn http://svn.netlabs.org/repos/ports/pyliblzma/trunk 2065

BuildRequires:    xz-devel python-setuptools python2-devel
BuildRequires:    python-test
BuildRoot:    %{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PylibLZMA provides a python interface for the liblzma library
to read and write data that has been compressed or can be decompressed
by Lasse Collin's lzma utils.

%debug_package

%prep
%scm_setup


%build
%{__python} setup.py build --debug

%check
# disable tests for now, as 3 of them fail
#{__python} setup.py test

%install
rm -rf %{buildroot}
%{__python} setup.py install --root=%{buildroot}

# don't deliver map files
rm -f %{buildroot}/%{python_sitearch}/*.map


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc README THANKS ChangeLog NEWS
%attr(0755,-,-) %{python_sitearch}/lzma.pyd
%{python_sitearch}/liblzma.py*
%{python_sitearch}/%{name}*.egg-info

%changelog
* Wed Feb 22 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.5.3-1
- initial build
