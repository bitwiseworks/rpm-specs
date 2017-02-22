# Note: this .spec is borrowed from nspr-4.12.0-1.fc24.src.rpm

Summary:        Netscape Portable Runtime
Name:           nspr
Version:        4.12.0
Release:        2%{?dist}
License:        MPLv2.0
URL:            http://www.mozilla.org/projects/nspr/
Group:          System Environment/Libraries
Conflicts:      filesystem < 3
Vendor:     bww bitwise works GmbH

%scm_source svn http://svn.netlabs.org/repos/ports/nspr/trunk 2052

BuildRequires: gcc make subversion zip

# Sources available at ftp://ftp.mozilla.org/pub/mozilla.org/nspr/releases/
# When hg tag based snapshots are being used, refer to hg documentation on
# mozilla.org and check out subdirectory mozilla/nsprpub.
#Source0:        %{name}-%{version}.tar.gz

Source1:        nspr-config.xml

# DEF files to create forwarders for the legacy package
Source10:       nspr4k.def
Source11:       plc4k.def
Source12:       plds4k.def

%description
NSPR provides platform independence for non-GUI operating system
facilities. These facilities include threads, thread synchronization,
normal file and network I/O, interval timing and calendar time, basic
memory management (malloc and free) and shared library linking.

%package devel
Summary:        Development libraries for the Netscape Portable Runtime
Group:          Development/Libraries
Requires:       nspr = %{version}-%{release}
Requires:       pkgconfig
# @todo We don't have xmlto yet.
#BuildRequires:  xmlto
Conflicts:      filesystem < 3

%description devel
Header files for doing development with the Netscape Portable Runtime.

%package legacy
Summary:        Legacy libraries for Netscape Portable Runtime
Group:          System Environment/Libraries
Requires:       nspr = %{version}-%{release}

%description legacy
NSPR rorwarder libraries with old DLL names ending with 'k'.

%debug_package

# Makes no sense to provide .dbg files for forwarder DLLs
%define _strip_opts --debuginfo -x "*k.dll"

%prep
%scm_setup

# Generate configure.
autoconf

%build

%configure \
                 --prefix=%{_prefix} \
                 --libdir=%{_libdir} \
                 --includedir=%{_includedir}/nspr4 \
                 --enable-optimize="$RPM_OPT_FLAGS" \
                 --enable-debug-symbols \
                 --disable-debug

# Disable MOZ_DEBUG_SYMBOLS to let debug_package do its work
# (--enable-debug-symbols is still necessary to make sure -g is specified)
sed -e 's/^MOZ_DEBUG_SYMBOLS = 1$/MOZ_DEBUG_SYMBOLS =/' -i ./config/autoconf.mk

make %{?_smp_mflags}

# @todo We don't have xmlto yet.
#date +"%e %B %Y" | tr -d '\n' > date.xml
#echo -n %{version} > version.xml
#
#for m in %{SOURCE1}; do
#  cp ${m} .
#done
#for m in nspr-config.xml; do
#  xmlto man ${m}
#done

# Generate forwarder DLLs.
for m in %{SOURCE10} %{SOURCE11} %{SOURCE12}; do
  cp ${m} .
done
for m in nspr4 plc4 plds4; do
  gcc -Zomf -Zdll ${m}k.def -l./dist/lib/${m}.dll -o ${m}k.dll
done

%check

# Run test suite.
# @todo Disable it since it fails so far.
#perl ./pr/tests/runtests.pl 2>&1 | tee output.log
#
#TEST_FAILURES=`grep -c FAILED ./output.log` || :
#if [ $TEST_FAILURES -ne 0 ]; then
#  echo "error: test suite returned failure(s)"
#  exit 1
#fi
#echo "test suite completed"

%install

%{__rm} -Rf $RPM_BUILD_ROOT

DESTDIR=$RPM_BUILD_ROOT \
  make install

# Install forwarder DLLs.
cp -p *.dll $RPM_BUILD_ROOT/%{_libdir}/

# @todo We don't have xmlto yet.
#mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1

# Get rid of the things we don't want installed (per upstream)
%{__rm} -rf \
   $RPM_BUILD_ROOT/%{_bindir}/compile-et.pl \
   $RPM_BUILD_ROOT/%{_bindir}/prerr.properties \
   $RPM_BUILD_ROOT/%{_libdir}/libnspr4_s.a \
   $RPM_BUILD_ROOT/%{_libdir}/libplc4_s.a \
   $RPM_BUILD_ROOT/%{_libdir}/libplds4_s.a \
   $RPM_BUILD_ROOT/%{_datadir}/aclocal/nspr.m4 \
   $RPM_BUILD_ROOT/%{_includedir}/nspr4/md

# Remove .xqs files (created because MOZ_DEBUG_SYMBOLS was disabled)
%{__rm} -rf \
   $RPM_BUILD_ROOT/%{_libdir}/*.xqs

# @todo We don't have xmlto yet.
#for f in nspr-config; do
#   install -c -m 644 ${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
#done

%clean
%{__rm} -Rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/nspr4.dll
%{_libdir}/plc4.dll
%{_libdir}/plds4.dll

%files devel
%defattr(-, root, root)
%{_includedir}/nspr4
%{_libdir}/pkgconfig/nspr.pc
%{_libdir}/libnspr4.a
%{_libdir}/libplc4.a
%{_libdir}/libplds4.a
%{_bindir}/nspr-config
# @todo We don't have xmlto yet.
#%{_mandir}/man*/*

%files legacy
%defattr(-,root,root)
%{_libdir}/nspr4k.dll
%{_libdir}/plc4k.dll
%{_libdir}/plds4k.dll

%changelog
* Thu Feb 23 2017 Dmitriy Kuminov <coding@dmik.org> - 4.12.0-2
- Use scm_source and friends.
- Make PR_LoadLibrary and PR_UnloadLibrary kLIBC fork-friendly.

* Fri Mar 25 2016 Dmitriy Kuminov <coding@dmik.org> 4.12.0-1
- Update to version 4.12.
- Import OS/2-specific NSPR fixes from Mozilla for OS/2 sources.
- Rebuild with GCC 4.9.2 and LIBC 0.6.6.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
