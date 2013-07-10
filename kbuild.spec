#
# http://svn.netlabs.org/kbuild
#
# NOTES:
# 1. Requires GCC 3.3.5 CSD5 (ftp://ftp.netlabs.org/pub/gcc/GCC-3.3.5-csd5.zip)
# 2. Build with rpmbuild -ba -D "master_mode 1" when packing a new release
#    and changing %svn_rev / %svn_url.
# 3. Use -D "skip_unpack 1" to skip the unpack step when debugging the build.
#

Name:       kbuild
Vendor:     netlabs.org
License:    BSD and GPLv2+
Url:        http://svn.netlabs.org/kbuild

%define ver_major   0
%define ver_minor   1
%define ver_patch   9998

%define os2_release 6

%define rpm_release 1

%define svn_url     http://svn.netlabs.org/repos/kbuild/trunk
%define svn_rev     2687

%define descr_brief kBuild is a GNU Make fork with a set of scripts to simplify\
complex build tasks and portable versions of various UNIX tools to ensure\
cross-platform portability.

%define pkg_docdir      %{_docdir}/%{name}

%if 0%{?os2_release}
Version:    %{ver_major}.%{ver_minor}.%{ver_patch}.%{os2_release}
%else
Version:    %{ver_major}.%{ver_minor}.%{ver_patch}
%endif
Release:    %{rpm_release}

Source:     %{name}-%{version}.zip

Patch1:     kbuild-001-os2_default_inst_dll_to_bin.patch
Patch2:     kbuild-002-gcc3omf_make_ld_ar_quiet.patch
Patch3:     kbuild-003-gcc3omf_support_dll_as_library_source.patch
Patch4:     kbuild-004-gcc3omf_add_rc_support.patch
Patch5:     kbuild-005-gcc3omf_gen_implib_for_dll.patch
Patch7:     kbuild-007-gcc3omf_add_rc_support-NEW.patch

BuildRequires: kbuild

#------------------------------------------------------------------------------
# commons
#------------------------------------------------------------------------------

# TODO: patch -s (2.6.1-3.oc00) always fails, remove this flag from defaults
%define _default_patch_flags %nil

#------------------------------------------------------------------------------
# main package
#------------------------------------------------------------------------------

Summary:    Framework for writing simple makefiles for complex tasks
Group:      System Environment/Libraries

%description
%{descr_brief}

%files
%defattr(-,root,root,-)
%docdir %{pkg_docdir}/
%{_bindir}/*
%exclude %{_bindir}/make.exe
%{_datadir}/*

#------------------------------------------------------------------------------
%package make
#------------------------------------------------------------------------------

Summary:    GNU Make 3.81 implementation based on kBuild's kmk
Group:      System Environment/Libraries
Provides:   make = 3.81

%description make
A GNU Make executable compiled from the kmk source tree. The kmk tool itself is
a fork of GNU Make and this build just disables all kmk-specific features. It
may also contain some minor GNU Make bugfixes not specific to kmk which are
absent from the upstream version. However, this executable should be fully
compatible with the vanilla GNU Make function-wise.

%files make
%defattr(-,root,root,-)
%{_bindir}/make.exe

#------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------

%if 0%{?master_mode}
# get clean source tree from SVN (both for building and for SRPM)
%setup -n "%{name}-%{version}" -Tc
svn export %{svn_url}@%{svn_rev} . --force
# generate SvnInfo.kmk
echo \
"KBUILD_SVN_URL := %{svn_url}@%{svn_rev}
KBUILD_SVN_REV := %{svn_rev}
" > SvnInfo.kmk
# zip it up
rm -f "%{_sourcedir}/%{name}-%{version}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}.zip" "%{name}-%{version}")
%else
# use source zip
%if 0%{?skip_unpack}
%setup -TD
%else
%setup -q
%endif
%endif

%if ! 0%{?skip_unpack}
%patch1
[ $? = 0 ] || exit 1
%patch2
[ $? = 0 ] || exit 1
%patch3
[ $? = 0 ] || exit 1
%patch4
[ $? = 0 ] || exit 1
%patch5
[ $? = 0 ] || exit 1
%patch7
[ $? = 0 ] || exit 1
%endif

#------------------------------------------------------------------------------
%build
#------------------------------------------------------------------------------

# Note: we must remove the leading slash from path overrides, otherwise
# kmk complains about that (kind of a strange bug-o-feature)
%define kmk_env \
    MY_INST_BIN=%{_bindir} \
    MY_INST_DATA=%{_datadir}/kbuild \
    MY_INST_DOC=%{pkg_docdir} \
    KMK_FLAGS="\
        KBUILD_VERBOSE=2 \
        BUILD_TYPE=release \
        NIX_INSTALL_DIR=%{_prefix} \
        MY_INST_BIN=${MY_INST_BIN#/}/ \
        MY_INST_DATA=${MY_INST_DATA#/}/ \
        MY_INST_DOC=${MY_INST_DOC#/}/ \
        MY_INST_MODE=0644 \
        MY_INST_BIN_MODE=0755" \
    unset BUILD_PLATFORM

%{kmk_env}

cmd /c "kBuild\envos2.cmd" kmk $KMK_FLAGS

#------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------

%{kmk_env}

rm -rf "%{buildroot}"

cmd /c "kBuild\envos2.cmd" kmk $KMK_FLAGS PATH_INS="%{buildroot}" install

# We don't want LIBC*.DLL, there is a separate package for them
rm "%{buildroot}%{_bindir}"/*.dll

# Additional docs (not installed by install)
cp -dp COPYING ChangeLog kBuild/doc/COPYING-FDL-1.3 "%{buildroot}%{pkg_docdir}/"

# To make GNU Make we simply copy kmk_gmake.exe, this should be enough
cp -dp "%{buildroot}%{_bindir}/kmk_gmake.exe" "%{buildroot}%{_bindir}/make.exe"

#------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------

rm -rf "%{buildroot}"

#------------------------------------------------------------------------------
%changelog

* Thu Jul 11 2013 Dmitriy Kuminov <coding@dmik.org> 0.1.9998.6-1
- New SVN release 2687 of version 0.1.9998.
- Add kbuild-make package containing vanilla GNU Make executable.

* Mon Nov 5 2012 Dmitriy Kuminov <coding/dmik.org> 0.1.9998.5-1
- New patch:
  - Add switching between RC/WRC in GCC3OMF/GXX3OMF tools based on
    EMXOMFLD_RC_* environment variables [Patch6].

* Mon Oct 16 2012 Dmitriy Kuminov <coding/dmik.org> 0.1.9998.4-1
- New SVN release 2663 of version 0.1.9998.

* Mon Oct 15 2012 Dmitriy Kuminov <coding/dmik.org> 0.1.9998.3-1
- New SVN release 2662 of version 0.1.9998.
- New patches:
  - Automatically create import library for DLL in GCC3OMF/GXX3OMF
    tools (may be disasbled with KMK_NOIMPLIB in LDFLAGS) [005.patch].

* Fri Feb 10 2012 Dmitriy Kuminov <coding/dmik.org> 0.1.9998.2-1
- New SVN release 2557 of version 0.1.9998.
- New patches:
  - Install DLLs to "bin/" by default [001.patch].
  - Make ld and ar in GCC3OMF/GXX3OMF tools output obey KBUILD_VERBOSE
    setting and be quiet by default [002.patch].
  - Support DLLs as sources for LIBRARIES targets for making import
    libraries with GCC3OMF/GXX3OMF tools [003.patch].
  - Add RC support to GCC3OMF/GXX3OMF tools [004.patch].

* Wed Oct 5 2011 Dmitriy Kuminov <coding/dmik.org> 0.1.9998.1-1
- New SVN release 2546 of version 0.1.9998.

