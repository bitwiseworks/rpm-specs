%if !0%{?os2_version}
%bcond_without selinux
%else
%bcond_with selinux
%endif
# Don't run check on 32-bit arches, seems to be issues with some tests
%ifarch %{ix86} %{arm} || 0%{?os2_version}
%bcond_with check
%else
%bcond_without check
%endif

Summary: GNU file archiving program
Name: tar
Epoch: 2
Version: 1.35
Release: 1%{?dist}
License: GPL-3.0-or-later
URL: https://www.gnu.org/software/tar/

%if !0%{?os2_version}
Source0: https://ftp.gnu.org/gnu/tar/tar-%{version}.tar.xz
Source1: https://ftp.gnu.org/gnu/tar/tar-%{version}.tar.xz.sig

# Note that all patches are documented in patch files (git format-patch format)
Patch1:  tar-1.28-loneZeroWarning.patch
Patch2:  tar-1.28-vfatTruncate.patch
Patch3:  tar-1.29-wildcards.patch
Patch4:  tar-1.28-atime-rofs.patch
Patch9:  tar-1.28-document-exclude-mistakes.patch
Patch10: tar-1.33-fix-capabilities-test.patch
Patch11: tar-1.35-padding-zeros.patch
Patch12: tar-1.30-disk-read-error.patch
Patch13: tar-1.35-fix-spurious-diagnostic-during-extraction-of-.-with-keep-newer-files.patch
Patch14: tar-1.35-add-forgotten-tests-from-upstream.patch
Patch15: tar-1.35-revert-fix-savannah-bug-633567.patch
# Source: https://cgit.git.savannah.gnu.org/cgit/tar.git/diff/?id=5114218025b4562392dd260e2533d3fa2bc0220e
Patch16: tar-1.35-Fix-Savane-bug-64581.patch
# Source: https://cgit.git.savannah.gnu.org/cgit/tar.git/diff/?id=4e742fc8674064a9fa00d4483d06aca48d5b0463
Patch22: tar-1.35-no-overwrite-dir-no-overwrite-even-temporarily.patch
#tar commits from upstream
# 56fb4a96ca43c247261b8c04dd65592f990f98ac
# 7c241126f14975c7f5df4268b434f276fc7f8842
# bdd773d028cd21f9b76b8cc306c57e0db3607e82
# cdb586803b762d9021db2ae8bf5dad3f9b8e4f77
# 915a8077af12a3eaf7800dbb1a4259783d9933ca
# 8fca2d35e88d10f0ddcb36720e88f40ac57f67f0
# e1445cfdf0dfd2f792532afc1eb18b01523dbfb4
# 75b03fdff48916bd0654677ed21379bdb0db016d
# 8767b1c84a910cce562059abad5bbf14e72434a0
#Gnulib commits from upstream to bring openat2 support
# 0b97ffdf32bdab909d02449043447237273df75e
# c706216fec5a509bf9b1214892de01aa9303ade0
# c6502cda83752ff2235d2064c213e7a9e2214201
# 5746cd1cdbb2caf0e321ea79041885fc7ef22423
# 3d23c8df2582a6b0e44e048d431ecb00a14667ec
# a209366ed34eca8ede481ec1b1c4e22f614c448d
# 8e85114bf1d51d9ea54a89f058c3a2cfa0c19c5e
# 6bff6c3741209e933e721e81e1b5c5abdbd4389a
# 24d2acd301cea7cde1928c84f926a54707e945d5
# 4e1fa851f4f43f749d18b83500757f5bcf1f47bd
# 20074698382b7e4f049f52bbdeaf6a39508a8601
# d1aeb7388926e045bdec0f7934c5522c4745f02c
# 45b6e6898d1f931bfca41d961289bd6ac33238e5
Patch23: tar-1.35-CVE-2025-45582.patch
# merely a preparation to apply Patch27, the change is obsoleted by it
Patch24: tar-1.35-tar-one-top-level-DIR-must-be-relative.patch
# Source: https://cgit.git.savannah.gnu.org/cgit/tar.git/commit/?id=08c3fc2e9337094aff01a511170fd35fdb8f1ee3
# Fixes build with acl 2.4.0
Patch25: tar-1.35-Avoid-acl_-prefix-for-functions.patch
#Upstream commits
# b009124ffde415515081db844d7a104e1d1c6c58
# b8d8a61b25588caca4efaf9bdd2e3f1a49da77e3
# 67981bbb1587803bb1e029393d2228492cef8c4f
# 19a3a73e8c48bd3c59cbea9b5ed6780fc6836c6d
Patch26: tar-1.35-CVE-2026-5704.patch
#Upstream commits
# bfc33463942060316f70f275471ed202b0076972
# b4fc9ca13617411c5db57286a3ff534bd40acdc1
# 67c8dff6968aae58fcdfb05268eb1b4c07308f1a
# 55e8233438b3c13294109df502a9b220a9a3f4f5
# 0470c109c08f466d8332ba3326070554b4d81aa1
# 1b91f5f66f8e6c490eef0fdee50f652cfe155844
# 325b899214ac13519153318e66c889a31c15342d
# 1980e032afe60c5fe0e5df573457885ece4e69d5
# e335e2c8b102f83b63ffd373f0b88401da3ebe6c
# part of 941f62b2
# Also "by the way" fixes CVE-2026-18508.
Patch27: tar-1.35-fix-absolute-one-top-level.patch
#Upstream commits
# 0714d2f082104005a1c70ee6ec4175194943ea88
# d479b2cc9160d9c2fb61afbc9ee70c2faadf80db
# b17665b2c0548c77b6cd8d2d5b61e4c4fcc4f770
Patch28: tar-1.35-CVE-2026-18477.patch
%else
Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: gettext
%if !0%{?os2_version}
BuildRequires: libacl-devel
%endif
BuildRequires: make
BuildRequires: texinfo

%if %{with check}
# cover needs of tar's testsuite
BuildRequires: attr acl policycoreutils
%endif

%if %{with selinux}
BuildRequires: libselinux-devel
%endif
Provides: bundled(gnulib)
Provides: bundled(paxutils)
%if !0%{?os2_version}
Provides: /bin/tar
Provides: /bin/gtar
%else
Provides: /@unixroot/bin/tar
Provides: /@unixroot/bin/gtar
Provides: /@unixroot/bin/tar.exe
%endif

%description
The GNU tar program saves many files together in one archive and can
restore individual files (or all of the files) from that archive. Tar
can also be used to add supplemental files to an archive and to update
or list files in the archive. Tar includes multivolume support,
automatic archive compression/decompression, the ability to perform
remote archives, and the ability to perform incremental and full
backups.

If you want to use tar for remote backups, you also need to install
the rmt package on the remote box.


%prep
%if !0%{?os2_version}
%autosetup -p1
autoreconf -v
%else
%scm_setup
autoreconf -fvi
%endif

# Keep only entries related to the latest release.
%if !0%{?os2_version}
mv ChangeLog{,~}
%else
mv ChangeLog ChangeLog~
%endif
awk 'stop = false; /^2014-07-27/ { stop = true; exit }; { print }' \
    < ChangeLog~ > ChangeLog


%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export LIBS="-lcx -lintl"
export FORCE_UNSAFE_CONFIGURE=1
%endif
%configure \
    %{!?with_selinux:--without-selinux} \
    --with-lzma="xz --format=lzma" \
    DEFAULT_RMT_DIR=%{_sysconfdir} \
%if !0%{?os2_version}
    RSH=/usr/bin/ssh
%else
    --disable-year2038 \
    RSH=/@unixroot/usr/bin/ssh
%endif

%make_build


%install
%make_install

%if !0%{?os2_version}
ln -s tar $RPM_BUILD_ROOT%{_bindir}/gtar
%else
ln -s tar.exe $RPM_BUILD_ROOT%{_bindir}/gtar
%endif
rm -f $RPM_BUILD_ROOT/%{_infodir}/dir
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
ln -s tar.1.gz $RPM_BUILD_ROOT%{_mandir}/man1/gtar.1

# XXX Nuke unpackaged files.
rm -f $RPM_BUILD_ROOT%{_sysconfdir}/rmt
rm -f $RPM_BUILD_ROOT%{_mandir}/man8/rmt.8*

%find_lang %name


%check
%if %{with check}
rm -f $RPM_BUILD_ROOT/test/testsuite
# make check TESTSUITEFLAGS='-k \!dirrem01,\!dirrem02' || (
make check || (
    # get the error log
    set +x
    find -name testsuite.log | while read line; do
        echo "=== $line ==="
        cat "$line"
        echo
    done
    false
)
%endif


%files -f %{name}.lang
%license COPYING
%doc AUTHORS README THANKS NEWS ChangeLog
%{_bindir}/tar%{_exeext}
%{_bindir}/gtar
%{_mandir}/man1/tar.1*
%{_mandir}/man1/gtar.1*
%{_infodir}/tar.info*


%changelog
* Fri Nov 20 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.35-1
- update to vendor version 1.35
- reworked the spec according to fedora spec

* Thu Feb 02 2012 yd
- Remove symlinks from /bin.

* Thu Jan 28 2012 yd
- Fix change target directory with -C option (libc cannot dup() a directory fd).

* Wed Nov 16 2011 yd
- keep all executables to /usr/bin and place symlinks in /bin
