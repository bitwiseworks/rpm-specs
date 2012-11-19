%global gcc_version 4.4.6
%global gcc_target_platform %{_target_cpu}

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}
Release: 15%{?dist}

# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
URL: http://gcc.gnu.org

Source0: gcc-os2-20111223.tar.bz2
Patch0: gcc-os2.diff

BuildRoot: %{_tmppath}/%{name}-%{version}-root-%(%{__id_u} -n)

Obsoletes: gcc < %{gcc_version}

BuildRequires: binutils
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1

Requires: libgcc446 = %{gcc_version}
Requires: libc-devel >= 0.6.3
Requires: binutils

%description
The gcc package contains the GNU Compiler Collection version 4.4.
You'll need this package in order to compile C code.

%package -n libgcc446
Summary: GCC version 4.4 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc446
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libssp
Summary: GCC stack protector shared library
Group: System Environment/Libraries

%description -n libssp
This package contains GCC shared library which is needed
for stack protector.

%package -n libstdc++
Summary: GNU Standard C++ Library v3
Group: System Environment/Libraries

%description -n libstdc++
This package contains GNU Standard C++ Library v3 shared library.

%package -n libsupc++
Summary: GNU Standard C++ Library v3 subset
Group: System Environment/Libraries

%description -n libsupc++
This package contains GNU Standard C++ Library v3 subset shared library.

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
%setup -q -c
%patch0 -p1 -b .os2~

%build
rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

script_dir=%{_topdir}/BUILD/%{name}-%{version}/obj-%{gcc_target_platform}
export PATH="$script_dir/gcc${PATH:+;$PATH}"
export BEGINLIBPATH="$script_dir/gcc${BEGINLIBPATH:+;$BEGINLIBPATH}"

export CONFIG_SHELL=/@unixroot/usr/bin/sh.exe;
export AWK=awk;
export CFLAGS="$RPM_OPT_FLAGS -DEMX -DOS2"
export CXXFLAGS="$RPM_OPT_FLAGS -DEMX -DOS2"
export LDFLAGS="-g -Zexe -Zomf -Zmap -Zargs-wild -Zhigh-mem"
export LANG="";
../configure --prefix=%{_prefix} \
    --with-sysroot=/@unixroot \
    --enable-shared \
    --enable-languages=c,c++ \
    --with-gnu-as \
    --disable-bootstrap \
    --disable-multilib \
    --disable-libstdcxx-pch \
    --enable-threads \
   "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

cd obj-%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
#make -C %{gcc_target_platform}/libstdc++-v3

#make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
#  infodir=%{buildroot}%{_infodir} install

make DESTDIR=${RPM_BUILD_ROOT} install

#build dll
dllar -o stdcpp.dll i386-pc-os2-emx/libstdc++-v3/src/.libs/stdc++.a \
	-d "GNU stdc++ %{gcc_version}" \
	-nolxlite -flags "-Zmap -Zhigh-mem -Zomf -g" \
	-ex "___main ___do_global_* ___ctordtor* ___eh* ___pop* _DLL_InitTerm" \
	-libf "INITINSTANCE TERMINSTANCE" \
	-libd "DATA MULTIPLE"
cp -p stdcpp.dll %{buildroot}%{_libdir}
cp -p stdcpp.a %{buildroot}%{_libdir}/stdc++.a
cp -p stdcpp.lib %{buildroot}%{_libdir}/stdc++.lib
mv %{buildroot}%{_libdir}/stdc++.a %{buildroot}%{_libdir}/stdc++_s.a

#build dll
dllar -o supcpp.dll i386-pc-os2-emx/libstdc++-v3/libsupc++/.libs/supc++.a \
	-d "GNU supc++ %{gcc_version}" \
	-nolxlite -flags "-Zmap -Zhigh-mem -Zomf -g" \
	-ex "___main ___do_global_* ___ctordtor* ___eh* ___pop* _DLL_InitTerm" \
	-libf "INITINSTANCE TERMINSTANCE" \
	-libd "DATA MULTIPLE"
cp -p supcpp.dll %{buildroot}%{_libdir}
cp -p supcpp.a %{buildroot}%{_libdir}/supc++.a
cp -p supcpp.lib %{buildroot}%{_libdir}/supc++.lib
mv %{buildroot}%{_libdir}/supc++.a %{buildroot}%{_libdir}/supc++_s.a

#build dll
dllar -o ssp.dll i386-pc-os2-emx/libssp/.libs/ssp.a \
	-d "GNU Stack Protector %{gcc_version}" \
	-nolxlite -flags "-Zmap -Zhigh-mem -Zomf -g" \
	-ex "___main ___do_global_* ___ctordtor* ___eh* ___pop* _DLL_InitTerm" \
	-libf "INITINSTANCE TERMINSTANCE" \
	-libd "DATA MULTIPLE"
cp -p ssp.dll %{buildroot}%{_libdir}
cp -p ssp.a %{buildroot}%{_libdir}
cp -p ssp.lib %{buildroot}%{_libdir}
mv %{buildroot}%{_libdir}/ssp.a %{buildroot}%{_libdir}/ssp_s.a

cd ..

echo dummy for virtual package > gcc-wrc.txt
echo dummy for virtual package > gcc-wlink.txt

#mkdir -p %{buildroot}%{_usr}

rm %{buildroot}%{_libdir}/*.la

#mv %{buildroot}%{_usr}/readme.os2 $RPM_BUILD_ROOT%_docdir/%{name}-%{version}/

ln -s ./cc1.exe %{buildroot}%{_libexecdir}/gcc/i386-pc-os2-emx/%{version}/cc1
ln -s ./cc1plus.exe %{buildroot}%{_libexecdir}/gcc/i386-pc-os2-emx/%{version}/cc1plus

#yd fix attributes for executables
chmod 0755 %{buildroot}%{_bindir}/*.exe

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
%{_libdir}/*.lib
%{_libdir}/*.dll
%exclude %{_libdir}/*.dll
%{_libdir}/*.spec
%{_libdir}/gcc/*
%{_usr}/libexec
%{_usr}/man
%{_usr}/share

%files -n libssp
%defattr(-,root,root,-)
%{_libdir}/ssp.dll

%files -n libstdc++
%defattr(-,root,root,-)
%{_libdir}/stdcpp.dll

%files -n libsupc++
%defattr(-,root,root,-)
%{_libdir}/supcpp.dll

%files wlink
%doc gcc-wlink.txt

%files wrc
%doc gcc-wrc.txt

%files -n libgcc446
%defattr(-,root,root,-)
%{_libdir}/gcc446.dll
#%doc %{_datadir}/doc/*

%changelog
* Wed Jan 11 2012 yd
- use more conventionional names for shared libraries packages.

* Mon Jan 09 2012 yd
- install also dlls with main package.

* Sun Jan 08 2012 yd
- moved dlls out from main package.

* Fri Dec 23 2011 yd
- fixed spawn internal error report.
- fixed handling of big command lines (fixes OOo building).
- fixed Optlink calls.

* Fri Dec 9 2011 yd
- updated source code to 4.4.6, github tree
