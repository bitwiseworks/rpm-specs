Summary: A memory mapped emulation for OS/2-eComStation
Name: mmap
Version: 20111102
Release: 8%{?dist}
License: unknown
Group: Development/Libraries
Source: mmap-%{version}-os2.zip

Requires: libc >= 0.6.3

%description
A memory mapped files emulation library.

%prep
%setup -q -c


%build
export KCFLAGS="%{optflags}"
kmk -C src
kmk -C src install
kmk -C src build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp mmap.dll %{buildroot}%{_libdir}
cp mmap_dll.a %{buildroot}%{_libdir}/mmap.a
cp mmap_s.lib %{buildroot}%{_libdir}
cp mmap_g.lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*

%changelog
* Wed Nov 02 2011 yd
- added -Zdll to build system
- improved build system
- included wpstk source code
