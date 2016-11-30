#define svn_url     e:/trees/libjpeg/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/libjpeg/trunk
%define svn_rev     1848

Summary: A library for manipulating JPEG image format files
Name: libjpeg
Version: 8d
Release: 2%{?dist}
License: IJG
Group: System Environment/Libraries
URL: http://www.ijg.org/

Vendor:  bww bitwise works GmbH
Source:  %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

# DEF files to create forwarders for the legacy package
Source10:       jpeg.def

BuildRequires: autoconf libtool
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

%description
The libjpeg package contains a library of functions for manipulating
JPEG images, as well as simple client programs for accessing the
libjpeg functions.  Libjpeg client programs include cjpeg, djpeg,
jpegtran, rdjpgcom and wrjpgcom.  Cjpeg compresses an image file into
JPEG format.  Djpeg decompresses a JPEG file into a regular image
file.  Jpegtran can perform various useful transformations on JPEG
files.  Rdjpgcom displays any text comments included in a JPEG file.
Wrjpgcom inserts text comments into a JPEG file.

%package devel
Summary: Development tools for programs which will use the libjpeg library
Group: Development/Libraries
Requires: libjpeg = %{version}-%{release}

%description devel
The libjpeg-devel package includes the header files and documentation
necessary for developing programs which will manipulate JPEG files using
the libjpeg library.

If you are going to develop programs which will manipulate JPEG images,
you should install libjpeg-devel.  You'll also need to have the libjpeg
package installed.

%package static
Summary: Static JPEG image format file library
Group: Development/Libraries
Requires: libjpeg-devel = %{version}-%{release}

%description static
The libjpeg-static package contains the statically linkable version of libjpeg.
Linking to static libraries is discouraged for most applications, but it is
necessary for some boot packages.

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

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done

# Hack: disable autoheader so that it doesn't overwrite our cfg template.
export AUTOHEADER="echo autoheader ignored"
autoreconf -vif

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export VENDOR="%{vendor}"
%configure \
     --enable-shared --enable-static

make %{?_smp_mflags}

%check
# this export is needed, as else the dll for the tests are not found
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/.libs
make test

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

#install -m 755 jpeg.dll $RPM_BUILD_ROOT/%{_libdir}
#install -m 755 .libs/jpeg_s.a $RPM_BUILD_ROOT/%{_libdir}

# We don't ship .la files.
rm $RPM_BUILD_ROOT%{_libdir}/*.la

# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib jpeg.def -l$RPM_BUILD_ROOT/%{_libdir}/jpeg8.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/jpeg.dll

%files
%defattr(-,root,root)
%doc usage.txt README
%{_libdir}/jpeg*.dll
%{_bindir}/*.exe
%{_mandir}/*/*

%files devel
%defattr(-,root,root)
%doc libjpeg.txt coderules.txt structure.txt wizard.txt example.c
%{_libdir}/jpeg*_dll.a
%{_includedir}/*.h

%files static
%defattr(-,root,root)
%{_libdir}/jpeg.a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Nov 30 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8d-2
- add -nostdlib to forwarders, to need less heap

* Wed Sep 21 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8d-1
- update to version 8d
- change build part
- add debug files

* Mon Dec 19 2011 yd
- initial build.
