%define debug_package %{nil}

Summary:    Firefox DLLs high
Name:       firefox-highmem
Version:    45.9.0
Release:    1%{?dist}
License:    proprietary
URL:        http://www.bitwiseworks.com
Vendor:     bww bitwiseworks GmbH.
Requires:   highmem >= 1.0.0

Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root

%description
The purpose of this utility is to load Firefox DLLs in the upper meomry arena.

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build
%install
for f in readme.txt ; do
  install -p -m0644 -D $f  $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}/$f
done

%clean
rm -rf "$RPM_BUILD_ROOT"

%post 
%global title %{summary}
%bww_folder -t %{title}
%bww_readme -f %{_defaultdocdir}/%{name}-%{version}/readme.txt
%highmem qb %{_libdir}/firefox-%{version}/*.dll

%postun 
%highmem qu %{_libdir}/firefox-%{version}/*.dll

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/readme.txt

%changelog
* Fri Jun 29 2018 herwig Bauernfeind <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- first public rpm version

