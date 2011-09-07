Summary: Watcom Compiler tools for gcc
Name: watcom
Version: 1.6
Release: 1
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
cp wrc.exe $RPM_BUILD_ROOT%{_bindir}
cp wl.exe $RPM_BUILD_ROOT%{_bindir}

%clean
rm -rf %{buildroot}

%files wlink-hll
%defattr(-,root,root)
%{_bindir}/wl.exe

%files wrc
%defattr(-,root,root)
%{_bindir}/wrc.exe
