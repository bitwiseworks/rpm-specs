#
# http://svn.netlabs.org/kbuild
#
# NOTES:
# 1. Requires GCC 3.3.5 CSD4 (ftp://ftp.netlabs.org/pub/gcc/GCC-3.3.5-csd4.zip)
# 2. Build with rpmbuild -ba -D "master_mode 1" when packing a new release
#    and changing %svn_rev / %svn_url.
# 3. Use -D "test_mode 1" to skip the unzip step when debugging the build.
#

Name:       kbuild
Vendor:     netlabs.org
License:    BSD and GPLv2+
Url:        http://svn.netlabs.org/kbuild

%define ver_major   0
%define ver_minor   1
%define ver_patch   9998

%define os2_release 1

%define rpm_release 1

%define svn_url     http://svn.netlabs.org/repos/kbuild/trunk
%define svn_rev     2546

%define descr_brief kBuild is a GNU make fork with a set of scripts to simplify\
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

#------------------------------------------------------------------------------
# commons
#------------------------------------------------------------------------------

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
%{_datadir}/*

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
%if 0%{?test_mode}
%setup -TD
%else
%setup -q
%endif
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
rm "%{buildroot}%{_bindir}/*.dll"

# Additional docs (not installed by install)
cp -dp COPYING ChangeLog kBuild/doc/COPYING-FDL-1.3 "%{buildroot}%{pkg_docdir}/"

#------------------------------------------------------------------------------
%clean
#------------------------------------------------------------------------------

rm -rf "%{buildroot}"

#------------------------------------------------------------------------------
%changelog

* Wed Oct 5 2011 Dmitriy Kuminov <dmik/coding.org> 0.1.9998-1
- New SVN release 2546 of version 0.1.9998.
