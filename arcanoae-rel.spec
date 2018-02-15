
Summary: ArcaNoae Stable Repository
Name:    arcanoae-rel
Version: 0.0.0
Release: 1%{?dist}
License: free
Vendor:  Arca Noae LLC
BuildArch: noarch

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)


%description
ArcaNoae Release Repository.
This is the recommended repository for users since packages in this repository
are considered stable versions.


%prep
# nothing to do


%build
# nothing to do


%install
mkdir -p %{buildroot}%{_sysconfdir}/yum/repos.d/
cat << EOF > %{buildroot}%{_sysconfdir}/yum/repos.d/arcanoae-rel.repo
[arcanoae-rel]
name=ArcaNoae stable repository \$releasever
baseurl=https://repos.arcanoae.com/release/\$releasever/
enabled=1
EOF


%clean
rm -rf $RPM_BUILD_ROOT


%files
%config(noreplace) %{_sysconfdir}/yum/repos.d/*.repo


%changelog
* Wed Feb 15 2018 Silvan Scherrer <silvan.scherrer@aroa.ch> - 0.0.0-1
- use NoArch as architecture
- add Vendor
