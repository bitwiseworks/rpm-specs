Summary: unlink rename pending operation
Name: urpo
Version: 20111102
Release: 6%{?dist}
License: unknown
Group: Development/Libraries
Source: urpo-%{version}-os2.zip

Requires: libc >= 0.6.3

%description
unlink rename pending operation library.

%prep
%setup -q -c

%build
export KCFLAGS="%{optflags}"
kmk -C src
kmk -C src install
kmk -C src build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp urpo.dll %{buildroot}%{_libdir}
cp urpo_dll.a %{buildroot}%{_libdir}/urpo.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*

%changelog
* Wed Nov 02 2011 yd
- improved build system
