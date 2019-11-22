%global os2_wipfcdir %{_datadir}/os2/wipfc

Summary: Watcom Compiler tools for gcc
Name: watcom
Version: 2.0beta3
Release: 5%{?dist}
License: none

Group: Development/Languages

Source: watcom.zip

# For os2_dos_path, os2_langdir etc. macros
Requires: os2-rpm >= 0-4

%description
Watcom tools.

%package wlink-hll
Summary: Watcom Compiler linker for gcc.

%description wlink-hll
Watcom Compiler linker for gcc.

%package wrc
Summary: Watcom Compiler resource compiler.

%description wrc
Watcom Compiler resource compiler.

%package wipfc
Summary: Watcom Compiler IPFC tool

%description wipfc
Provides Watcom Compiler Information Presentation Facility tool
including the IPF complier and support files.

%package debug
Summary: Watcom Compiler debug package

%description debug
Watcom Compiler debug package contains the SYM files.


%prep
%setup -q -c


%install
rm -rf %{buildroot}

# install exe files
for f in *.exe ; do
  install -p -m0755 -D $f %{buildroot}%{_bindir}/$f
done

# install sym files
for f in *.sym ; do
  install -p -m0644 -D $f %{buildroot}%{_bindir}/$f
done

# ipfc
cd wipfc
for f in * ; do
  install -p -m0644 -D $f %{buildroot}%{os2_wipfcdir}/$f
done
cd ..

%clean
rm -rf %{buildroot}


%post wipfc -e
%cube {ADDSTRING "%{os2_dos_path %{_datadir}/os2/wipfc}" IN "SET WIPFC=" (FIRST IFNEW BEFORE ADDBOTTOM RS(%%)} %%{os2_config_sys} > NUL

%postun wipfc -e
if [ "$1" = 0 ] ; then
# execute only on last uninstall
%cube {DELSTRING "%{os2_dos_path %{_datadir}/os2/wipfc}" IN "SET WIPFC=" (FIRST RS(%%)} %%{os2_config_sys} > NUL
fi


%files wlink-hll
%defattr(-,root,root)
%{_bindir}/wl.exe
%doc wl.lvl

%files wrc
%defattr(-,root,root)
%{_bindir}/wrc.exe
%doc wrc.lvl

%files wipfc
%defattr(-,root,root)
%{_bindir}/wipfc.exe
%doc wipfc.lvl
%{os2_wipfcdir}/*

%files debug
%{_bindir}/*.sym


%changelog
* Fri Nov 22 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.0beta3-5
- use -e and %% in scriplets, so it gets expanded right

* Mon Jun 18 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.0beta3-4
- use %{os2_config_sys} macro instead of fixed c:\config.sys

* Mon Mar 19 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.0beta3-3
- wipfc doesn't like the trailing ; in set wpifc

* Wed Mar 14 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.0beta3-2
- change/add the wipfc config files

* Wed Mar 07 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 2.0beta3-1
- add the executable flag to the exe
- add a debug package for sym files
- added wipfc subpackage

* Fri Jun 20 2014 yd
- wlink build 20140527, uses highmem allocations.

* Fri Apr 18 2014 yd
- wrc, corrects large (over 64KB) page table truncation
- wrc, uses per-process unique temporary file names

* Wed Oct 30 2013 yd
- upgraded wlink with highmem patch from R.Walsh (firefox build).

* Mon Nov 28 2011 yd
- upgraded wrc to release 1.9.
