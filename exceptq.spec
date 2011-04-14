#disable lxlite strip
%define __os_install_post	%{nil}

Summary: Exceptq creates a debugging report.
Name: exceptq
Version: 7.1
Release: 1%{?dist}
License: custom
Group: Development/Libraries
Source: exceptq71.zip
Source1: exceptq.h
Source2: exceptq71-dev.zip

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
%setup -q -c -a 2

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_libdir}
mkdir -p %{buildroot}%{_includedir}

cp distorm.* %{buildroot}%{_libdir}
cp exceptq.* %{buildroot}%{_libdir}

cp exceptq71-dev/mapxqs.* %{buildroot}%{_bindir}
cp exceptq71-dev/demangl.dll %{buildroot}%{_libdir}
cp %{SOURCE1} %{buildroot}%{_includedir}
cp exceptq71-dev/exceptq.lib %{buildroot}%{_libdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.dll
%{_libdir}/*.xqs
%doc readme.exceptq

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_includedir}/*.h
%{_libdir}/*.lib
%doc exceptq71-dev/exceptq.txt
