#define svn_url     e:/trees/libspectre/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/libspectre/trunk
%define svn_rev     1691

Name:           libspectre
Version:        0.2.8
Release:        1%{?dist}
Summary:        A library for rendering PostScript(TM) documents

Group:          System Environment/Libraries
License:        GPLv2+
URL:            http://libspectre.freedesktop.org
Vendor:         bww bitwise works GmbH
Source:         %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: ghostscript-devel >= 8.61

%description
%{name} is a small library for rendering PostScript(TM) documents.
It provides a convenient easy to use API for handling and rendering
PostScript documents.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       pkgconfig


%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%debug_package


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
export LDFLAGS="-Zhigh-mem"
# we do autoreconf even fedora doesn't do it
autoreconf -fiv

%configure --disable-static --enable-shared
make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT


#post -p /sbin/ldconfig

#postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING AUTHORS NEWS README TODO
%{_libdir}/spectre*.dll

%files devel
%defattr(-,root,root,-)
%{_includedir}/libspectre/
%{_libdir}/spectre*_dll.a
%{_libdir}/pkgconfig/libspectre.pc


%changelog
* Tue Sep 06 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.2.8-1
- initial version
