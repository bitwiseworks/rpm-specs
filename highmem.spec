%define debug_package %{nil}

Summary:    HighMem, a LX format 32bit DLL module 'loading above 512MB' marking utility,
Name:       highmem
Version:    1.0.0
Release:    1%{?dist}
License:    proprietary
URL:        http://www.bitwiseworks.com
Vendor:     Yuri Dario

Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root

%description
The purpose of this utility is to mark DLLs as high loadable.
Partially based on ABOVE512 (C) 2004 Takayuki 'January June' Suwa.

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build

%install
rm -rf %{buildroot}
for f in *.exe ; do
  install -p -m 0755 -D $f  $RPM_BUILD_ROOT%{_bindir}/$f
done

%clean
rm -rf "$RPM_BUILD_ROOT"

%files
%defattr(-,root,root,-)
%doc readme.txt
%_bindir/*.exe

%changelog
* Fri Jun 15 2018 herwig Bauernfeind <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- first public rpm version
