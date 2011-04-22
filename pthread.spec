Summary: A posix pthread emulation for OS/2-eComStation
Name: pthread
Version: 20110422
Release: 4%{?dist}
License: unknown
Group: Development/Libraries
Source: pthread-%{version}-os2.zip
Source1: pthread-legacy-os2.zip

Requires: libc >= 0.6.3

%description
A posix pthread emulation library.

%package devel
Summary: Header files developing apps which will use pthread
Group: Development/Libraries

%description devel
Header files and a library of pthread functions, for developing apps
which will use the library.

%package legacy
Summary: The previous posix pthread emulation library.

%description legacy
The previous posix pthread emulation library.

%prep
%setup -q -c -a 1


%build
export KCFLAGS="%{optflags}"
kmk -C src
kmk -C src build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp pthread.dll %{buildroot}%{_libdir}
cp pthr01.dll %{buildroot}%{_libdir}
cp pthread.h %{buildroot}%{_includedir}
cp pthread.a %{buildroot}%{_libdir}/pthread.a
cp pthread_s.a %{buildroot}%{_libdir}/pthread_s.a
cp pthread_g.a %{buildroot}%{_libdir}/pthread_g.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/pthr??.dll

%files devel
%defattr(-,root,root)
%{_libdir}/*.a
%{_includedir}/*

%files legacy
%defattr(-,root,root)
%{_libdir}/pthread.dll
