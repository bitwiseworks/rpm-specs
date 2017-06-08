%define debug_package %{nil}
%define _strip_opts --no-compress --no-debuginfo

Summary:    bitwiseworks icons and folders
Name:       bww-resources
Version:    1.0.1
Release:    1%{?dist}
License:    Proprietory
Group:      Applications/System
URL:        http://www.bitwiseworks.com
Vendor:     bww bitwiseworks GmbH
Source1:    macros.bww
Source10:   bwwfbkg.bmp
Source11:   bwwfldrc.ico
Source12:   bwwfldro.ico
Source13:   mkdll.cmd
Source14:   mkres.obj
Source15:   mkres.def
Source16:   bwwres.rc
BuildRoot:  %_tmppath/%name-%version-%release-root
BuildArch:  noarch
Obsoletes:  bwwres <= 1.0.0-5

%description
This package provides bitwiseworks icons and folder background

%package devel
Summary:    bww macros and the like
Group:      Development/Libraries

%description devel
This package provides bitwiseworks macros

%prep
%setup -n "%{name}-%{version}" -Tc

# Prepare forwarder DLLs.
for m in %{SOURCE1} %{SOURCE10} %{SOURCE11} %{SOURCE12} %{SOURCE13} %{SOURCE14} %{SOURCE15} %{SOURCE16}; do
  cp ${m} .
done

%build
mkdll.cmd

%install
install -p -m0644 -D bwwres.dll  $RPM_BUILD_ROOT%{_libdir}/bwwres.dll
install -p -m0644 -D macros.bww  $RPM_BUILD_ROOT%{_rpmconfigdir}/macros.d/macros.bww
install -p -m0644 -D bwwfbkg.bmp $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfbkg.bmp 
install -p -m0644 -D bwwfldrc.ico $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfldrc.ico
install -p -m0644 -D bwwfldro.ico $RPM_BUILD_ROOT%{_datadir}/os2/bww/bwwfldro.ico

%clean
rm -rf "$RPM_BUILD_ROOT"

%post

%postun

%files
%defattr(-,root,root,-)
%_libdir/bwwres.dll
%_datadir/os2/bww/bwwfbkg.bmp
%_datadir/os2/bww/*.ico

%files devel
%_libdir/rpm/macros.d/macros.bww

%changelog
* Thu Jun 08 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0.1-1
- redesigned the macro completely
- moved the macro to -devel
- renamed the spec

* Sat Mar 18 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-5
- fix -a switch (diver)

* Tue Mar 14 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-4
- -a switch in order to allow file filters

* Mon Mar 06 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-3
- -t switch in order to allow custom object titles (diver)

* Mon Mar 06 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-2
- fix exe shadow
- heavily modified specfile (diver)

* Fri Mar 03 2017 hb <herwig.bauernfeind@bitwiseworks.com> 1.0.0-1
- first release of bitwiseworks icons, bitmaps and macros
