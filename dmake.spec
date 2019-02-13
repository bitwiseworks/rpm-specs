Summary:	Dmake is a make utility similar to GNU make
Name:		dmake
Version:	4.12
Release:	1
License:	GPL v1
Group:          Development/Languages
URL:		https://github.com/mohawk2/dmake

%scm_source github https://github.com/mohawk2/dmake master
#scm_source git file://F:/rd/ports/dmake/dmake master

%description
Dmake is a make utility similar to GNU make


%debug_package


%prep
%scm_setup


%build
export LDFLAGS="-Zomf -Zhigh-mem -Zargs-wild -Zargs-resp"
autoreconf -i
%configure --enable-spawn
%{__make} %{?_smp_mflags} 


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(644,root,root,755)
%{_bindir}/dmake.exe
%{_datadir}/startup/


%changelog
* Tue Feb 12 2019 yd <yd@os2power.com> 4.12-1
- initial rpm build.
