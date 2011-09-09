Summary: Free rexx "compiler" (generates .EXE from .CMD)
Name: rexx2exe
Version: 99.349
Release: 2%{?dist}
License: None
Group: System Environment/Shells
Source: rexx2exe.zip

%description
This tool has many generation options and allowes
you to create PM programs (makes using
RxMessageBox() easier), standalone programs or
smaller programs that require a generated DLL.
The code is optionally encrypted and packed so
the generated code can be quite small.


%prep
%setup -q -c


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
cp -p rexx2exe.exe %{buildroot}/%{_bindir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/rexx2exe.exe
%doc rexx2exe.txt
%doc rexx2exe.inf
