%define release_name Prelude
%define dist_version 00

Summary:	OS/2 release files
Name:		os2-release
Version:	%{dist_version}
Release:        4%{?dist}
License:	GPLv2
Group:		System Environment/Base
URL:		http://www.netlabs.org

Obsoletes:	redhat-release
Provides:	redhat-release
Provides:	system-release = %{version}-%{release}
BuildArch:	noarch

%description
Package for release management for OS/2 and eComStation.
Note that Version code in this package selects the repository release for 
Yum downloads.

%install
install -d $RPM_BUILD_ROOT%{_sysconfdir}
echo "OS/2 release %{version} (%{release_name})" > $RPM_BUILD_ROOT%{_sysconfdir}/os2-release

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.dist << EOF
# dist macros.

%%os2		%{dist_version}
%%dist		.oc%{dist_version}
%%oc%{dist_version}		1
%%os2_version	5
EOF

%files
%defattr(-,root,root,-)
%config %attr(0644,root,root) %{_sysconfdir}/os2-release
%config %attr(0644,root,root) %{_sysconfdir}/rpm/macros.dist

%changelog
* Wed Mar 18 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 00-4
- add os2_version to macros.dist, so %%if %%{os2_version} works in spec files

* Mon Aug 29 2011 yd <yd@os2power.com> 00-3
- massive rebuild (not released spec)

* Fri Nov 26 2010 yd <yd@os2power.com> 00-2
- added dist tag to release build number

* Fri Oct 29 2010 yd <yd@os2power.com> 00-1
- first os/2 rpm
