
Summary: Netlabs Stable Repository
Name: netlabs-rel
Version: 0.0.0
Release: 5%{?dist}

License: free

Source: netlabs-rel.zip

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Netlabs Release Repository.
This is the recommended repository for users since packages on this repository
are considered stable versions.

%prep
%setup -q -c

%build
# nothing to do

%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d
cp -p netlabs-rel.repo $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%config(noreplace) %{_sysconfdir}/yum/repos.d/*.repo


%changelog
* Wed Jan 21 2015 yd
- fixed description. ticket#105.

* Mon Jan 07 2013 yd
- add US mirror URL.

