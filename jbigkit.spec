Name:           jbigkit
Version:        2.1
Release:        1%{?dist}
Summary:        JBIG1 lossless image compression tools

Group:          Development/Libraries
License:        GPLv2+
URL:            http://www.cl.cam.ac.uk/~mgk25/jbigkit/
Vendor:         bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/jbigkit-os2 master

Requires:       jbigkit-libs% = %{version}-%{release}

%package libs
Summary:        JBIG1 lossless image compression library
Group:          Development/Libraries

%package devel
Summary:        JBIG1 lossless image compression library -- development files
Group:          Development/Libraries
Requires:       jbigkit-libs% = %{version}-%{release}

%description libs
JBIG-KIT provides a portable library of compression and decompression
functions with a documented interface that you can include very easily
into your image or document processing software. In addition, JBIG-KIT
provides ready-to-use compression and decompression programs with a
simple command line interface (similar to the converters found in netpbm).

JBIG-KIT implements the specification:
    ISO/IEC 11544:1993 and ITU-T Recommendation T.82(1993):
     Information technology  Coded representation of picture and audio
     information  Progressive bi-level image compression 

which is commonly referred to as the JBIG1 standard

%description devel
The jbigkit-devel package contains files needed for development using 
the JBIG-KIT image compression library.

%description
The jbigkit package contains tools for converting between PBM and JBIG1
formats.


%debug_package

%prep
%scm_setup

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
make %{?_smp_mflags}

%install
mkdir -p $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_includedir}
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

install -p -m0755 libjbig/jbig.dll $RPM_BUILD_ROOT/%{_libdir}
install -p -m0755 libjbig/jbig85.dll $RPM_BUILD_ROOT/%{_libdir}

install -p -m0755 libjbig/libjbig.a $RPM_BUILD_ROOT/%{_libdir}
install -p -m0755 libjbig/libjbig85.a $RPM_BUILD_ROOT/%{_libdir}

install -p -m0644 libjbig/jbig.h $RPM_BUILD_ROOT%{_includedir}
install -p -m0644 libjbig/jbig85.h $RPM_BUILD_ROOT%{_includedir}
install -p -m0644 libjbig/jbig_ar.h $RPM_BUILD_ROOT%{_includedir}

install -p -m0755 pbmtools/???to???.exe $RPM_BUILD_ROOT%{_bindir}
install -p -m0755 pbmtools/???to???85.exe $RPM_BUILD_ROOT%{_bindir}
install -p -m0644 pbmtools/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%check
# remember to set beginlibpath by hand for now, as dash doesn't do it so far
# as soon as it's fixed the below line will work
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/libjbig
make test

#%post libs -p /sbin/ldconfig

#%postun libs -p /sbin/ldconfig

%files
%{_bindir}/???to*.exe
%{_mandir}/man1/*
%doc COPYING

%files libs
%{_libdir}/jbig*.dll
%doc COPYING ANNOUNCE TODO CHANGES

%files devel
%{_libdir}/libjbig*.a
%{_includedir}/jbig*.h

%changelog
* Tue Nov 28 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.1-1
- initial rpm build
