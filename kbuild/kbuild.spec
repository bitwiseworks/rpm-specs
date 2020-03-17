Name:       kbuild
Vendor:     netlabs.org
License:    BSD and GPLv2+
Url:        https://github.com/bitwiseworks/kbuild-os2

# Epoch is needed after dropping os2_release to keep proper updates.
Epoch:      1

Version:    0.1.9998
Release:    13%{?dist}

%scm_source github https://github.com/bitwiseworks/kbuild-os2 d197e375ed672dbe2c78f55313ffe0d826e7a484
#scm_source git file://D:/Coding/kbuild/master d197e375ed672dbe2c78f55313ffe0d826e7a484

%define descr_brief kBuild is a GNU Make fork with a set of scripts to simplify\
complex build tasks and portable versions of various UNIX tools to ensure\
cross-platform portability.

%define pkg_docdir      %{_docdir}/%{name}

BuildRequires: kbuild gettext-devel libcx-devel

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
%exclude %{_bindir}/*.dbg
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
%exclude %{_bindir}/*.dbg

%debug_package

#------------------------------------------------------------------------------
%prep
#------------------------------------------------------------------------------

%scm_setup

# Makefiles expect SVN info, generate it. Note that we shorten the commit hash
# to 7 digits and add 0x before to make it a valid C integer number.
echo \
"KBUILD_SVN_URL := %{__source_url}
KBUILD_SVN_REV := 0x%{lua: print(string.sub(rpm.expand('%{__source_rev}'), 1, 7))}
KBUILD_SVN_GIT := 1
" > SvnInfo.kmk

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
        BUILD_TYPE=release \
        LDFLAGS=-lintl \
        NIX_INSTALL_DIR=%{_prefix} \
        MY_INST_BIN=${MY_INST_BIN#/}/ \
        MY_INST_DATA=${MY_INST_DATA#/}/ \
        MY_INST_DOC=${MY_INST_DOC#/}/ \
        MY_INST_MODE=0644 \
        MY_INST_BIN_MODE=0755" \
    BUILD_PLATFORM=os2 \

%{kmk_env}

cmd /c "kBuild\envos2.cmd" kmk $KMK_FLAGS

#------------------------------------------------------------------------------
%install
#------------------------------------------------------------------------------

%{kmk_env}

%{__rm} -rf "%{buildroot}"

cmd /c "kBuild\envos2.cmd" kmk $KMK_FLAGS PATH_INS="%{buildroot}" install

# Additional docs (not installed by install)
%{__cp} -dp COPYING ChangeLog kBuild/doc/COPYING-FDL-1.3 "%{buildroot}%{pkg_docdir}/"

# To make GNU Make we simply copy kmk_gmake.exe, this should be enough
%{__cp} -dp "%{buildroot}%{_bindir}/kmk_gmake.exe" "%{buildroot}%{_bindir}/make.exe"

#------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------

%{__rm} -rf "%{buildroot}"

#------------------------------------------------------------------------------
%changelog
* Tue Mar 17 2020 Silvan Scherrer <silvan.scherrer@aroa.ch> 0.1.9998-13
- add a debug package to the rpm

* Sat Feb 2 2019 Dmitriy Kuminov <coding@dmik.org> 0.1.9998-12
- Fix kmk crash when processing some makefiles (e.g. LIBCx ones).
- Link kmk binaries against LIBCx to install EXCEPTQ handler.
- Print (significant) leading zeroes of git commit hash in version strings.

* Fri Jan 25 2019 Dmitriy Kuminov <coding@dmik.org> 0.1.9998-11
- Backlevel sources to SVN r3137 from vendor. This is the last revision prior
  to updating kmk to GNU make 4.2.1 sources that produce a plenty of errors on
  OS/2 (as shown by the previous RPM) and need a lot of porting to be usable.
- Print git commit hash in hex and with '-git' suffix in version strings
  instead of a misleading 'r' followed by a dec number (like SVN revision).

* Tue Nov 6 2018 Dmitriy Kuminov <coding@dmik.org> 0.1.9998-10
- Update sources to SVN r3236 from vendor.

* Wed Jul 26 2017 Dmitriy Kuminov <coding@dmik.org> 0.1.9998-9
- Use a forked GitHub repository where all previous patches have been applied.
- Drop changing the default DLL install dir from /lib to /bin (in an RPM
  Unix-like environment which is our primary target this is not needed).
- Update sources to SVN r3051 from vendor.
- Disable annoying wlink warning 1121 for GCC3OMF/GXX3OMF tools.
- Install qt-Q_OBJECT.sed needed by qt3 and qt4 units.
- Support SDL RPM install in LIBSDL sdk.
- Use abbveviated commit hash instead of SVN revision in kmk version strings.
- Add missing spaces after -i and -d in RC invocation for GCC3OMF/GXX3OMF tools.
- Add current directory to RC include path for GCC3OMF/GXX3OMF/OPENWATCOM tools.
- Fix failure to create an import library for a DLL in GXX3OMF tool.

* Thu Dec 17 2015 Dmitriy Kuminov <coding@dmik.org> 0.1.9998-8
- New SVN release 2803 of version 0.1.9998.
- Fix slashes in .rsp files for OpenWatcom (#125).
- Add major version suffix to Qt libs (#126).
- Fix unsetting env vars in kmk_redirect (#127).

* Wed Aug 05 2015 Dmitriy Kuminov <coding@dmik.org> 0.1.9998.7-1
- New SVN release 2786 of version 0.1.9998.
- Drop patches 2, 3 and 4 (applied upstream in r2774:2776).
- Disable patch 7 claimed to be not necessary (see ticket #109).
- Build with GCC 4 against LIBC 0.6.6 (patch 8, #124).

* Thu Jul 11 2013 Dmitriy Kuminov <coding@dmik.org> 0.1.9998.6-1
- New SVN release 2687 of version 0.1.9998.
- Add kbuild-make package containing vanilla GNU Make executable.

* Mon Nov 5 2012 Dmitriy Kuminov <coding/dmik.org> 0.1.9998.5-1
- New patch:
  - Add switching between RC/WRC in GCC3OMF/GXX3OMF tools based on
    EMXOMFLD_RC_* environment variables [Patch6].

* Tue Oct 16 2012 Dmitriy Kuminov <coding/dmik.org> 0.1.9998.4-1
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

