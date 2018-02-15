
Summary: Netlabs Experimental Repository
Name: netlabs-exp
Version: 0.0.0
Release: 5%{?dist}
License: free
Vendor:  netlabs.org
BuildArch: noarch

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
Netlabs Experimental Repository.
Use with caution, packages on this repository are not considered stable versions.


%prep
# nothing to do


%build
# nothing to do


%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d
cat << EOF > %{buildroot}%{_sysconfdir}/yum/repos.d/netlabs-exp.repo
[netlabs-exp]
name=Netlabs experimental repository \$releasever - \$basearch
baseurl=http://rpm.netlabs.org/experimental/\$releasever/\$basearch/
        http://www.2rosenthals.com/rpm.netlabs.org/experimental/\$releasever/\$basearch/
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

* Mon Jan 07 2013 yd
- add US mirror URL.
