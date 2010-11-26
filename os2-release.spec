%define release_name Prelude
%define dist_version 00

Summary:	OS/2 release files
Name:		os2-release
Version:	%{dist_version}
Release:        2%{?dist}
License:	GPLv2
Group:		System Environment/Base
URL:		http://www.netlabs.org

Obsoletes:	redhat-release
Provides:	redhat-release
Provides:	system-release = %{version}-%{release}
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:	noarch

%description
Package for release management for OS/2 and eComStation.
Note that Version code in this package selects the repository release for 
Yum downloads.

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}
echo "OS/2 release %{version} (%{release_name})" > $RPM_BUILD_ROOT%{_sysconfdir}/os2-release

# Set up the dist tag macros
install -d -m 755 $RPM_BUILD_ROOT%{_sysconfdir}/rpm
cat >> $RPM_BUILD_ROOT%{_sysconfdir}/rpm/macros.dist << EOF
# dist macros.

%%os2		%{dist_version}
%%dist		.oc%{dist_version}
%%oc%{dist_version}		1
EOF

%files
%defattr(-,root,root,-)
%config %attr(0644,root,root) %{_sysconfdir}/os2-release
%config %attr(0644,root,root) %{_sysconfdir}/rpm/macros.dist
