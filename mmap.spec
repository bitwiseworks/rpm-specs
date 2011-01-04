Summary: A memory mapped emulation for OS/2-eComStation
Name: mmap
Version: 20110104
Release: 6%{?dist}
License: unknown
Group: Development/Libraries
Source: mmap-%{version}-os2.zip

Requires: libc >= 0.6.3

%description
A memory mapped files emulation library.

%prep
%setup -q -c


%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp bin/mmap.dll %{buildroot}%{_libdir}
cp lib/mmap_dll.a %{buildroot}%{_libdir}/mmap.a
cp lib/mmap_s.lib %{buildroot}%{_libdir}
cp lib/mmap_g.lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*
