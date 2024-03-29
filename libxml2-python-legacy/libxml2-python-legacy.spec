# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# this spec is not needed anymore with the current libxml2, as there
# all is built within one spec, same as fedora also does
# !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!


%define name libxml2-python
%define version 2.7.7
%define unmangled_version 2.7.7

Summary: libxml2 package
Name: %{name}
Version: %{version}
Release: 6%{?dist}
Source: libxml2-%{version}.tar.gz
#Source1: %{name}-%{unmangled_version}.tar.gz
License: MIT Licence
Group: Development/Libraries
Prefix: %{_prefix}
Vendor: Daniel Veillard <veillard@redhat.com>
Url: http://xmlsoft.org/python.html

Patch1: libxml2-os2.diff

BuildRequires:  libxml2-devel python-devel 
#BuildRequires:  python-xml
BuildRoot: %{_tmppath}/libxml2-%{version}-%{release}-buildroot

Requires: libxml2 = %{version}
Requires: python
Requires: python(abi) = %{python_version}

%description
The libxml2-python package contains a module that permits applications
written in the Python programming language to use the interface
supplied by the libxml2 library to manipulate XML files.

This library allows manipulation of XML files. It includes support for
reading, modifying, and writing XML and HTML files. There is DTD
support that includes parsing and validation even with complex DTDs,
either at parse time or later once the document has been modified.

%prep
%setup -q -n libxml2-%{unmangled_version}
%patch001 -p1 -b .os2~

%build
cd python
env CFLAGS="$RPM_OPT_FLAGS" python setup.py build

%install
cd python
python setup.py install --root=$RPM_BUILD_ROOT --prefix %{_prefix} --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f python/INSTALLED_FILES
%defattr(-,root,root)

%changelog
* Tue Apr 08 2014 yd
- workaround for http://trac.netlabs.org/rpm/ticket/71

* Mon Apr 07 2014 yd
- build for python 2.7.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
