Summary: unlink rename pending operation
Name: urpo
Version: 20110223
Release: 2%{?dist}
License: unknown
Group: Development/Libraries
Source: urpo-%{version}-os2.zip

Requires: libc >= 0.6.3

%description
unlink rename pending operation library.

%prep
%setup -q -c

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp urpo.dll %{buildroot}%{_libdir}
cp urpo_imp.a %{buildroot}%{_libdir}/urpo.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*
