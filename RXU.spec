%define debug_package %{nil}

Summary:    Dave Boll's RXU REXX library
Name:       RXU
Version:    1.a.0
Release:    2%{?dist}
License:    Freeware
Group:      System/Libraries
URL:        http://www.edm2.com/index.php/OS2_API:RXU
Vendor:     Dave Boll
Source:     %{name}-%{version}.zip
BuildRoot:  %_tmppath/%name-%version-%release-root
Requires:   os2-rpm >= 1-2

%description
RXU v1.a - Rich set of Rexx functions which expose most of the OS/2 API set to
Rexx programs (memory management/access, semaphores, pipes, queues, module handling,
threading/tasking, system information, i/o, devioctl, etc.), as well as providing
many functions which aid in Rexx programming (variable pool access, "expose" variables
across external function calls, queue manipulation, macrospace management, etc.).
Package includes .INF file and sample Rexx programs.  Freeware.  Uploaded by author.


%prep
%setup -n "%{name}-%{version}" -Tc
unzip -q %{_sourcedir}/%{name}-%{version}.zip

%build


%install
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cp usr/bin/*.exe $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_libdir}
cp usr/lib/*.dll $RPM_BUILD_ROOT%{_libdir}
mkdir -p $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
cp usr/share/doc/rxu/* $RPM_BUILD_ROOT%{_defaultdocdir}/%{name}-%{version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/os2/book
cp usr/share/os2/book/*.inf $RPM_BUILD_ROOT%{_datadir}/os2/book


%clean
rm -rf "$RPM_BUILD_ROOT"

%post
if [ "$1" -ge 1 ]; then # (upon update)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/Library wpi4rpm del %{vendor}/%{name}/Library %{version}-%{release}
fi
%wps_object_create_begin
WP_BWWHELP:WPFolder|bww Help|<WP_ASSISTANCE>|TITLE=bitwiseworks Help Center;SHOWALLINTREEVIEW=YES;ICONRESOURCE=60,PMWP.DLL;
%wps_object_create_end
%{_rpmconfigdir_os2}/wpi4rpm add %{vendor}/%{name}/Library %{version}-%{release}

%postun
if [ "$1" -eq 0 ]; then # (upon removal)
    %wps_object_delete_all
    %{_rpmconfigdir_os2}/wpi4rpm del %{vendor}/%{name}/Library %{version}-%{release}
fi

%files
%defattr(-,root,root,-)
%_defaultdocdir/%{name}-%{version}/*
%_bindir/*.exe
%_libdir/*.dll
%_datadir/os2/book/*.inf


%changelog
* Thu Jun 07 2018 hb <herwig.bauernfeind@bitwiseworks.com> 1.a.0-2
- Fix location of wpi4rpm and objects

* Sun Feb 05 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.a.0-1
- final release by Dave Boll
