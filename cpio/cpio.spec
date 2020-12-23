Summary: A GNU archiving program
Name: cpio
Version: 2.13
Release: 1%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/cpio/
%if !0%{?os2_version}
Source: ftp://ftp.gnu.org/gnu/cpio/cpio-%{version}.tar.bz2

# help2man generated manual page distributed only in RHEL/Fedora
Source1: cpio.1

# We use SVR4 portable format as default.
Patch1: cpio-2.9-rh.patch

# fix warn_if_file_changed() and set exit code to 1 when cpio fails to store
# file > 4GB (#183224)
# http://lists.gnu.org/archive/html/bug-cpio/2006-11/msg00000.html
Patch2: cpio-2.13-exitCode.patch

# Support major/minor device numbers over 127 (bz#450109)
# http://lists.gnu.org/archive/html/bug-cpio/2008-07/msg00000.html
Patch3: cpio-2.13-dev_number.patch

# Define default remote shell as /usr/bin/ssh (#452904)
Patch4: cpio-2.9.90-defaultremoteshell.patch

# Fix segfault with nonexisting file with patternnames (#567022)
# http://savannah.gnu.org/bugs/index.php?28954
# We have slightly different solution than upstream.
Patch5: cpio-2.10-patternnamesigsegv.patch

# Fix bad file name splitting while creating ustar archive (#866467)
# (fix backported from tar's source)
Patch7: cpio-2.10-longnames-split.patch

# Cpio does Sum32 checksum, not CRC (downstream)
Patch8: cpio-2.11-crc-fips-nit.patch

# Fix multiple definition of `program_name'
Patch9: cpio-2.13-mutiple-definition.patch

# Revert fix for CVE-2015-1197 (#1797163)
# reverts upstream commit 45b0ee2b4
Patch10: cpio-2.13-revert-CVE-2015-1197-fix.patch

# Extract: retain times for symlinks
# downstream patch (#1486364)
# https://www.mail-archive.com/bug-cpio@gnu.org/msg00605.html
Patch11: cpio-2.11-retain-symlink-times.patch
%else
Vendor:  bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

%if !0%{?os2_version}
Provides: bundled(gnulib)
Provides: bundled(paxutils)
Provides: /bin/cpio
%endif
BuildRequires: gcc
%if !0%{?os2_version}
BuildRequires: texinfo, autoconf, automake, gettext, gettext-devel, rmt
%else
BuildRequires: texinfo, autoconf, automake, gettext, gettext-devel
%endif
BuildRequires: make

%description
GNU cpio copies files into or out of a cpio or tar archive.  Archives
are files which contain a collection of other files plus information
about them, such as their file name, owner, timestamps, and access
permissions.  The archive can be another file on the disk, a magnetic
tape, or a pipe.  GNU cpio supports the following archive formats:  binary,
old ASCII, new ASCII, crc, HPUX binary, HPUX old ASCII, old tar and POSIX.1
tar.  By default, cpio creates binary format archives, so that they are
compatible with older cpio programs.  When it is extracting files from
archives, cpio automatically recognizes which kind of archive it is reading
and can read archives created on machines with a different byte-order.

Install cpio if you need a program to manage file archives.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif


%build
autoreconf -fi
export CFLAGS="$RPM_OPT_FLAGS -D_GNU_SOURCE -D_FILE_OFFSET_BITS=64 -D_LARGEFILE64_SOURCE -pedantic -fno-strict-aliasing -Wall $CFLAGS"
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
%endif
%configure --with-rmt="%{_sysconfdir}/rmt"
%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif
(cd po && make update-gmo)


%install
%make_install

rm -f $RPM_BUILD_ROOT%{_libexecdir}/rmt
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
%if !0%{?os2_version}
rm -f $RPM_BUILD_ROOT%{_mandir}/man1/*.1*
install -c -p -m 0644 %{SOURCE1} ${RPM_BUILD_ROOT}%{_mandir}/man1
%endif

%find_lang %{name}

%check
rm -f ${RPM_BUILD_ROOT}/test/testsuite
make check || {
    echo "### TESTSUITE.LOG ###"
    cat tests/testsuite.log
    exit 1
}


%files -f %{name}.lang
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/*
%if 0%{?os2_version}
%exclude %{_bindir}/*.dbg
%endif
%{_mandir}/man*/*
%{_infodir}/*.info*

%changelog
* Mon Dec 21 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.13-1
- update to vendor version 2.13
- use scm_* macros
- resynced with fedora spec

* Fri Feb 03 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.12-1
- update to vendor version 2.12
- update some gnulib tool to latest gnulib

* Fri Oct 14 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2.11-5
- add debug package
- adapt to latest toolchain
- fixed utimes usage
- rolled back r164 partially

* Mon Dec 03 2012 yd
- remove file name ending \r due to binary stdin. fixes ticket:16.
