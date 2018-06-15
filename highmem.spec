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
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp *.exe $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp readme.txt $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}

%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
fi

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/readme.txt
%_bindir/*.exe

%changelog
* Fri Jun 15 2018 Yuri Dario <yd@os2power.com> 1.0.0-1
- first public rpm version
