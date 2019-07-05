Name:           check
Version:        0.12.0
Release:        1%{?dist}
Summary:        A unit test framework for C
License:        LGPLv2+
URL:            http://libcheck.github.io/check/
Group:          Development/Tools

Vendor:         bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/check-os2 %{version}-os2

# DEF files to create forwarders for the legacy package
Source10:       check.def

BuildRequires:  gcc
BuildRequires:  libtool
#BuildRequires:  patchutils
BuildRequires:  pkgconfig
#BuildRequires:  subunit-devel
BuildRequires:  texinfo

%description
Check is a unit test framework for C. It features a simple interface for 
defining unit tests, putting little in the way of the developer. Tests 
are run in a separate address space, so Check can catch both assertion 
failures and code errors that cause segmentation faults or other signals. 
The output from unit tests can be used within source code editors and IDEs.

%package devel
Summary:        Libraries and headers for developing programs with check
Group:          Development/Libraries
Requires:       pkgconfig
Requires:       %{name} = %{version}-%{release}

%description devel
Libraries and headers for developing programs with check

%package static
Summary:        Static libraries of check
Group:          Development/Libraries

%description static
Static libraries of check.

%package checkmk
Summary:        Translate concise versions of test suites into C programs
License:        BSD
BuildArch:      noarch
Requires:       %{name} = %{version}-%{release}

%description checkmk
The checkmk binary translates concise versions of test suites into C
programs suitable for use with the Check unit test framework.

%debug_package


%prep
%scm_setup

# Get rid of version control files
find . -name .cvsignore -exec rm {} +

# Regenerate configure
autoreconf -ivf

# Prepare forwarder DLLs.
for m in %{SOURCE10}; do
  cp ${m} .
done


%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"

%configure

make %{?_smp_mflags}

%install
make DESTDIR=$RPM_BUILD_ROOT install
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm -rf $RPM_BUILD_ROOT%{_infodir}/dir
rm -rf $RPM_BUILD_ROOT%{_docdir}/%{name}


# Generate & install forwarder DLLs.
gcc -Zomf -Zdll -nostdlib check.def -l$RPM_BUILD_ROOT/%{_libdir}/check0.dll -lend -o $RPM_BUILD_ROOT/%{_libdir}/check.dll


%check
#export LD_LIBRARY_PATH=$PWD/src/.libs
#make check
# Don't need to package the sh, log or trs files
# when we scoop the other checkmk/test files for doc
rm -rf checkmk/test/check_checkmk*
# these files are empty
rm -rf checkmk/test/empty_input


%files
%doc AUTHORS ChangeLog
%license COPYING.LESSER
%{_libdir}/*.dll
%{_infodir}/check*

%files devel
%doc doc/example
%{_includedir}/check.h
%{_includedir}/check_stdint.h
%{_libdir}/check*_dll.a
%{_libdir}/pkgconfig/check.pc
%{_datadir}/aclocal/check.m4

#check used to be static only, hence this.
%files static
%license COPYING.LESSER
%{_libdir}/check.a

%files checkmk
%doc checkmk/README checkmk/examples
%doc checkmk/test
%{_bindir}/checkmk
%{_mandir}/man1/checkmk.1*

%changelog
* Mon Jul 01 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.12.0-1
- update vendor source to version 0.12.0

* Thu Apr 13 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.11.0-2
- fix a script error

* Mon Apr 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.11.0-1
- update vendor source to version 0.11.0
- move source from netlabs svn to github

* Mon Aug 29 2011 yd <yd@os2power.com> 0.9.8-3
- massive rebuild due to new rpm lx parser updates

* Wed Apr 20 2011 yd <yd@os2power.com> 0.9.8-2
- add target cpu field in cache file

* Wed Nov 10 2010 yd <yd@os2power.com> 0.9.8-1
- first initial rpm
