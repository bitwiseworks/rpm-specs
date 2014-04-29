#disable lxlite strip
%define __os_install_post	%{nil}

Summary: Exceptq creates a debugging report.
Name: exceptq
Version: 7.11
Release: 8%{?dist}
License: custom
Group: Development/Libraries
Source: exceptq-7.11-shl-2014-03-03.zip
#Source1: exceptq.h
#Source2: exceptq71-dev.zip

%description
Exceptq creates a debugging report whenever a program that uses it
encounters a fatal exception (i.e. the app crashes).  Programmers can
also use it to generate debugging reports while the app is running.

It emits a two-tone beep, then generates the report and puts it in the
directory containing the .exe that crashed.  The name is based on the
IDs of the process and thread that encountered the problem.  For example,
'006C_01.TRP' describes a trap in process 6C, thread 1.

Reports are typically 10-30k - small enough that it should be easy to
email them to the program's author, even on dialup.  Most of the info
they contain is of little value to the user.  However, you may want to
examine the last section, "DLLs accessible from this process", to see
if a dll was loaded from an incorrect or unexpected directory.

If you have any questions about Exceptq - or any problems with it,
please contact:

  Rich Walsh <rich@e-vertise.com>
or
  Steven Levine <steve53@earthlink.net>

%package devel
Summary: Exceptq developer package

%description devel
Exceptq developer package


%prep
%setup -q -c

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp -p dll/*.dll %{buildroot}%{_libdir}
cp -p dll/*.xqs %{buildroot}%{_libdir}

cp -p bin/mapxqs.* %{buildroot}%{_bindir}
#cp -p exceptq71-dev/demangl.dll %{buildroot}%{_libdir}
cp -p include/exceptq.h %{buildroot}%{_includedir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.dll
#%exclude %{_libdir}/demangl.dll
%{_libdir}/*.xqs
#%doc distorm-shl.txt
%doc exceptq.txt
%doc exceptq-shl.txt
%doc HISTORY
%doc readme.exceptq

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*.h
#%{_libdir}/demangl.dll
#%doc distorm-shl.txt
%doc exceptq.txt
%doc exceptq-shl.txt
%doc HISTORY
%doc readme.exceptq

%changelog
* Tue Apr 29 2014 yd
- update to SHL 2014-03-03 binaries.

* Fri Feb 28 2014 yd
- update to SHL 2014-02-07 binaries.

* Mon Oct 28 2013 yd
- update to SHL 2013-10-15 binaries.
