#define svn_url     F:/rd/ports/cron2/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/cron2/trunk
%define svn_rev     1163

%define kmk_dist out/os2.x86/release/dist

Summary: unlink rename pending operation
Name: cron2
Version: 1.4.2
Release: 0.0%{?dist}
License: This is a FreeWare product.
Group: Development/Libraries

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Requires: libc >= 0.6.6

%description
CRON/2, client/server-based  timed program execution.

%package debug
Summary: HLL debug data for exception handling support.
Requires: %{name} = %{version}-%{release}

%description debug
HLL debug data for exception handling support.

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

%build
export KCFLAGS="%{optflags}"
kmk -C src
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
%wps_object_create_begin
WP_TOOLS_CRON2_EXEC:WPProgram|Cron/2 Daemon|<WP_TOOLS>|EXENAME=((%_bindir/cron2.exe));STARTUPDIR=((%_bindir));ICONFILE=((%_defaultdocdir/%name-%version/cron2.ico));TITLE=Cron/2 Daemon;
WP_START_CRON2_EXEC:WPShadow|Cron/2 Daemon|<WP_START>|SHADOWID=<WP_TOOLS_CRON2_EXEC>

%wps_object_create_end

%postun
%wps_object_delete_all

%files
%defattr(-,root,root)
%doc src/cron2.doc
%doc src/cron2.ico
%{_bindir}/*.exe
%config(noreplace) %{_sysconfdir}/cron2.dat
%ghost %{_localstatedir}/log/cron2.log

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg

%changelog
* Tue Aug 25 2015 yd <yd@os2power.com> 1.4.2-1
- initial build with unixroot support for /@unixroot/etc/cron2.dat and default
  logging to /@unixroot/var/log/cron2.log.

