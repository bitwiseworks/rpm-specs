Name:		json-c
Version:	0.10
Release:	2%{?dist}
Summary:	A JSON implementation in C
Group:		Development/Libraries
License:	MIT
URL:		http://oss.metaparadigm.com/json-c/
Source0:	http://oss.metaparadigm.com/json-c/json-c-%{version}.tar.gz
Patch0:         json-c-os2.patch
Source1:        json-c-libtool.os2

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)


%description
JSON-C implements a reference counting object model that allows you to easily
construct JSON objects in C, output them as JSON formatted strings and parse
JSON formatted strings back into the C representation of JSON objects.

%package devel
Summary:	Development headers and library for json-c
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	pkgconfig

%description devel
This package contains the development headers and library for json-c.


%package doc
Summary:	Reference manual for json-c
Group:		Documentation
BuildArch:	noarch

%description doc
This package contains the reference manual for json-c.

%prep
%setup -q
%patch0 -p1 -b .os2~
cp %{SOURCE1} libtool.os2


%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
%configure \
    --enable-shared --disable-static \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Get rid of la files
rm -rf %{buildroot}%{_libdir}/*.la
rm -rf %{buildroot}%{_libdir}/*.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING NEWS README README.html
%{_libdir}/*.dll

%files devel
%defattr(-,root,root,-)
%{_includedir}/json/
%{_libdir}/*.lib
%{_libdir}/pkgconfig/json.pc

%files doc
%defattr(-,root,root,-)
%doc doc/html/*

%changelog
* Sat Dec 29 2012 yd
- add object iterator to library, reduce exports to API only.

* Fri Dec 28 2012 yd
- initial build.
