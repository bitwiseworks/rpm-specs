# Disable automatic bytecompilation. We install only one script and we will
# never "import" it.
%undefine py_auto_byte_compile

Name:           python-rpm-generators
Summary:        Dependency generators for Python RPMs
Version:        10
Release:        1%{?dist}

# Originally all those files were part of RPM, so license is kept here
License:        GPLv2+
Url:            https://src.fedoraproject.org/python-rpm-generators
# Commit is the last change in following files
%dnl Source0:        https://raw.githubusercontent.com/rpm-software-management/rpm/102eab50b3d0d6546dfe082eac0ade21e6b3dbf1/COPYING
Source1:        python.attr
Source2:        pythondist.attr
Source3:        pythondeps.sh
Source4:        pythondistdeps.py

BuildArch:      noarch

%description
%{summary}.

%package -n python3-rpm-generators
Summary:        %{summary}
Requires:       python3-setuptools
# The point of split
Conflicts:      rpm-build < 4.13.0.1-2
# Breaking change, change a way how depgen is enabled
Conflicts:      python-rpm-macros < 3-35

%description -n python3-rpm-generators
%{summary}.

%prep
%setup -c -T
cp -a %{sources} .

%install
install -Dpm0644 -t %{buildroot}%{_fileattrsdir} python.attr pythondist.attr
install -Dpm0755 -t %{buildroot}%{_rpmconfigdir} pythondeps.sh pythondistdeps.py

%files -n python3-rpm-generators
%dnl %license COPYING
%{_fileattrsdir}/python.attr
%{_fileattrsdir}/pythondist.attr
%{_rpmconfigdir}/pythondeps.sh
%{_rpmconfigdir}/pythondistdeps.py

%changelog
* Fri May 02 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> - 10-1
- first OS/2 rpm
