
Summary: Netlabs Stable Repository
Name: netlabs-rel
Version: 0.0.0
Release: 6%{?dist}
License: free
Vendor:  netlabs.org
BuildArch: noarch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Netlabs Release Repository.
This is the recommended repository for users since packages on this repository
are considered stable versions.


%prep
# nothing to do


%build
# nothing to do


%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d
cat << EOF > %{buildroot}%{_sysconfdir}/yum/repos.d/netlabs-rel.repo
[netlabs-rel]
name=Netlabs Stable Repository \$releasever - \$basearch
baseurl=http://rpm.netlabs.org/release/\$releasever/\$basearch/
        http://www.2rosenthals.com/rpm.netlabs.org/release/\$releasever/\$basearch/
enabled=1
EOF


%clean
rm -rf $RPM_BUILD_ROOT


%files
%config(noreplace) %{_sysconfdir}/yum/repos.d/*.repo


%changelog
* Wed Feb 15 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.0-5
- use NoArch as architecture
- add Vendor
- don't use a external zip file for the source

* Wed Jan 21 2015 yd
- fixed description. ticket#105.

* Mon Jan 07 2013 yd
- add US mirror URL.
