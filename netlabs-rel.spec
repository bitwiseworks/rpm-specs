
Summary: Netlabs Stable Repository
Name: netlabs-rel
Version: 0.0.0
Release: 1

License: free

Source: netlabs-rel.zip

Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
Netlabs Experimental Repository.
Use with caution, packages on this repository are not considered stable versions.

%prep
%setup -q -c

%build
# nothing to do

%install
mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d
cp netlabs-rel.repo $RPM_BUILD_ROOT/%{_sysconfdir}/yum/repos.d/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%config(noreplace) %{_sysconfdir}/yum/repos.d/*.repo
