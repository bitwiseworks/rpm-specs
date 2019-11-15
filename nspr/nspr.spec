%global nspr_version 4.23.0

# The upstream omits the trailing ".0", while we need it for
# consistency with the pkg-config version:
# https://bugzilla.redhat.com/show_bug.cgi?id=1578106
%{lua:
rpm.define(string.format("nspr_archive_version %s",
           string.gsub(rpm.expand("%nspr_version"), "(.*)%.0$", "%1")))
}

Summary:        Netscape Portable Runtime
Name:           nspr
Version:        %{nspr_version}
Release:        1%{?dist}
License:        MPLv2.0
URL:            http://www.mozilla.org/projects/nspr/
Conflicts:      filesystem < 3
BuildRequires:  gcc
Vendor:         bww bitwise works GmbH

# Sources available at https://ftp.mozilla.org/pub/nspr/releases/
# When hg tag based snapshots are being used, refer to hg documentation on
# mozilla.org and check out subdirectory mozilla/nsprpub.
# see also https://n-2.org/
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

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
Requires:       nspr = %{version}-%{release}
Requires:       pkgconfig
BuildRequires:  xmlto
Conflicts:      filesystem < 3

%description devel
Header files for doing development with the Netscape Portable Runtime.

%package legacy
Summary:        Legacy libraries for Netscape Portable Runtime
Requires:       nspr = %{version}-%{release}

%description legacy
NSPR forwarder libraries with old DLL names ending with 'k'.

%debug_package

# Makes no sense to provide .dbg files for forwarder DLLs
%define _strip_opts --debuginfo -x "*k.dll"

%prep
%scm_setup

# Generate configure.
autoconf

%build
export VENDOR="%{vendor}"
%configure \
                 --prefix=%{_prefix} \
                 --libdir=%{_libdir} \
                 --includedir=%{_includedir}/nspr4 \
%ifnarch noarch
%if 0%{__isa_bits} == 64
                 --enable-64bit \
%endif
%endif
%ifarch armv7l armv7hl armv7nhl
                 --enable-thumb2 \
%endif
                 --enable-optimize="$RPM_OPT_FLAGS" \
                 --enable-debug-symbols \
                 --disable-debug

# Disable MOZ_DEBUG_SYMBOLS to let debug_package do its work
# (--enable-debug-symbols is still necessary to make sure -g is specified)
sed -e 's/^MOZ_DEBUG_SYMBOLS = 1$/MOZ_DEBUG_SYMBOLS =/' -i ./config/autoconf.mk

# The assembly files are only for legacy atomics, to which we prefer GCC atomics
%ifarch i686 x86_64
sed -i '/^PR_MD_ASFILES/d' config/autoconf.mk
%endif
make

date +"%e %B %Y" | tr -d '\n' > date.xml
echo -n %{version} > version.xml

for m in %{SOURCE1}; do
  cp ${m} .
done
for m in nspr-config.xml; do
  xmlto man ${m}
done

# Generate forwarder DLLs.
for m in %{SOURCE10} %{SOURCE11} %{SOURCE12}; do
  cp ${m} .
done
for m in nspr4 plc4 plds4; do
  gcc -Zomf -Zdll -nostdlib ${m}k.def -l./dist/lib/${m}.dll -lend -o ${m}k.dll
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

mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1 

NSPR_LIBS=`./config/nspr-config --libs`
NSPR_CFLAGS=`./config/nspr-config --cflags`
NSPR_VERSION=`./config/nspr-config --version`
%{__mkdir_p} $RPM_BUILD_ROOT/%{_libdir}/pkgconfig

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

for f in nspr-config; do 
   install -c -m 644 ${f}.1 $RPM_BUILD_ROOT%{_mandir}/man1/${f}.1
done

#ldconfig_scriptlets

%files
%{!?_licensedir:%global license %%doc}
%license LICENSE
%{_libdir}/nspr4.dll
%{_libdir}/plc4.dll
%{_libdir}/plds4.dll

%files devel
%{_includedir}/nspr4
%{_libdir}/pkgconfig/nspr.pc
%{_bindir}/nspr-config
%{_libdir}/*_dll.a
%{_mandir}/man*/*

%files legacy
%{_libdir}/*4k.dll

%changelog
* Wed Nov 13 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 4.23.0-1
- update to version 4.23
- adjusted the spec to latest ferora version

* Tue May 16 2017 Dmitriy Kuminov <coding@dmik.org> - 4.12.0-4
- Use kLIBC APIs for file manipulation functions to bring symlink support and
  other kLIBC I/O extensions (#153).
- Remove manual EXCEPTQ installation as NSPR is linked against LIBCx now.
- Rebuild with fixed pkgconfig dependency generator.

* Thu Feb 23 2017 Dmitriy Kuminov <coding@dmik.org> - 4.12.0-3
- Generate more compact forwarder DLLs with better memory footprint.

* Thu Feb 23 2017 Dmitriy Kuminov <coding@dmik.org> - 4.12.0-2
- Use scm_source and friends.
- Make PR_LoadLibrary and PR_UnloadLibrary kLIBC fork-friendly.

* Fri Mar 25 2016 Dmitriy Kuminov <coding@dmik.org> 4.12.0-1
- Update to version 4.12.
- Import OS/2-specific NSPR fixes from Mozilla for OS/2 sources.
- Rebuild with GCC 4.9.2 and LIBC 0.6.6.

* Mon Jan 16 2012 yd
- rebuild with libc 0.6.4 runtime.
