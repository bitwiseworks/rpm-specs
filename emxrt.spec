
Summary: EMX runtime
Name: emxrt
Version: 0.9d
Release: 1
License: free software
Group: Development/Languages
Source0: emxrt.zip

%description
The emx runtime is an environment for 32-bit programs under OS/2 2.x, OS/2 3.x
 (OS/2, in short), MS-DOS, and PC-DOS (DOS, in short) on machines with a 
386 CPU (or one of its successors). 

%prep
%setup -q -c

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p %{buildroot}%{_usr}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_defaultdocdir}/emxrt

cp emx/bin/* %{buildroot}%{_bindir}
cp emx/book/* %{buildroot}%{_defaultdocdir}/emxrt
cp emx/doc/* %{buildroot}%{_defaultdocdir}/emxrt
cp emx/dll/* %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%{_usr}/*

%changelog
