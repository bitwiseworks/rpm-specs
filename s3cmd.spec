%define name s3cmd
%define version 1.1.0.beta3
%define unmangled_version 1.1.0.beta3
%define release 5

Summary: Command line tool for managing Amazon S3 and CloudFront services
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{unmangled_version}.tar.gz
License: GPL version 2
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-buildroot
Prefix: %{_prefix}
BuildArch: noarch
Vendor: Michal Ludvig <michal@logix.cz>
Url: http://s3tools.org

%description


S3cmd lets you copy files from/to Amazon S3 
(Simple Storage Service) using a simple to use
command line client. Supports rsync-like backup,
GPG encryption, and more. Also supports management
of Amazon's CloudFront content delivery network.


Authors:
--------
    Michal Ludvig  <michal@logix.cz>


%prep
%setup -n %{name}-%{unmangled_version}

%build
python setup.py build

%install
python setup.py install --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES
# temporary workaround for wrong paths http://trac.netlabs.org/rpm/ticket/71
mkdir $RPM_BUILD_ROOT/@unixroot
mv $RPM_BUILD_ROOT/USR $RPM_BUILD_ROOT/@unixroot/usr
sed -e 's#/USR/#/@unixroot/usr/#g' -i INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Tue Apr 08 2014 yd
- workaround for http://trac.netlabs.org/rpm/ticket/71

* Mon Apr 07 2014 yd
- build for python 2.7.
