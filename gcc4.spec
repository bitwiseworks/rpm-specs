%global gcc_version 4.4.4

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: 8%{?dist}

# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
URL: http://gcc.gnu.org

Source0: gcc-%{version}-os2-20101229.zip
Source1: gpl.zip
#Source2: gcc-ssp.zip

BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

Obsoletes: gcc < %{gcc_version}
Requires: libgcc444 = %{gcc_version}
Requires: libc-devel >= 0.6.3

%description
The gcc package contains the GNU Compiler Collection version 4.4.
You'll need this package in order to compile C code.

%package -n libgcc444
Summary: GCC version 4.4 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc444
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package stack-protector
Summary: GCC stack protector shared library
Group: System Environment/Libraries

%description stack-protector
This package contains GCC shared library which is needed
for stack protector.

%package wlink
Summary: GCC configuration changes for Watcom linker support.
Group: Development/Languages
Requires: watcom-wlink-hll

%description wlink
This package triggers the required config.sys settings to allow use of Watcom
Linker instead of ld.

%package wrc
Summary: GCC configuration changes for Watcom resource compiler support.
Group: Development/Languages
Requires: watcom-wrc

%description wrc
This package triggers the required config.sys settings to allow use of Watcom
resource compiler instead of IBM one.

%prep
%setup -q -c -a 1

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_usr}
cp -r usr/local444/* %{buildroot}%{_usr}/

mkdir -p %{buildroot}/%_docdir/%{name}-%{version}
cp COPYING %{buildroot}%_docdir/%{name}-%{version}/
cp COPYING.LGPL %{buildroot}%_docdir/%{name}-%{version}/

#cp ssp* %{buildroot}%{_libdir}
#rm %{buildroot}%{_libdir}/ssp*.lib
#rm %{buildroot}%{_libdir}/ssp*.dll

mv %{buildroot}%{_usr}/gcc444.cmd $RPM_BUILD_ROOT%_docdir/%{name}-%{version}/
mv %{buildroot}%{_usr}/readme.os2 $RPM_BUILD_ROOT%_docdir/%{name}-%{version}/
mv %{buildroot}%{_usr}/stdio.diff $RPM_BUILD_ROOT%_docdir/%{name}-%{version}/

ln -s /@unixroot/usr/libexec/gcc/i386-pc-os2-emx/4.4.4/cc1.exe %{buildroot}/@unixroot/usr/bin/cc1.exe
ln -s /@unixroot/usr/libexec/gcc/i386-pc-os2-emx/4.4.4/cc1plus.exe %{buildroot}/@unixroot/usr/bin/cc1plus.exe


%clean
rm -rf %{buildroot}

%post wrc
if [ "$1" = 1 ] ; then
#execute only on first install
%cube {DELLINE "SET EMXOMFLD_RC="} c:\config.sys > NUL
%cube {DELLINE "SET EMXOMFLD_RC_TYPE="} c:\config.sys > NUL
%cube {ADDLINE "SET EMXOMFLD_RC=wrc.exe"} c:\config.sys > NUL
%cube {ADDLINE "SET EMXOMFLD_RC_TYPE=WRC"} c:\config.sys > NUL
fi

%postun wrc
if [ "$1" = 0 ] ; then
#execute only on last uninstall
%cube {DELLINE "SET EMXOMFLD_RC="} c:\config.sys > NUL
%cube {DELLINE "SET EMXOMFLD_RC_TYPE="} c:\config.sys > NUL
fi

%post wlink
if [ "$1" = 1 ] ; then
#execute only on first install
%cube {DELLINE "SET EMXOMFLD_LINKER="} c:\config.sys > NUL
%cube {DELLINE "SET EMXOMFLD_TYPE="} c:\config.sys > NUL
%cube {ADDLINE "SET EMXOMFLD_LINKER=wl.exe"} c:\config.sys > NUL
%cube {ADDLINE "SET EMXOMFLD_TYPE=WLINK"} c:\config.sys > NUL
fi

%postun wlink
if [ "$1" = 0 ] ; then
#execute only on last uninstall
%cube {DELLINE "SET EMXOMFLD_LINKER="} c:\config.sys > NUL
%cube {DELLINE "SET EMXOMFLD_TYPE="} c:\config.sys > NUL
fi

%files
%defattr(-,root,root,-)
%{_usr}/bin
%{_usr}/include
%{_usr}/info
%{_libdir}/*.*a
%{_libdir}/*.spec
%{_libdir}/gcc/*
%{_usr}/libexec
%{_usr}/man
%{_usr}/share

%files stack-protector
%defattr(-,root,root,-)
%{_libdir}/ssp.dll

%files wlink
%doc gcc-wlink.txt

%files wrc
%doc gcc-wrc.txt

%files -n libgcc444
%defattr(-,root,root,-)
%{_libdir}/gcc444.dll
%doc %{_datadir}/doc/*

%changelog
