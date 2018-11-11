# Conformance tests disabled by default since it requires 1 GB of test data
#global runcheck 1

#global optional_components 1

Name:           openjpeg2
Version:        2.3.0
Release:        1%{?dist}
Summary:        C-Library for JPEG 2000

# windirent.h is MIT, the rest is BSD
License:        BSD and MIT
URL:            https://github.com/uclouvain/openjpeg
Vendor: bww bitwise works GmbH
#scm_source github http://github.com/bitwiseworks/openjpeg-os2 master-os2
%scm_source git E:/Trees/openjpeg/git master-os2
%if 0%{?runcheck}
# git clone git@github.com:uclouvain/openjpeg-data.git
Source1:        data.tar.xz
%endif


BuildRequires:  cmake
# The library itself is C only, but there is some optional C++ stuff, hence the project is not marked as C-only in cmake and hence cmake looks for a c++ compiler
#BuildRequires:  gcc-c++
BuildRequires:  gcc
BuildRequires:  make
BuildRequires:  zlib-devel
BuildRequires:  libpng-devel
BuildRequires:  libtiff-devel
BuildRequires:  lcms2-devel
BuildRequires:  doxygen

%if 0%{?optional_components}
BuildRequires:  java-devel
BuildRequires:  xerces-j2
%endif

%description
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains
* JPEG 2000 codec compliant with the Part 1 of the standard (Class-1 Profile-1
  compliance).
* JP2 (JPEG 2000 standard Part 2 - Handling of JP2 boxes and extended multiple
  component transforms for multispectral and hyperspectral imagery)


%package devel
Summary:        Development files for OpenJPEG 2
Requires:       %{name} = %{version}-%{release}
# OpenJPEGTargets.cmake refers to the tools
Requires:       %{name}-tools = %{version}-%{release}

%description devel
The %{name}-devel package contains libraries and header files for developing
applications that use OpenJPEG 2.


%package devel-docs
Summary:        Developer documentation for OpenJPEG 2
BuildArch:      noarch

%description devel-docs
The %{name}-devel-docs package contains documentation files for developing
applications that use OpenJPEG 2.


%package tools
Summary:        OpenJPEG 2 command line tools
Requires:       %{name} = %{version}-%{release}

%description tools
Command line tools for JPEG 2000 file manipulation, using OpenJPEG2:
 * opj2_compress
 * opj2_decompress
 * opj2_dump

%if 0%{?optional_components}
##### MJ2 #####

%package mj2
Summary:        OpenJPEG2 MJ2 module
Requires:       %{name} = %{version}-%{release}

%description mj2
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the MJ2 module (JPEG 2000 standard Part 3)


%package mj2-devel
Summary:        Development files for OpenJPEG2 MJ2 module
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-mj2 = %{version}-%{release}

%description mj2-devel
Development files for OpenJPEG2 MJ2 module


%package mj2-tools
Summary:        OpenJPEG2 MJ2 module command line tools
Requires:       %{name}-mj2 = %{version}-%{release}

%description mj2-tools
OpenJPEG2 MJ2 module command line tools

##### JPWL #####

%package jpwl
Summary:        OpenJPEG2 JPWL module
Requires:       %{name} = %{version}-%{release}

%description jpwl
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JPWL (JPEG 2000 standard Part 11 - Jpeg 2000 Wireless)


%package jpwl-devel
Summary:        Development files for OpenJPEG2 JPWL module
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-jpwl = %{version}-%{release}

%description jpwl-devel
Development files for OpenJPEG2 JPWL module


%package jpwl-tools
Summary:        OpenJPEG2 JPWL module command line tools
Requires:       %{name}-jpwl = %{version}-%{release}

%description jpwl-tools
OpenJPEG2 JPWL module command line tools

##### JPIP #####

%package jpip
Summary:        OpenJPEG2 JPIP module
Requires:       %{name} = %{version}-%{release}

%description jpip
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JPWL (JPEG 2000 standard Part 9 - Jpeg 2000 Interactive Protocol)


%package jpip-devel
Summary:        Development files for OpenJPEG2 JPIP module
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-jpwl = %{version}-%{release}

%description jpip-devel
Development files for OpenJPEG2 JPIP module


%package jpip-tools
Summary:        OpenJPEG2 JPIP module command line tools
Requires:       %{name}-jpip = %{version}-%{release}
Requires:       jpackage-utils
Requires:       java

%description jpip-tools
OpenJPEG2 JPIP module command line tools

##### JP3D #####

%package jp3d
Summary:        OpenJPEG2 JP3D module
Requires:       %{name} = %{version}-%{release}

%description jp3d
The OpenJPEG library is an open-source JPEG 2000 library developed in order to
promote the use of JPEG 2000.

This package contains the JP3D (JPEG 2000 standard Part 10 - Jpeg 2000 3D)


%package jp3d-devel
Summary:        Development files for OpenJPEG2 JP3D module
Requires:       %{name}-devel = %{version}-%{release}
Requires:       %{name}-jp3d = %{version}-%{release}

%description jp3d-devel
Development files for OpenJPEG2 JP3D module


%package jp3d-tools
Summary:        OpenJPEG2 JP3D module command line tools
Requires:       %{name}-jp3d = %{version}-%{release}

%description jp3d-tools
OpenJPEG2 JP3D module command line tools
%endif

%debug_package


%prep
%scm_setup

# Remove all third party libraries just to be sure
#rm -rf thirdparty


%build
export LDFLAGS="-Zhigh-mem -Zomf -lcx"
export VENDOR="%{vendor}"

mkdir build
cd build
# TODO: Consider
# -DBUILD_JPIP_SERVER=ON -DBUILD_JAVA=ON
%cmake -DCMAKE_BUILD_TYPE=RelWithDebInfo -DOPENJPEG_INSTALL_LIB_DIR=%{_lib} \
    %{?optional_components:-DBUILD_MJ2=ON -DBUILD_JPWL=ON -DBUILD_JPIP=ON -DBUILD_JP3D=ON} \
    -DBUILD_DOC=ON \
    -DBUILD_STATIC_LIBS=OFF \
    -DBUILD_SHARED_LIBS=ON \
    %{?runcheck:-DBUILD_TESTING:BOOL=ON -DOPJ_DATA_ROOT=$PWD/../data} \
    ..
cd ..

make VERBOSE=1 -C build


%install
%make_install -C build


# Docs are installed through %%doc
rm -rf %{buildroot}%{_datadir}/doc/

%if 0%{?optional_components}
# Move the jar to the correct place
mkdir -p %{buildroot}%{_javadir}
mv %{buildroot}%{_datadir}/opj_jpip_viewer.jar %{buildroot}%{_javadir}/opj2_jpip_viewer.jar
cat > %{buildroot}%{_bindir}/opj2_jpip_viewer <<EOF
java -jar %{_javadir}/opj2_jpip_viewer.jar "$@"
EOF
chmod +x %{buildroot}%{_bindir}/opj2_jpip_viewer
%endif


#%ldconfig_scriptlets


%check
%if 0%{?runcheck}
make test -C build
%endif


%files
%{!?_licensedir:%global license %doc}
%license LICENSE
%doc AUTHORS.md NEWS.md README.md THANKS.md
%{_libdir}/openjp*.dll
%{_mandir}/man3/libopenjp2.3*

%files devel
%dir %{_includedir}/openjpeg-2.3/
%{_includedir}/openjpeg-2.3/openjpeg.h
%{_includedir}/openjpeg-2.3/opj_config.h
%{_includedir}/openjpeg-2.3/opj_stdint.h
%{_libdir}/openjp*_dll.a
%{_libdir}/openjpeg-2.3/
%{_libdir}/pkgconfig/libopenjp2.pc

%files devel-docs
%doc build/doc/html

%files tools
%{_bindir}/opj_compress.exe
%{_bindir}/opj_decompress.exe
%{_bindir}/opj_dump.exe
%{_mandir}/man1/opj_compress.1*
%{_mandir}/man1/opj_decompress.1*
%{_mandir}/man1/opj_dump.1*

%if 0%{?optional_components}
%files mj2
%{_libdir}/libopenmj2.so.*

%files mj2-devel
%{_libdir}/libopenmj2.so

%files mj2-tools
%{_bindir}/opj2_mj2*

%files jpwl
%{_libdir}/libopenjpwl.so.*

%files jpwl-devel
%{_libdir}/libopenjpwl.so
%{_libdir}/pkgconfig/libopenjpwl.pc

%files jpwl-tools
%{_bindir}/opj2_jpwl*

%files jpip
%{_libdir}/libopenjpip.so.*

%files jpip-devel
%{_libdir}/libopenjpip.so
%{_libdir}/pkgconfig/libopenjpip.pc

%files jpip-tools
%{_bindir}/opj2_jpip*
%{_bindir}/opj2_dec_server
%{_javadir}/opj2_jpip_viewer.jar

%files jp3d
%{_libdir}/libopenjp3d.so.*

%files jp3d-devel
%{_includedir}/openjpeg-2.0/openjp3d.h
%{_libdir}/libopenjp3d.so
%{_libdir}/pkgconfig/libopenjp3d.pc

%files jp3d-tools
%{_bindir}/opj2_jp3d*
%endif


%changelog
* Fri Nov 2 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.3.0-1
- initial port
