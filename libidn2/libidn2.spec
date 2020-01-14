Summary:          Library to support IDNA2008 internationalized domain names
Name:             libidn2
Version:          2.3.0
Release:          1%{?dist}
License:          (GPLv2+ or LGPLv3+) and GPLv3+
URL:              https://www.gnu.org/software/libidn/#libidn2

Vendor:           bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

#BuildRequires:    gnupg2
BuildRequires:    gcc
BuildRequires:    gettext
BuildRequires:    libunistring-devel
#Provides:         bundled(gnulib)

%description
Libidn2 is an implementation of the IDNA2008 specifications in RFC
5890, 5891, 5892, 5893 and TR46 for internationalized domain names
(IDN). It is a standalone library, without any dependency on libidn.

%package devel
Summary:          Development files for libidn2
Requires:         %{name} = %{version}-%{release}, pkgconfig

%description devel
The libidn2-devel package contains libraries and header files for
developing applications that use libidn2.

%package -n idn2
Summary:          IDNA2008 internationalized domain names conversion tool
License:          GPLv3+
Requires:         %{name} = %{version}-%{release}
%if 0%{?rhel} && 0%{?rhel} <= 7
Requires(post):   /@unixroot/usr/sbin/install-info
Requires(preun):  /@unixroot/usr/sbin/install-info
%endif

%description -n idn2
The idn2 package contains the idn2 command line tool for testing
IDNA2008 conversions.

%debug_package

%prep
%scm_setup

# we do autoreconf even fedora doesn't do it
autoreconf -fvi

%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
%configure --disable-static
make %{?_smp_mflags}

%install
%make_install

# Clean-up examples for documentation
make -C examples distclean
rm -f examples/Makefile*

# Don't install any libtool .la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# Some file cleanups
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%find_lang %{name}

%check
export BEGINLIBPATH=%{_builddir}/%{buildsubdir}/lib/.libs
make -C tests check

#ldconfig_scriptlets

%if 0%{?rhel} && 0%{?rhel} <= 7
%post -n idn2            
install-info %{_infodir}/%{name}.info.gz %{_infodir}/dir || :            

%preun -n idn2            
if [ $1 = 0 ]; then            
  install-info --delete %{_infodir}/%{name}.info.gz %{_infodir}/dir || :            
fi
%endif

%files -f %{name}.lang
%license COPYING COPYING.LESSERv3 COPYING.unicode COPYINGv2
%doc AUTHORS NEWS README.md
%{_libdir}/*.dll

%files devel
%doc doc/%{name}.html examples
%{_libdir}/*_dll.a
%{_libdir}/pkgconfig/%{name}.pc
%{_includedir}/*.h
%{_mandir}/man3/*
%{_datadir}/gtk-doc/

%files -n idn2
%{_bindir}/idn2.exe
%{_mandir}/man1/idn2.1*
%{_infodir}/%{name}.info*

%changelog
* Mon Jan 13 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.3.0-1
- first OS/2 rpm
