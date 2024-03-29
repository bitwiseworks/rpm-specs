%define ver_major   4
%define ver_minor   9
%define ver_patch   2

%define os2_release 1

%define rpm_release 3

%global gcc_version %{ver_major}.%{ver_minor}.%{ver_patch}
%global gcc_target_platform %{_target_cpu}

# New package version scheme: X.Y.Z.N-R, where X.Y.Z is the GCC release (e.g.
# 4.5.4, matches gcc_version above), N is the OS/2 release (1, 2, etc) and R is
# the RPM release (1, 2, etc). The OS/2 release number increases with each
# OS/2 specific update to the sources followed by a new build, the RPM repease
# number increases with each new RPM build (which may use the same source tree
# but fix only some RPM-specific things). Note that the RPM release number
# resets to 1 each time the OS/2 release increases (which is reset to 1 in turn
# when the GCC release changes.

Summary: Various compilers (C, C++, Objective-C, Java, ...)
Name: gcc
Version: %{gcc_version}.%{os2_release}
Release: %{rpm_release}%{?dist}

# libgcc, libgfortran, libmudflap, libgomp, libstdc++ and crtstuff have
# GCC Runtime Exception.
License: GPLv3+ and GPLv3+ with exceptions and GPLv2+ with exceptions
Group: Development/Languages
URL: http://gcc.gnu.org

Source0: gcc-gcc-4_9-branch-os2.tar.bz2
Source1: gcc-libgcc-fwd.zip

Obsoletes: gcc < %{gcc_version}

BuildRequires: binutils make
BuildRequires: os2-base-fhs
BuildRequires: ash gcc gcc-wlink gcc-wrc grep gettext-devel diffutils gawk flex sed
BuildRequires: gmp-devel >= 4.1.2-8, mpfr-devel >= 2.2.1, mpc-devel
BuildRequires: libc-devel >= 0.6.6-25
BuildRequires: rpm >= 4.8.1-22

Requires: libgcc1 = %{version}-%{release}
Requires: libssp = %{version}-%{release}
Requires: libstdc++6 = %{version}-%{release}
Requires: libsupc++6 = %{version}-%{release}
# libc header fixes
Requires: libc-devel >= 0.6.6-25
# rpm color workaround
Requires: rpm >= 4.8.1-22
Requires: binutils

%description
The gcc package contains the GNU Compiler Collection version %{ver_major}.%{ver_minor}.
You'll need this package in order to compile C code.

%package -n libgcc-fwd
Summary: GCC version shared support forwarder library
Group: System Environment/Libraries
Autoreq: false
Obsoletes: libgcc335 libgcc432 libgcc433 libgcc434 libgcc440 libgcc441
Obsoletes: libgcc442 libgcc444 libgcc445 libgcc446 libgcc452 libgcc453
Obsoletes: libgcc473 libgcc490 libgcc492

%description -n libgcc-fwd
This package contains GCC shared support forwarder library which is needed
e.g. for exception handling support.

%package -n libgcc1
Summary: GCC version 1 shared support library
Group: System Environment/Libraries
Autoreq: false

%description -n libgcc1
This package contains GCC shared support library which is needed
e.g. for exception handling support.

%package -n libssp
Summary: GCC stack protector shared library
Group: System Environment/Libraries
Obsoletes: gcc-stack-protector

%description -n libssp
This package contains GCC shared library which is needed
for stack protector.

%package -n libstdc++6
Summary: GNU Standard C++ Library v3
Group: System Environment/Libraries

%description -n libstdc++6
This package contains GNU Standard C++ Library v3 shared library.

%package -n libsupc++6
Summary: GNU Standard C++ Library v3 subset
Group: System Environment/Libraries

%description -n libsupc++6
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

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.


%prep
%setup -q -c -a 1


%build
rm -fr obj-%{gcc_target_platform}
mkdir obj-%{gcc_target_platform}
cd obj-%{gcc_target_platform}

script_dir=%{_topdir}/BUILD/%{name}-%{version}/obj-%{gcc_target_platform}
export PATH="$script_dir/gcc${PATH:+;$PATH}"
export BEGINLIBPATH="$script_dir/gcc${BEGINLIBPATH:+;$BEGINLIBPATH}"
export LIBPATHSTRICT=T

export CFLAGS="$RPM_OPT_FLAGS -DEMX -DOS2"
export CXXFLAGS="$RPM_OPT_FLAGS -DEMX -DOS2"
export LDFLAGS="-g -Zexe -Zomf -Zmap -Zargs-wild -Zhigh-mem"
export LANG=en_US
export GREP=grep

export PATH_SEPARATOR=;
export CONFIG_SITE=/@unixroot/usr/share/config.legacy

../configure --prefix=%{_prefix} \
    --with-sysroot=/@unixroot \
    --enable-shared \
    --enable-languages=c,c++ \
    --enable-frame-pointer \
    --with-gnu-as \
    --disable-bootstrap \
    --disable-multilib \
    --disable-libstdcxx-pch \
    --enable-threads 

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
cd obj-%{gcc_target_platform}

# There are some MP bugs in libstdc++ Makefiles
#make -C %{gcc_target_platform}/libstdc++-v3

#make prefix=%{buildroot}%{_prefix} mandir=%{buildroot}%{_mandir} \
#  infodir=%{buildroot}%{_infodir} install

make DESTDIR=${RPM_BUILD_ROOT} install

# copy runtime files
emxomf -o i386-pc-os2-emx/libgcc/libgcc_so_d.lib i386-pc-os2-emx/libgcc/libgcc_so_d.a
#cp -p i386-pc-os2-emx/libgcc/libgcc_so_d.a %{buildroot}%{_libdir}
#cp -p i386-pc-os2-emx/libgcc/libgcc_so_d.lib %{buildroot}%{_libdir}
#cp -p i386-pc-os2-emx/libgcc/gcc%{ver_major}%{ver_minor}%{ver_patch}.dll %{buildroot}%{_libdir}

#build dll
dllar -o stdcpp6.dll i386-pc-os2-emx/libstdc++-v3/src/.libs/libstdc++.a \
	-d "GNU stdc++ %{version}-%{release}" \
	-nolxlite -flags "-Zmap -Zhigh-mem -Zomf -g -L%{buildroot}%{_libdir}" \
	-ex "___main ___do_global_* ___ctordtor* ___eh* ___pop* _DLL_InitTerm" \
	-libf "INITINSTANCE TERMINSTANCE" \
	-libd "DATA MULTIPLE"
cp -p stdcpp6.dll %{buildroot}%{_libdir}
cp -p stdcpp6.a %{buildroot}%{_libdir}/stdc++.a
cp -p stdcpp6.lib %{buildroot}%{_libdir}/stdc++.lib
mv %{buildroot}%{_libdir}/libstdc++.a %{buildroot}%{_libdir}/stdc++_s.a

#build dll
dllar -o supcpp6.dll i386-pc-os2-emx/libstdc++-v3/libsupc++/.libs/libsupc++.a \
	-d "GNU supc++ %{version}-%{release}" \
	-nolxlite -flags "-Zmap -Zhigh-mem -Zomf -g -L%{buildroot}%{_libdir}" \
	-ex "___main ___do_global_* ___ctordtor* ___eh* ___pop* _DLL_InitTerm" \
	-libf "INITINSTANCE TERMINSTANCE" \
	-libd "DATA MULTIPLE"
cp -p supcpp6.dll %{buildroot}%{_libdir}
cp -p supcpp6.a %{buildroot}%{_libdir}/supc++.a
cp -p supcpp6.lib %{buildroot}%{_libdir}/supc++.lib
mv %{buildroot}%{_libdir}/libsupc++.a %{buildroot}%{_libdir}/supc++_s.a

#build dll
dllar -o ssp.dll i386-pc-os2-emx/libssp/.libs/ssp.a \
	-d "GNU Stack Protector %{version}-%{release}" \
	-nolxlite -flags "-Zmap -Zhigh-mem -Zomf -g -L%{buildroot}%{_libdir}" \
	-ex "___main ___do_global_* ___ctordtor* ___eh* ___pop* _DLL_InitTerm" \
	-libf "INITINSTANCE TERMINSTANCE" \
	-libd "DATA MULTIPLE"
cp -p ssp.dll %{buildroot}%{_libdir}
cp -p ssp.a %{buildroot}%{_libdir}
cp -p ssp.lib %{buildroot}%{_libdir}
mv %{buildroot}%{_libdir}/ssp.a %{buildroot}%{_libdir}/ssp_s.a

cd ..

#build gccXXX forwarders
for bld in 335 432 433 434 435 440 441 442 444 445 446 452 453 454 464 473 474 482 483 490 491 492; do
  sed -i 's/Forwarder/Forwarder %{version}-%{release}/' gcc${bld}.def
  gcc -Zomf -Zmap -Zdll -nostdlib -o gcc${bld}.dll gcc${bld}.def fwdstub.s obj-%{gcc_target_platform}/gcc/libgcc_so_d.a -llibc
  cp -p gcc${bld}.dll %{buildroot}%{_libdir}
done

echo dummy for virtual package > gcc-wrc.txt
echo dummy for virtual package > gcc-wlink.txt

#mkdir -p %{buildroot}%{_usr}

rm %{buildroot}%{_libdir}/*.la
rm %{buildroot}%{_libdir}/*.py

ln -s ./cc1.exe %{buildroot}%{_libexecdir}/gcc/i386-pc-os2-emx/%{gcc_version}/cc1
ln -s ./cc1plus.exe %{buildroot}%{_libexecdir}/gcc/i386-pc-os2-emx/%{gcc_version}/cc1plus

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
%exclude %{_bindir}/*.dbg
%{_usr}/include
%{_libdir}/*.*a
%{_libdir}/*.lib
%exclude %{_libdir}/*.dll
%exclude %{_libdir}/*.dbg
%{_libdir}/gcc/*
%{_libexecdir}
%exclude %{_libexecdir}/gcc/i386-pc-os2-emx/%{gcc_version}/*.dbg
%exclude %{_libexecdir}/gcc/i386-pc-os2-emx/%{gcc_version}/install-tools/*.dbg
%{_datadir}/gcc-%{gcc_version}
%{_datadir}/locale
%{_datadir}/info
%{_datadir}/man
%doc ChangeLog ChangeLog.*
%doc README README.*
%doc COPYING COPYING.*
%doc MAINTAINERS

%files -n libssp
%defattr(-,root,root,-)
%{_libdir}/ssp.dll

%files -n libstdc++6
%defattr(-,root,root,-)
%{_libdir}/stdcp*.dll

%files -n libsupc++6
%defattr(-,root,root,-)
%{_libdir}/supcp*.dll

%files wlink
%doc gcc-wlink.txt

%files wrc
%doc gcc-wrc.txt

%files -n libgcc-fwd
%defattr(-,root,root,-)
%{_libdir}/gcc???.dll

%files -n libgcc1
%defattr(-,root,root,-)
%{_libdir}/gcc1.dll

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{_libdir}/*.dbg
%{_libexecdir}/gcc/i386-pc-os2-emx/%{gcc_version}/*.dbg
%{_libexecdir}/gcc/i386-pc-os2-emx/%{gcc_version}/install-tools/*.dbg

%changelog
* Tue Jan 30 2015 yd <yd@os2power.com> 4.9.2.1-3
- updated source code to gcc 4.9.2.
- create gccXXX forwarders to gcc1 runtime dll, use libc06 exports for
  non-standard symbols.
- use --enable-frame-pointer to disable unwinding table generation.
- build requires patched builtin.h and stddef.h (libc-0.6.6-25).
- use standard toolchain to build gcc runtime dll, use named exports only.

* Wed Nov 27 2013 yd
- Rename the following packages to avoid ABI breaks (using gcc versioning policy):
  + libstdc++ => libstdc++6
  + libsupc++ => libsupc++6
- updated source code to gcc 4.7.3.

* Mon Jul 25 2013 Dmitriy Kuminov <coding@dmik.org> - 4.4.6.17-1
- New OS/2 Release 17 of 4.4.6. See ChangeLog.OS2 for more information.

* Mon Jul 23 2013 Dmitriy Kuminov <coding@dmik.org> - 4.4.6.16-1
- New OS/2 Release 16 of 4.4.6. See ChangeLog.OS2 for more information.
- Rename the following packages to better match the conventions:
  + gcc-stack-protector => libssp
  + gcc-stdc++-shared-library => libstdc++
  + gcc-supc++-shared-library => libsupc++

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
