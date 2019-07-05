%define debug_package %{nil}

Summary:    Install Font
Name:       instfont
Version:    1.0.0
Release:    1%{?dist}
License:    proprietary
URL:        http://www.altsan.org/programming/os2/#instfont
Vendor:     Alex Tylor
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root

%description
The purpose of this utility is to install fonts into the WPS.

%prep
%setup -n "%{name}-%{version}" -Tc
unzip -qj %{_sourcedir}/%{name}-%{version}.zip

%build


%install
for f in *.exe ; do
  install -p -m 0755 -D $f  $RPM_BUILD_ROOT%{_bindir}/$f
done
wpi4rpm add %{vendor}/%{name}/binaries %{version}-%{release}

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
%doc instfont.txt instfont.c
%_bindir/*.exe

%changelog
* Tue Mar 21 2017 Alex Taylor <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- first public version
