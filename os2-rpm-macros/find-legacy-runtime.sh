#!/@unixroot/usr/bin/sh

#
# Helper script for %legacy_runtime_packages macro. This macro allows to
# automatically create legacy sub-packages with runtime components needed for
# compatibility with legacy applications.
#
# This script assumes the following drectory layout:
#
#   RPM_SOURCE_DIR/PACKAGE-legacy
#     ABI_X
#       ARCH_X
#         FILES
#       ARCH_X.list
#       ARCH_X.files.list
#       ARCH_X.dbugfiles.list
#       ARCH_Y
#         FILES
#       ARCH_Y.list
#       ARCH_Y.files.list
#       ARCH_Y.dbugfiles.list
#       ...
#     ABI_Y
#       ...
#     abi.list
#
# where PACKAGE is the main package name, ABI_* is the ABI version of the legacy
# runtime, ARCH_* is a target platform for which this runtime was compiled and
# FILES is a list of runtime components to install. ARCH_*.list is an index
# file that contains a line `TS|RPM|NAME|VER` where TS is the timestamp of the
# RPM file where FILES are extracted from, NAME is the name of the respective
# (sub-)package and VER is its full version. ARCH_*.files.list is a list of all
# FILES to include (one per line). ARCH_*.debugfiles.list is a list of
# respective debug info files. The abi.list file contains a space-separated list
# of all ABI_* values to create legacy packages for. If the PACKAGE's target
# platform matches one of ARCH_* values, then the respective set of files is
# placed to a sub-package called ABI_*, otherwise the first ARCH_* (in FS order)
# will be picked up.
#
# The %legacy_runtime_packages macro, when instantiated in a PACKAGE.spec file,
# will cause rpmbuild to automatically generate the given number of legacy
# sub-packages as described above. These sub-packages will have Priovides set
# to NAME = VER and Obsoletes to NAME <= VER so that they will be picked up
# by the dependency resolver for legacy applications that still depend on a
# NAME = VER package and also they will replace an existing installation of
# NAME = VER (this only makes sense for casese when NAME, i.e. the old runmtime
# package name, doesn't match the PACKAGE's main name and there are no
# explicit dependencies between them set with Requires).
#
# The above layout is nomrally created by the rpmbuild-bot.sh script (see
# http://trac.netlabs.org/rpm/browser/rpmbuild-bot) by pulling the respective
# components from older RPM files but may be also created by hand if needed.
#

COMMAND="$1"

die()
{
  (>&2 echo "$0: ERROR: $1")
  exit 1
}

if [ "$COMMAND" = "package" ] ; then
  RPM_PACKAGE_NAME="$2"
  RPM_SOURCE_DIR="$3"
  RPM_TARGET_CPU="$4"
  RPM_BUILD_ROOT="$5"
elif [ "$COMMAND" = "install" ] ; then
  RPM_TARGET_CPU="$2"
  RPM_BUILD_SUBDIR="$3"
else
  die "Command '$COMMAND' is invalid."
fi

[ -z "$RPM_PACKAGE_NAME" -o -z "$RPM_SOURCE_DIR"  -o -z "$RPM_TARGET_CPU" -o -z "$RPM_BUILD_ROOT" ] && \
  die "Invalid environment/arguments ($*)."

abi_base="$RPM_SOURCE_DIR/$RPM_PACKAGE_NAME-legacy"

read abi_list < "$abi_base/abi.list"
[ -n "$abi_list" ] || die "Legacy ABI versions are not found."

for abi in $abi_list ; do
  #locate the RPM list file for the given arch
  rpm_list="$abi_base/$abi/$RPM_TARGET_CPU.list"
  if [ ! -f "$rpm_list" ] ; then
    # try to use the first found arch when no exact match
    read -r arch <<EOF
`find "$abi_base/$abi" -mindepth 1 -maxdepth 1 -type d`
EOF
    [ -n "$arch" ] && rpm_list="$arch.list"
  fi
  # get properties (see rpmbuild-bot.sh)
  IFS='|' read ts rpm name ver < "$rpm_list"
  [ -z "$name" -o -z "$ver" ] && die "Name or version field is missing in $rpm_list."
  # get the file list
  filesdir="${rpm_list%.list}"
  fileslist="${rpm_list%.list}.files.list"
  [ -f "$fileslist" ] || die "File $fileslist not found."
  # process commands
  if [ "$COMMAND" = "package" ] ; then
    # Note: we have to store original Version and Release tag values in
    # %main_version and %main_release for later use since we redefine them
    # within %package and there is a bug in RPM that makes it permanent, see
    # https://www.redhat.com/archives/rpm-list/2000-October/msg00218.html)
    echo "

%global main_version %version
%global main_release %release

%package legacy-$abi

Version: ${ver%%-*}
Release: ${ver#*-}.L
Provides: $name = $ver.L
Obsoletes: $name <= $ver

Summary: Legacy runtime components (ABI version $abi).

%description legacy-$abi
This package contains runtime components for ABI version $abi.
It is provided for compatibility with legacy applications.

%files legacy-$abi
%defattr(-,root,root)
`cat "$fileslist"`

"
  else # install
    [ -z "$RPM_BUILD_SUBDIR" ] && die "RPM_BUILD_SUBDIR is not set."
    # Copy all listed files to RPM_BUILD_ROOT
    while read -r f ; do
      [ -f "$RPM_BUILD_ROOT$f" ] && die "File $RPM_BUILD_ROOT$f already exists."
      cp -p "$filesdir$f" "$RPM_BUILD_ROOT$f" || die "Copying $filesdir$f to $RPM_BUILD_ROOT$f failed."
    done < "$fileslist"
    # Now, if there are debug files, copy them too and append to debugfiles.list
    # (to be picked up by %debug_package magic in brp-strip.os2)
    dbgfilelist="${rpm_list%.list}.debugfiles.list"
    if [ -f "$dbgfilelist" ] ; then
      while read -r f ; do
        [ -f "$RPM_BUILD_ROOT$f" ] && die "File $RPM_BUILD_ROOT$f already exists."
        cp -p "$filesdir$f" "$RPM_BUILD_ROOT$f" || die "Copying $filesdir$f to $RPM_BUILD_ROOT$f failed."
      done < "$dbgfilelist"
      cat "$dbgfilelist" >> "$RPM_BUILD_SUBDIR/debugfiles.list"
    fi
  fi
done

exit 0
