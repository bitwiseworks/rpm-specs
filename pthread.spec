Summary: A posix pthread emulation for OS/2-eComStation
Name: pthread
Version: 20100929
Release: 1
License: unknown
Group: Development/Libraries
Source: pthread-%{version}-os2.zip

%description
A posix pthread emulation library.

%prep
%setup -q -c


%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp bin/pthread.dll %{buildroot}%{_libdir}
cp include/pthread.h %{buildroot}%{_includedir}
cp lib/pthread_dll.a %{buildroot}%{_libdir}/pthread.a
cp lib/pthread_s.a %{buildroot}%{_libdir}/pthread_s.a
cp lib/pthread_g.a %{buildroot}%{_libdir}/pthread_g.a

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*
%{_includedir}/*
