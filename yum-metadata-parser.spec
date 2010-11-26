
Summary: A fast metadata parser for yum
Name: yum-metadata-parser
Version: 1.1.4
Release: 2%{?dist}
Source0: %{name}-%{version}.tar.gz
License: GPL
Group: Development/Libraries
URL: http://devel.linux.duke.edu/cgi-bin/viewcvs.cgi/yum-metadata-parser/
Requires: yum >= 2.6.2
BuildRequires: python-devel
BuildRequires: glib2-devel
BuildRequires: libxml2-devel
BuildRequires: sqlite-devel
BuildRequires: pkgconfig
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Requires: sqlite, glib2, libxml2

%description
Fast metadata parser for yum implemented in C.

%prep
%setup

%build
%{__python} setup.py build

%install
%{__python} setup.py install -O1 --root=%{buildroot}

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc README AUTHORS ChangeLog
%{_libdir}/*


%changelog
