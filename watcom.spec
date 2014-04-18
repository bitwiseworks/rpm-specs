Summary: Watcom Compiler tools for gcc
Name: watcom
Version: 1.9
Release: 5%{?dist}
License: none

Group: Development/Languages

Source: watcom.zip

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

%prep
%setup -q -c

%install
rm -rf %{buildroot}
mkdir -p $RPM_BUILD_ROOT/%{_bindir}
cp -p wrc.exe $RPM_BUILD_ROOT%{_bindir}
cp -p wl.exe $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf %{buildroot}

%files wlink-hll
%defattr(-,root,root)
%{_bindir}/wl.exe

%files wrc
%defattr(-,root,root)
%{_bindir}/wrc.exe
%doc wrc.lvl

%changelog
* Fri Apr 18 2014 yd
- wrc, corrects large (over 64KB) page table truncation
- wrc, uses per-process unique temporary file names

* Wed Oct 30 2013 yd
- upgraded wlink with highmem patch from R.Walsh (firefox build).

* Mon Nov 28 2011 yd
- upgraded wrc to release 1.9.
