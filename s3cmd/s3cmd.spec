
%define name s3cmd
%define version 1.6.1
%define unmangled_version 1.6.1
%define release 1

Summary: Command line tool for managing Amazon S3 and CloudFront services
Name: %{name}
Version: %{version}
Release: %{release}%{?dist}
Source0: %{name}-%{unmangled_version}.tar.gz
Source1: python-wrapper.zip

License: GPL version 2
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
Vendor: Michal Ludvig <michal@logix.cz>
Url: http://s3tools.org

Requires: python(abi) = %{python_version}

%description


S3cmd lets you copy files from/to Amazon S3 
(Simple Storage Service) using a simple to use
command line client. Supports rsync-like backup,
GPG encryption, and more. Also supports management
of Amazon's CloudFront content delivery network.


Authors:
--------
    Michal Ludvig  <michal@logix.cz>


%debug_package


%prep
%setup -n %{name}-%{unmangled_version} -a 1

%build
python setup.py build

%install
S3CMD_PACKAGING=Yes python setup.py install --root=$RPM_BUILD_ROOT --prefix %{_prefix} --record=INSTALLED_FILES
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -m 644 s3cmd.1 $RPM_BUILD_ROOT%{_mandir}/man1

#build exe wrapper
gcc -g -Zomf %optflags -DPYTHON_EXE=\"python%{python_version}.exe\" -o $RPM_BUILD_ROOT/%{_bindir}/%{name}.exe exec-py.c

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
%{_bindir}/*.exe
%{_mandir}/man1/s3cmd.1*
%doc NEWS README.md

%changelog
* Wed May 10 2017 yd <yd@os2power.com> 1.6.1-1
- update source code to 1.6.1

* Wed Jun 18 2014 yd
- rebuild to fix for http://trac.netlabs.org/rpm/ticket/77

* Tue Apr 08 2014 yd
- workaround for http://trac.netlabs.org/rpm/ticket/71

* Mon Apr 07 2014 yd
- build for python 2.7.
