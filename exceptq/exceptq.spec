#disable lxlite strip
%define __os_install_post	%{nil}

Summary: Exceptq creates a debugging report.
Name: exceptq
Version: 7.11.6
Release: 1%{?dist}
License: custom
Group: Development/Libraries
Source: exceptq-7.11.6-shl-2023-02-23.zip

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

cp -p lib/*.dll %{buildroot}%{_libdir}
cp -p lib/*.xqs %{buildroot}%{_libdir}
cp -p lib/*.lib %{buildroot}%{_libdir}

cp -p bin/mapxqs.* %{buildroot}%{_bindir}
cp -p include/exceptq.h %{buildroot}%{_includedir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_libdir}/*.dll
%{_libdir}/*.xqs
%doc exceptq.txt
%doc exceptq-shl.txt
%doc HISTORY
%doc readme.exceptq

%files devel
%defattr(-,root,root)
%{_bindir}/*
%{_libdir}/*.lib
%{_includedir}/*.h

%changelog
* Wed May 10 2023 Dmitriy Kuminov <coding@dmik.org> 7.11.6-1
- Update to 7.11.6-shl-2023-02-23 binaries.

* Fri Feb 26 2021 Dmitriy Kuminov <coding@dmik.org> 7.11.5-1
- Update to 7.11.5-shl-beta8-2020-06-01 binaries.
- Clean up spec file.

* Mon Aug 01 2016 yd <yd@os2power.com> 7.11.3-1
- update to SHL 2016-07-27 binaries.
- revert header fix.

* Tue May 20 2014 Dmitriy Kuminov <coding@dmik.org> 7.11-9
- Patch exceptq.h to fix usage in muptiple sources.

* Tue Apr 29 2014 yd
- update to SHL 2014-03-03 binaries.

* Fri Feb 28 2014 yd
- update to SHL 2014-02-07 binaries.

* Mon Oct 28 2013 yd
- update to SHL 2013-10-15 binaries.
