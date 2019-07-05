Name:           liboauth
Version:        1.0.0
Release:        1%{?dist}
Summary:        OAuth library functions

Group:          System Environment/Libraries
License:        MIT
URL:            http://liboauth.sourceforge.net/
Source0:        http://liboauth.sourceforge.net/pool/liboauth-%{version}.tar.gz
Patch0:         liboauth-os2.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildRequires:  curl-devel nss-devel
#Requires:       

%description
liboauth is a collection of POSIX-c functions implementing the OAuth
Core RFC 5849 standard. liboauth provides functions to escape and
encode parameters according to OAuth specification and offers
high-level functionality to sign requests or verify OAuth signatures
as well as perform HTTP requests.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
%if 0%{?el5}
Requires:       pkgconfig curl-devel nss-devel
%endif

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q
%patch0 -p1 -b .os2~


%build
export CONFIG_SHELL="/@unixroot/usr/bin/sh.exe"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lurpo -lmmap"
%configure \
    --disable-static \
    --enable-nss \
    "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_libdir}/*.a

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING.MIT README 
%{_libdir}/*.dll

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_libdir}/*.lib
%{_libdir}/pkgconfig/oauth.pc
%{_mandir}/man3/oauth.*


%changelog
* Fri Dec 28 2012 yd
- initial build.
