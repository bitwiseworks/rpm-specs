#define svn_url     F:/rd/ports/cron2/trunk
%scm_source svn http://svn.netlabs.org/repos/ports/cron2/trunk 2323

%define kmk_dist out/os2.x86/release/dist

Summary: daemon to execute scheduled commands
Name: cron2
Version: 1.4.2
Release: 1%{?dist}
License: This is a FreeWare product.
Group: Development/Libraries

Requires: libc >= 0.6.6

%description
CRON/2, client/server-based  timed program execution.

%debug_package

%prep
%scm_setup

%global kmk_flags CFLAGS="%{optflags}" LDFLAGS=-Zhigh-mem KBUILD_VERBOSE=2 BUILD_TYPE=release INST_PREFIX="%{_prefix}"

%build
kmk -C src %{kmk_flags}
kmk -C src install

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_sysconfdir}
mkdir -p %{buildroot}%{_localstatedir}/log

cp %{kmk_dist}/bin/at.exe %{buildroot}%{_bindir}/at.exe
cp %{kmk_dist}/bin/cron2.exe %{buildroot}%{_bindir}/cron2.exe
cp src/cron2.dat %{buildroot}%{_sysconfdir}/cron2.dat

# Ghost config files:
touch ${RPM_BUILD_ROOT}%{_localstatedir}/log/cron2.log

%clean
rm -rf %{buildroot}

%post
if [ "$1" -ge 1 ]; then # (upon update)
  %wps_object_delete_all
fi
%wps_object_create_begin
WP_TOOLS_CRON2_EXEC:WPProgram|Cron/2 Daemon|<WP_TOOLS>|EXENAME=((%_bindir/cron2.exe));STARTUPDIR=((%_bindir));ICONFILE=((%_defaultdocdir/%name-%version/cron2.ico));TITLE=Cron/2 Daemon;
WP_START_CRON2_EXEC:WPShadow|Cron/2 Daemon|<WP_START>|SHADOWID=<WP_TOOLS_CRON2_EXEC>

%wps_object_create_end

%postun
if [ "$1" = "0" ]; then
  %wps_object_delete_all
fi

%files
%defattr(-,root,root)
%doc src/cron2.doc
%doc src/cron2.ico
%{_bindir}/*.exe
%config(noreplace) %{_sysconfdir}/cron2.dat
%ghost %{_localstatedir}/log/cron2.log

%changelog
* Fri Jan 18 2019 yd <yd@os2power.com> 1.4.2-2
- fixed dat file parsing

* Tue Aug 25 2015 yd <yd@os2power.com> 1.4.2-1
- initial build with unixroot support for /@unixroot/etc/cron2.dat and default
  logging to /@unixroot/var/log/cron2.log.

