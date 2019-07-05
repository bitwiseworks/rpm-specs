Summary: OS/2 specific RPM macros and scripts
Name: os2-rpm
Version: 1
Release: 7%{?dist}
License: GPLv2+
Group: Development/System
Vendor: bww bitwise works GmbH

BuildArch: noarch

Requires: rpm >= 4.13.0-16
Requires: cube

Provides: system-rpm-config = %{version}-%{release}
# as we integrated the wpi4rpm rpm here, obsolete the old package 
Obsoletes: wpi4rpm <= 0.9.7
Provides:  wpi4rpm 

BuildRequires: rexx_exe

Source0: macros.os2
Source1: brp-strip-os2
Source2: find-legacy-runtime.sh
Source3: macros.scm
Source4: macros.cfg
Source5: macros.wps
Source6: wps-object.cmd
Source7: warpin-conflicts.cmd
Source8: getbootdrive.cmd
Source9: wpi4rpm.cmd
Source10: macros.scm_pwd

# This is necessary due to a silly "Provides: os2-rpm" in os2-rpm-build-0-1
Conflicts: os2-rpm-build <= 0-1

%description
OS/2 specific RPM macros and scripts neecessary to install RPM packages on
the OS/2 operating system.

%package build
Summary: OS/2 specific RPM macros and scripts to build RPM packages
Requires: %{name} = %{version}-%{release}
Requires: rpm-build >= 4.13.0-15

%description build
OS/2 specific RPM macros and scripts neecessary to build RPM packages for
the OS/2 operating system.

%global _rpmconfigdir_os2 %{_rpmconfigdir}/%{_vendor}
%global _rpmconfigdir_macros_d %{_rpmconfigdir}/macros.d

%prep
# Move all sources to build subdir to reference them by name instead of SOURCEx
%setup -c -T
%{__cp} -a %{sources} .

# Note: we put the value of _rpmconfigdir_os2 unexpanded.
%{__sed} -e 's|@RPMCONFIGDIR_OS2@|%%{_rpmconfigdir}/%%{_vendor}|' -i macros.os2

%build
# create a exe out of the cmd files
for f in *.cmd ; do
  rexx2vio "$f" "${f%.cmd}.exe"
done

%install
%{__mkdir_p} %{buildroot}%{_rpmconfigdir_os2}
%{__install} -p -m 644 macros.os2 %{buildroot}%{_rpmconfigdir_os2}/macros
%{__install} -p -m 644 -t %{buildroot}%{_rpmconfigdir_os2} brp-strip-os2 find-legacy-runtime.sh

%{__mkdir_p} %{buildroot}%{_rpmconfigdir_macros_d}
%{__install} -p -m 644 -t %{buildroot}%{_rpmconfigdir_macros_d} \
  macros.scm macros.cfg macros.wps
%{__mkdir_p} %{buildroot}%{_sysconfdir}/rpm
%{__install} -p -m 644 -t %{buildroot}%{_sysconfdir}/rpm macros.scm_pwd

# install OS/2 Rexx scripts
for f in *.exe ; do
  %{__install} -p -m 755 $f %{buildroot}%{_rpmconfigdir_os2}/$f
  ln -sf %{_rpmconfigdir_os2}/$f %{buildroot}%{_libdir}/rpm/${f%.exe}
done
%{__install} -D -p -m 755 wpi4rpm.exe %{buildroot}%{_bindir}/wpi4rpm.exe
%{__install} -D -p -m 755 warpin-conflicts.exe %{buildroot}%{_libdir}/rpm/warpin-conflicts.exe

%files
%dir %{_rpmconfigdir_os2}
%{_rpmconfigdir_os2}/macros
%{_rpmconfigdir_os2}/*.exe
%{_libdir}/rpm/wpi4rpm
%{_libdir}/rpm/warpin-conflicts*
%{_libdir}/rpm/wps-object
%{_libdir}/rpm/getbootdrive
%{_bindir}/wpi4rpm.exe
%{_rpmconfigdir_macros_d}/macros.cfg
%{_rpmconfigdir_macros_d}/macros.wps

%files build
%{_rpmconfigdir_os2}/brp-strip-os2
%{_rpmconfigdir_os2}/find-legacy-runtime.sh
%{_rpmconfigdir_macros_d}/macros.scm
%config(noreplace) %{_sysconfdir}/rpm/macros.scm_pwd

%changelog
* Mon May 27 2019 Herwig Bauernfeind <herwig.bauernfeind@bitwiseworks.com> 1-7
- chg warpin-conflicts to look for rpmdummy entries as well

* Mon Jan 21 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 1-6
- fix scm_macro to work with noarch only spec as well

* Tue Nov 27 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1-5
- some rather old packages still need warpin-conflicts at the old location,
  so copy it there as well ticket #321

* Sun Nov 11 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1-4
- add the possibility to have password protected github projects

* Mon Aug 20 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> 1-3
- copy wpi4rpm also to %{_bindir} ticket #308
- don't add an extention to symlinks

* Mon Apr 23 2018 Dmitriy Kuminov <coding@dmik.org> 1-2
- Fix os2_fwdslashes and os2_backslashes that would return garbage at the end.
- Remove useless os2_dos_path_f and add os2_expand_unixroot instead.

* Tue Feb 20 2018 Herwig Bauernfeind <herwig.bauernfeind@bitwiseworks.com> 1-1
- Unify format of error messages from wps-object, warpin-conflicts and wpi4rpm
- Integrate wpi4rpm into os2-rpm (as we don't want to add a 
  Provides wpi4rpm=version, we changed the spec version to 1)

* Wed Oct 4 2017 Dmitriy Kuminov <coding@dmik.org> 0-5
- Work around kLIBC bug #379 when unzipping archives with long file names
  in scm_setup.

* Fri Jul 28 2017 Dmitriy Kuminov <coding@dmik.org> 0-4
- Add os2_langdir, os2_bookdir and os2_helpdir macros.
- Make os2_dos_path understand ';' as path separator.
- Make os2_dos_path replace /@unixroot with %UNIXROOT% rather its current value
  (build-time values may differ from install-time values so should not be used).
- Add os2_fwdslashes and os2_backslashes for easy slash conversion in paths.
- Add os2_expand_dos_vars to expand env.vars (should only be used with -e
  option in scriplets to cause install-time expansion, as well as os2_boot_drive
  and os2_unixroot_path).

* Mon Jul 10 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 0-3
- add a symlink to the *.exe, so old rpm still work

* Fri Jun 9 2017 Dmitriy Kuminov <coding@dmik.org> 0-2
- Change mistyped "Provides: os2-rpm" to "Requires" in os2-rpm-base.
- Move scm_source/scm_setup macros from rpm to os2-rpm-build sub-package.
- Better support for local git repos via file://.
- Move WPS/WarpIn macros from rpm to os2-rpm-build sub-package.
- Move config.sys macros from rpm to os2-rpm package.
- Move os2_boot_drive from rpm to os2-rpm package.
- Add os2_dos_path macro to convert from Unix paths to DOS paths.
- Add os2_unixroot_path macro (replaces former os2_unixroot_drive in rpm).
- Install main OS/2 macros file from os2-rpm as RPM installation scriptlets
  need some definitions from it.

* Thu Apr 6 2017 Dmitriy Kuminov <coding@dmik.org> 0-1
- Initial release.

