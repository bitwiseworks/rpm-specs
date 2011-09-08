Summary: Wrap REXX scrips into OS/2 PM or VIO executables
Name: rexx_exe
Version: 2006.04.10
Release: 3%{?dist}
License: None
Group: System Environment/Shells
Source: rexx_exe.zip

%description
This package has two programs to wrap a rexx program in either a VIO
(commandline) or PM (presentation manager) executable. You probably know
some other rexx -> exe converters like VXRexx, Vispro, REXX2EXE,...
Features of this implementation:
 - build from assembler source: small size - comes close or is below
   the size of the wrapped rexx, less processing overhead and memory usage
 - turns the rexx scripts into plain executable resources - no need to
   compress the resources since the OS build in page compression can be
   used. Use LxLite to squeeze the last byte from the executable..
   I also see no need to encrypt a rexx script. Since there is nothing
   'compiled' or tokenized, the rexx program should be portable between
   different OS/2 rexx interpreter versions and lines.


%prep
%setup -q -c


%build


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_bindir}
cp exe/rexx_pm.exe %{buildroot}/%{_bindir}
cp exe/rexx_vio.exe %{buildroot}/%{_bindir}
cp exe/rexx2pm.exe %{buildroot}/%{_bindir}
cp exe/rexx2vio.exe %{buildroot}/%{_bindir}


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root)
%{_bindir}/*.exe
%doc doc/rexx_exe.txt
%doc doc/autor.txt


%changelog
20110908 use a temporary name for resource files, fixes smp builds.
