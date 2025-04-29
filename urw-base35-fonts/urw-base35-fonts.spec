#
# Important notes regarding the package:
# ======================================
# This package contains 35 fonts defined as PostScript Level 2 Core Font Set:
# > https://en.wikipedia.org/wiki/PostScript_fonts#Core_Font_Set
#
# This package is the replacement for previous 'urw-fonts' package (obsolete now).
#
# However, there are currently several issues that needed to be adressed:
# 1) This font set is owned by company (URW)++ [https://www.urwpp.de/en/], but
#    the company Artifex Software [http://www.artifex.com/] has negotiated with
#    (URW)++ the Open Source release of several fonts that (URW)++ owns, which
#    can be used as Level 2 Core Font Set.
#
#    Artifex Software is the owner/creator of Ghostscript software, and they use
#    those fonts as part of Ghostscript's resources.
#
#    However, (URW++) company does not provide any way to download those fonts.
#    So right now, we are using the fonts which Artifex Software company uses
#    in Ghostscript, and made available. They do not officially provide them,
#    but they have become the 'de facto' standard across Linux distributions.
#
#    Therefore, from now on, I will refer to Artifex Software as to 'upstream'.
#
# 2) Upstream has its own git repository for Core Font Set Level 2 sources:
#    > https://github.com/ArtifexSoftware/urw-base35-fonts
#
#    Here you can find 4 types of files (regarding the fonts):
#    *.t1  - https://en.wikipedia.org/wiki/PostScript_fonts#Type_1
#    *.afm - https://de.wikipedia.org/wiki/Adobe_Font_Metrics
#    *.ttf - https://en.wikipedia.org/wiki/TrueType
#    *.otf - https://en.wikipedia.org/wiki/OpenType
#
#    According to upstream, Ghostscript needs only Type 1 fonts to work properly.
#    It can use TTF or OTF fonts as substitutions as well in case the Type 1
#    fonts are missing, but the substitution is not (and can't be) guaranteed to
#    be absolutely flawless, unless the fonts use the CFF outlines:
#    > https://en.wikipedia.org/wiki/PostScript_fonts#Compact_Font_Format
#
#    And even though the OTF font files have CFF outlines embedded inside them,
#    those OTF fonts still cause problems when they are used with Ghostscript's
#    'pdfwrite' device as substitutions. This can break printing or conversions
#    for many users out there using Ghostscript. At the moment, upstream does
#    not have reason/motivation to fix the 'pdfwrite' device in the near future.
#
#    The AFM (Adobe Font Metrics) are useful for layout purposes of other
#    applications, and they contain general font information and font metrics.
#    These AFM files were distributed in the previous 'urw-fonts' package, so in
#    order to avoid possible regressions in the future, we need to continue
#    distributing them.
#
#    However, distributing AFM files would not be possible if we would create
#    this package from Ghostscript source package only. It does not contain
#    these AFM files, because as stated above - Ghostscript requires only T1
#    fonts. Therefore, we're using the archive with fonts provided from upstream.
#
#
# 3) The previous package 'urw-fonts' shipped the fonts in different format:
#    *.pfb - Printer Font Binary (compressed Type 1 fonts, which require an
#            8-bit transmission method)
#    *.pfm - Printer Font Metrics (same as *.afm files according to upstream)
#
#    These formats were basically replaced with T1 and AFM formats, currently
#    used by upstream.
#
# 4) (URW)++ does not have any sane versioning procedure. After reaching
#    version 1.10, they returned to version 1.00. That is the reason why
#    upstream switched to using git snapshot dates for versioning, and we
#    are sticking to that after discussion at fedora-devel mailing list.
#
# 5) The package scheme is this:
#
#    * urw-base35-fonts        -- Metapackage which does not contain anything,
#                                 but requires all its font subpackages. This
#                                 is a wrapper package to ease-up installation
#                                 of all fonts.
#
#    * urw-base35-fonts-common -- Package that contains only the license file,
#                                 to avoid duplication of it and to make the
#                                 font packages size smaller.
#
#    * urw-base35-[***]-fonts  -- Subpackage of base35 fonts, containing only
#                                 one font family, as required by FPG.
#
#    * urw-base35-fonts-devel  -- Devel subpackage that provides useful RPM
#                                 macro(s), so other packages can more easily
#                                 build against base35 fonts.
#
#    ==========================================================================
#
#    urw-base35-fonts ----- urw-base35-fonts-common
#                       |             |
#                       |             |
#                       \-- urw-base35-[***]-fonts
#
#    ==========================================================================
#
#    NOTE: Fedora Packaging Guidelines (FPG) requires to use OTF or TTF format:
#          https://fedoraproject.org/wiki/Choosing_the_right_font_format_to_package
#
#          However, there are several packages in Fedora that still hadn't been
#          updated to work with OTF/TTF formats, and thus still require the
#          Type1 font format to work correctly. These packages include e.g.:
#           * ghostscript
#           * ImageMagick
#           * hylafax+
#
#          On the other hand, more and more software (e.g. LibreOffice) is
#          moving away from Type1 format completely and dropping its support.
#
#          As a result, we currently need to ship both OTF and Type1/AFM formats.
#          In case all the packages depending on base35 fonts will finally start
#          supporting the OTF, then we will make complete switch to OTF only.
#
#    ==========================================================================

# GLOBAL MACROS:
# --------------
%global fontname            urw-base35
%global fontconfig_prio     61
%global urw_fonts_vers      3:2.4-25
%global tmpdir              %{_localstatedir}/lib/rpm-state/urw-base35-fonts
%global tmpfile             %{tmpdir}/cache-update-needed
%global legacydir           %{_datadir}/X11/fonts/urw-fonts


# By redefining the '_docdir_fmt' macro we override the default location of
# documentation or license files. Instead of them being located in
# 'urw-base35-fonts-common', they are located in 'urw-base35-fonts' folder.
%global _docdir_fmt         %{name}


# This will create an auxiliary file if it does not exist, to indicate that X11
# Logical Font Description database and fontconfig cache needs to be updated.
%global post_scriptlet()    \
(                           \
  if ! [[ -x %{tmpfile} ]]; then \
    rm -rf   %{tmpdir}      \
    mkdir -p %{tmpdir}      \
                            \
    touch    %{tmpfile}     \
    chmod +x %{tmpfile}     \
  fi                        \
)

# NOTE: At the moment, there's no equivalent of 'posttrans' macro for
#       uninstallation, meaning we can only use the 'posttrans'.
#
#       Because of it , we have to use 'postun' instead. That means this
#       scriptlet will be called for every font family subpackage being
#       uninstalled...
%global postun_scriptlet()  \
(                           \
  if [[ $1 -eq 0 ]]; then   \
    # mkfontscale %{_fontdir} &> /dev/null || : \
    # mkfontdir   %{_fontdir} &> /dev/null || : \
    true || :               \
  fi                        \
)


# The content of this scriptlet is only run once during install/update.
%global posttrans_scriptlet() \
(                             \
  if [[ -x %{tmpfile} ]]; then \
    # mkfontscale %{_fontdir}   \
    # mkfontdir   %{_fontdir}   \
    #                          \
    true || :                 \
    rm -rf %{tmpdir}          \
  fi                          \
)


%global common_desc \
The Level 2 Core Font Set is a PostScript specification of 35 base fonts that \
can be used with any PostScript file. These fonts are provided freely \
by (URW)++ company, and are mainly utilized by applications using Ghostscript.

# =============================================================================

Name:             %{fontname}-fonts
Summary:          Core Font Set containing 35 freely distributable fonts from (URW)++
Version:          20200910
Release:          1%{?dist}

# NOTE: (URW)++ holds the copyright, but Artifex Software has obtained rights to
#       release these fonts under GNU Affero General Public License (version 3).
#       Also contains subpackage legacy with older version of the fonts (with GPLv2.0+ license) still needed by a few applications.
License:          AGPLv3 and GPLv2+

URL:              https://www.urwpp.de/en/
%if !0%{?os2_version}
Source:           https://github.com/ArtifexSoftware/urw-base35-fonts/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
Source1:          urw-fonts-1.0.7pre44.tar.bz2
%else
#Source:           urw-base35-fonts-github-master-os2.zip
%scm_source       github https://github.com/bitwiseworks/urw-base35-fonts-os2 master-os2
%endif

BuildArch:        noarch

%if !0%{?os2_version}
Patch01:          urw-base35-fonts-20200910-dont-config-d050000l-as-fantasy-font.patch
%endif

BuildRequires:    fontpackages-devel
%if !0%{?os2_version}
BuildRequires:    libappstream-glib
%endif

BuildRequires:    git
BuildRequires:    sed

# ---------------

Provides:         urw-fonts = %{urw_fonts_vers}
Obsoletes:        urw-fonts < %{urw_fonts_vers}

# This is metapackage for installation all font subpackages, require them:
Requires:         %{name}-common = %{version}-%{release}
Requires:         %{fontname}-bookman-fonts
Requires:         %{fontname}-c059-fonts
Requires:         %{fontname}-d050000l-fonts
Requires:         %{fontname}-gothic-fonts
Requires:         %{fontname}-nimbus-mono-ps-fonts
Requires:         %{fontname}-nimbus-roman-fonts
Requires:         %{fontname}-nimbus-sans-fonts
Requires:         %{fontname}-p052-fonts
Requires:         %{fontname}-standard-symbols-ps-fonts
Requires:         %{fontname}-z003-fonts

# Upstream patches -- official upstream patches released by upstream since the
# ----------------    last rebase that are necessary for any reason:

%description
%{common_desc}

This meta-package will install all the 35 fonts from the %{name}.

# =============================================================================

# Macro for creating a subpackage for a given font family.
#
# USAGE: font_subpkg [-c] [-o old_subpackage_name]
#  -c    Make this subpackage conflict with the previous versions of URW fonts.
#  -o    Marks this supbackage to obsolete (& provide) other previous subpackage.
%define fontfamily_subpkg(coa:)\
                                                                               \
%define ff_filename   %(echo %{*} | tr --delete " ")                           \
%define subpkg_name   %(echo %{*} | tr "A-Z " "a-z-" | sed -e 's/urw-//')      \
                                                                               \
%package -n       %{fontname}-%{subpkg_name}-fonts                             \
Summary:          %{*} font family [part of Level 2 Core Font Set]             \
Requires:         %{name}-common = %{version}-%{release}                       \
                                                                               \
Requires(post):   fontconfig                                                   \
Requires(postun): fontconfig                                                   \
                                                                               \
                                                                               \
# The section below will be only added if the '-c' option was specified:       \
%{-c:                                                                          \
Conflicts:        urw-fonts < %{urw_fonts_vers} }                              \
                                                                               \
%description -n   %{fontname}-%{subpkg_name}-fonts                             \
This package contains %{*} font family,                                        \
which is part of Level 2 Core Font Set.                                        \
                                                                               \
%{common_desc}                                                                 \
                                                                               \
%post -n %{fontname}-%{subpkg_name}-fonts                                      \
%{post_scriptlet}                                                              \
                                                                               \
%postun -n %{fontname}-%{subpkg_name}-fonts                                    \
%{postun_scriptlet}                                                            \
                                                                               \
%posttrans -n %{fontname}-%{subpkg_name}-fonts                                 \
%{posttrans_scriptlet}                                                         \
                                                                               \
%files -n %{fontname}-%{subpkg_name}-fonts                                     \
%{_fontdir}/%{ff_filename}*.t1                                                 \
%{_fontdir}/%{ff_filename}*.afm                                                \
%{_fontdir}/%{ff_filename}*.otf                                                \
%{_datadir}/appdata/de.urwpp.%{ff_filename}.metainfo.xml                       \
%{_datadir}/fontconfig/conf.avail/%{fontconfig_prio}-urw-%{subpkg_name}.conf   \
%{_sysconfdir}/fonts/conf.d/%{fontconfig_prio}-urw-%{subpkg_name}.conf         \
# Temporary workaround for https://bugzilla.redhat.com/show_bug.cgi?id=1534206:\
%exclude %{_fontdir}/StandardSymbolsPS.otf                                     \

# =============================================================================

%package common
Summary:          Common files of the (URW)++ Level 2 Core Font Set
%if !0%{?os2_version}
Requires:         filesystem
%endif
Requires:         fontpackages-filesystem

%description common
%{common_desc}

This package contains the necessary license files for this font set.

# ---------------

%package devel
Summary:          RPM macros related to (URW)++ Level 2 Core Font Set
Requires:         %{name} = %{version}-%{release}

%description devel
%{common_desc}

This package is useful for development purposes only. It installs RPM
macros useful for building packages against %{name},
as well as all the fonts contained in this font set.

# ---------------

%package legacy
Summary:          Legacy version of (URW)++ Level 2 Core Font Set
%if !0%{?os2_version}
Requires(post):   mkfontscale mkfontdir
Requires(postun): mkfontscale mkfontdir
%endif

%description legacy
%{common_desc}

This package provides previous (legacy) versions of these fonts, which are still
required by some of the software, like e.g. xfig, X11, etc.

# =============================================================================
# NOTE: When making an update, make sure to check if any font families were
#       added/removed. We always need to pack all the fonts into subpackages.
# =============================================================================
%fontfamily_subpkg C059
%fontfamily_subpkg D050000L
%fontfamily_subpkg Nimbus Mono PS -a -c
%fontfamily_subpkg Nimbus Roman -a -c
%fontfamily_subpkg Nimbus Sans -a -c
%fontfamily_subpkg P052
%fontfamily_subpkg Standard Symbols PS -a -c
%fontfamily_subpkg URW Bookman -a -c
%fontfamily_subpkg URW Gothic -a -c
%fontfamily_subpkg Z003
# =============================================================================

# We need to ship the legacy fonts for now as well (BZ #1551219):
%prep
%if !0%{?os2_version}
%autosetup -N -S git
%else
%scm_setup
%endif

mkdir -p legacy
%if !0%{?os2_version}
tar --directory=legacy/ -xf %{SOURCE1}
rm -f legacy/ChangeLog legacy/README* legacy/fonts*

# Amend all the files to the initial commit, and patch the sources:
git add --all --force
git commit --all --amend --no-edit > /dev/null
%autopatch -p1
%endif

%install
install -m 0755 -d %{buildroot}%{_fontdir}
install -m 0755 -d %{buildroot}%{_datadir}/appdata
install -m 0755 -d %{buildroot}%{_datadir}/fontconfig/conf.avail
install -m 0755 -d %{buildroot}%{_sysconfdir}/fonts/conf.d
install -m 0755 -d %{buildroot}%{legacydir}
install -m 0755 -d %{buildroot}%{_datadir}/licenses/urw-fonts

install -m 0644 -p fonts/*.t1  %{buildroot}%{_fontdir}
install -m 0644 -p fonts/*.afm %{buildroot}%{_fontdir}
install -m 0644 -p fonts/*.otf %{buildroot}%{_fontdir}
%if !0%{?os2_version}
install -m 0644 -p legacy/*.afm legacy/*.pfm legacy/*.pfb %{buildroot}%{legacydir}
install -m 0644 -p legacy/COPYING %{buildroot}%{_datadir}/licenses/urw-fonts
%endif

install -m 0644 -p appstream/*.metainfo.xml %{buildroot}%{_datadir}/appdata/

# Install the fontconfig files with correct priority for our distribution:
for file in fontconfig/*.conf; do
  DISTRO_FILENAME="%{fontconfig_prio}-$(basename $file)"
  install -m 0644 -p $file %{buildroot}%{_datadir}/fontconfig/conf.avail/$DISTRO_FILENAME
  ln -sf %{_datadir}/fontconfig/conf.avail/$DISTRO_FILENAME %{buildroot}%{_sysconfdir}/fonts/conf.d/$DISTRO_FILENAME
done

# Some of the fontconfig files are not to be shipped:
#  * urw-fallback-specifics.conf - these mappings are already provided by fontconfig
#  * urw-fallback-generics.conf - no use-cases for this as far as we know
%if !0%{?os2_version}
rm -f %{buildroot}%{_datadir}/fontconfig/conf.avail/%{fontconfig_prio}-urw-fallback-{specifics,generics}.conf
rm -f %{buildroot}%{_sysconfdir}/fonts/conf.d/%{fontconfig_prio}-urw-fallback-{specifics,generics}.conf
%else
rm -f %{buildroot}%{_datadir}/fontconfig/conf.avail/%{fontconfig_prio}-urw-fallback-specifics.conf
rm -f %{buildroot}%{_sysconfdir}/fonts/conf.d/%{fontconfig_prio}-urw-fallback-specifics.conf
rm -f %{buildroot}%{_datadir}/fontconfig/conf.avail/%{fontconfig_prio}-urw-fallback-generics.conf
rm -f %{buildroot}%{_sysconfdir}/fonts/conf.d/%{fontconfig_prio}-urw-fallback-generics.conf
%endif

# We need to touch these files -- otherwise running 'rpm --setperms' would
# result in these files having incorrect permissions like this: [-------.]
#touch %{buildroot}%{_fontdir}/fonts.dir
#touch %{buildroot}%{_fontdir}/fonts.scale
touch %{buildroot}%{legacydir}/fonts.dir
touch %{buildroot}%{legacydir}/fonts.scale

# Install the symlink for the X11 Logical Font Description to actually work:
install -m 0755 -d %{buildroot}%{_sysconfdir}/X11/fontpath.d
#ln -sf %{_fontdir} %{buildroot}%{_sysconfdir}/X11/fontpath.d/%{name}
ln -sf %{legacydir} %{buildroot}%{_sysconfdir}/X11/fontpath.d/urw-fonts

# Generate the macro containing the path to our fonts:
install -m 0755 -d %{buildroot}%{_rpmconfigdir}/macros.d

cat > %{buildroot}%{_rpmconfigdir}/macros.d/macros.%{name} << _EOF
%%urw_base35_fontpath    %{_fontdir}
_EOF

# Check that the AppStream files are valid and safe. Otherwise they might not
# get used in Gnome Software...
%check
%if !0%{?os2_version}
appstream-util validate-relax --nonet %{buildroot}%{_datadir}/appdata/*.metainfo.xml
%endif

%post legacy
%if !0%{?os2_version}
mkfontscale %{legacydir}
mkfontdir   %{legacydir}
%endif

%postun legacy
%if !0%{?os2_version}
mkfontscale %{legacydir}
mkfontdir   %{legacydir}
%endif

# NOTE: There's no reason to run 'post' and 'postun' scriptlets for the main
#       metapackage or the *-common subpackage. Everything necessary is handled
#       by any of the actual font family subpackages.

# =============================================================================

%files
%{_datadir}/appdata/de.urwpp.URWCoreFontSetLevel2.metainfo.xml

# ---------------

%files common
%license LICENSE COPYING

%dir %{_fontdir}
#%ghost %verify (not md5 size mtime) %{_fontdir}/fonts.dir
#%ghost %verify (not md5 size mtime) %{_fontdir}/fonts.scale

%{_datadir}/fontconfig/conf.avail/%{fontconfig_prio}-urw-fallback-backwards.conf
%{_sysconfdir}/fonts/conf.d/%{fontconfig_prio}-urw-fallback-backwards.conf
#%%{_sysconfdir}/X11/fontpath.d/%%{name}

# ---------------

%files devel
%{_rpmconfigdir}/macros.d/macros.%{name}

# ---------------

%files legacy
%if !0%{?os2_version}
%license %{_datadir}/licenses/urw-fonts/COPYING
%endif
%ghost %verify (not md5 size mtime) %{legacydir}/fonts.dir
%ghost %verify (not md5 size mtime) %{legacydir}/fonts.scale
%{_sysconfdir}/X11/fontpath.d/urw-fonts
%if !0%{?os2_version}
%{legacydir}/*.afm
%{legacydir}/*.pfm
%{legacydir}/*.pfb
%endif

# =============================================================================

%changelog
* Mon Apr 25 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> - 20200910-1
- first os/2 version
