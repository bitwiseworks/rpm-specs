%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo

Summary:    Dave Boll's RXU REXX library
Name:       rxu
Version:    1.a.0
Release:    3%{?dist}
License:    Freeware
Group:      System/Libraries
URL:        http://www.edm2.com/index.php/OS2_API:RXU
Vendor:     Dave Boll
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   os2-rpm >= 1-2
Obsoletes:  RXU

%description
RXU v1.a - Rich set of Rexx functions which expose most of the OS/2 API set to
Rexx programs (memory management/access, semaphores, pipes, queues, module handling,
threading/tasking, system information, i/o, devioctl, etc.), as well as providing
many functions which aid in Rexx programming (variable pool access, "expose" variables
across external function calls, queue manipulation, macrospace management, etc.).
Package includes .INF file and sample Rexx programs.  Freeware.  Uploaded by author.


%prep
%setup -n "%{name}-%{version}" -Tc
unzip -qj %{_sourcedir}/%{name}-%{version}.zip

%build


%install
install -p -m0755 -D rxsrs.exe $RPM_BUILD_ROOT%{_bindir}/rxsrs.exe
install -p -m0644 -D rxu.dll $RPM_BUILD_ROOT%{_libdir}/rxu.dll
install -p -m0644 -D rxu.inf $RPM_BUILD_ROOT%{_datadir}/os2/book/rxu.inf


%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/Library %{version}-%{release}
fi
%{_rpmconfigdir_os2}/wpi4rpm add %{vendor}/%{name}/Library %{version}-%{release}

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/Library %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%doc rxu.dsc rxusmp.zip
%_bindir/*.exe
%_libdir/*.dll
%_datadir/os2/book/*.inf


%changelog
* Fri Sep 07 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.a.0-3
- Fix spec file (Silvan Scherrer)

* Thu Jun 07 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.a.0-2
- Fix location of wpi4rpm and objects

* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.a.0-1
- final release by Dave Boll
