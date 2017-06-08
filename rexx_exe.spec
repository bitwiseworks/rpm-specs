Summary: Wrap REXX scrips into OS/2 PM or VIO executables
Name: rexx_exe
Epoch: 1
Version: 1.0.0
Release: 1%{?dist}
License: None
Group: System Environment/Shells
Vendor: bww bitwise works GmbH

%scm_source github https://github.com/bitwiseworks/rexx_exe 0c61199a23285f592eda44f9f9c66a54d05f40c7

Requires: os2tk45-rc
BuildRequires: os2tk45-rc

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
%scm_setup


%build
# Tailor converter scripts to search for helper in usr/lib/%{name}
for f in exe/rexx2vio.cmd exe/rexx2pm.cmd ; do
  # Due to bug in sed 4.2.1-2 -i kills CRLF in processed files, so use redirection
  %{__sed} -e 's|rexx2xx.cmd|..\\lib\\%{name}\\rexx2xx.exe|g' -e 's|@call|@|g' "$f" > "$f.new"
  %{__rm} "$f"
  %{__mv} "$f.new" "$f"
done
# Convert all scripts to VIO EXE
for f in exe/*.cmd ; do
  exe/rexx2xx.cmd vio "$f"
done


%install
%{__rm} -rf %{buildroot}
%{__mkdir_p} %{buildroot}%{_bindir}
%{__cp} -p exe/rexx2pm.exe %{buildroot}%{_bindir}
%{__cp} -p exe/rexx2vio.exe %{buildroot}%{_bindir}
%{__mkdir_p} %{buildroot}%{_libdir}/%{name}
%{__cp} -p exe/rexx_pm.exe %{buildroot}%{_libdir}/%{name}
%{__cp} -p exe/rexx_vio.exe %{buildroot}%{_libdir}/%{name}
%{__cp} -p exe/rexx2xx.exe %{buildroot}%{_libdir}/%{name}


%clean
%{__rm} -rf %{buildroot}


%files
%{_bindir}/*.exe
%{_libdir}/%{name}/*.exe
%doc doc/rexx_exe.txt
%doc doc/autor.txt


%changelog
* Thu Jun 8 2017 Dmitriy Kuminov <coding@dmik.org> 1.0.0-1
- Store binary distribution on github for easy patching.
- Change epoch to 1 due to changed versioning scheme.
- Fix converter execution failure with no arguments.
- Use single source base for both rexx2vio.cmd and rexx2pm.cmd.
- Properly handle errors and use output EXE dir for temp files instead of TMP.
- Prefer RC16.EXE to RC.EXE when choosing resource compiler.
- Install VIO/PM stubs and helper script to usr/lib/rexx_exe instead of usr/bin.
- Depend on os2tk45 that provides RC16.EXE.

* Thu Sep 08 2011 yd
- use a temporary name for resource files, fixes smp builds.
