%scm_source  github https://github.com/ydario/libgd gd-2.2.5-os2

Summary:       A graphics library for quick creation of PNG or JPEG images
Name:          gd
Version:       2.2.5
Release:       1
License:       MIT
URL:           http://libgd.github.io/

BuildRequires: freetype-devel
BuildRequires: fontconfig-devel
BuildRequires: gettext-devel
BuildRequires: libjpeg-devel
BuildRequires: libpng-devel
BuildRequires: zlib-devel
BuildRequires: pkgconfig
BuildRequires: libtool


%description
The gd graphics library allows your code to quickly draw images
complete with lines, arcs, text, multiple colors, cut and paste from
other images, and flood fills, and to write out the result as a PNG or
JPEG file. This is particularly useful in Web applications, where PNG
and JPEG are two of the formats accepted for inline images by most
browsers. Note that gd is not a paint program.


%package progs
Requires:       %{name} = %{version}-%{release}
Summary:        Utility programs that use libgd

%description progs
The gd-progs package includes utility programs supplied with gd, a
graphics library for creating PNG and JPEG images.


%package devel
Summary:  The development libraries and header files for gd
Requires: %{name} = %{version}-%{release}
Requires: freetype-devel
Requires: fontconfig-devel
Requires: libjpeg-devel
Requires: libpng-devel
Requires: libtiff-devel
Requires: zlib-devel

%description devel
The gd-devel package contains the development libraries and header
files for gd, a graphics library for creating PNG and JPEG graphics.


%prep
%scm_setup
autoreconf -i -v

%build
export LIBS="-lpthread"
%configure
make %{?_smp_mflags}


%install
make install INSTALL='install -p' DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.la
rm -f $RPM_BUILD_ROOT/%{_libdir}/libgd.a


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_libdir}/*.dll

%files progs
%{_bindir}/*
%exclude %{_bindir}/gdlib-config

%files devel
%{_bindir}/gdlib-config
%{_includedir}/*
%{_libdir}/*.a
%{_libdir}/pkgconfig/gdlib.pc


%changelog
