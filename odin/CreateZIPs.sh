#!/bih/sh

#
# Odin distribution ZIP archive creator.
#
# Project Odin Software License can be found in LICENSE.TXT
#
# NOTE: This script requires the basic set of unix tools such as cp, mkdir,
# pwd, readlink, etc.
#

#
# Defaults
#

out_dir="tmp/zip"

#
# Functions
#

die() { echo "ERROR: $@"; cd "$start_dir"; exit 1; }

run()
{
    echo "$@"
    "$@" || die \
"Last command failed (exit status $?)."
}

cp_prg_file()
{
    # $1            file
    # $2            dest dir (relative to $out_base[_sym])
    # $out_base     dest base
    # $out_base_sym sym/map dest base

    [ -z "$1" -o -z "$2" -o -z "$out_base" -o -z "$out_base_sym" ] && \
        die "cp_prg_file: invalid arguments."

    local fbase=${1%.*}
    run cp -Rdp $1 "$out_base/$2"
    # don't copy .map, it's not in the right place of the build tree any more
#    run cp -Rdp $fbase.sym "$fbase.map" "$out_base_sym/$2"
    run cp -Rdp $fbase.sym "$out_base_sym/$2"

    # lxlite it in release mode
    if [ -z "$debug" ]; then
        lxlite /B- "$out_base/$2${1##*/}"
    fi
}

cmd_cleanup()
{
    [ -d "$out_dir" ] && \
        run rm -rf "$out_dir"
}

cmd_create()
{
    # $1 mode (nonzero - debug, else release)

    local name_base
    local name_base_sym
    local build_base

    local debug
    [ -n "$1" ] && debug="yes"

    if [ -z "$debug" ]; then
        name_base="odin-$ver_dots"
        name_base_sym="odin-$ver_dots-debuginfo"
        build_base="$odin_root-build/os2.x86/release"
    else
        name_base="odin-$ver_dots-debug"
        name_base_sym="odin-$ver_dots-debug-debuginfo"
        build_base="$odin_root-build/os2.x86/debug"
    fi

    local out_base="$out_dir/$name_base"
    local out_base_sym="$out_dir/$name_base_sym"

    cmd_cleanup

    # directories
    run mkdir -p "$out_base/system32/"
    run mkdir -p "$out_base_sym/system32/"

    # WGSS50
    run cp -Rdp "$odin_root/bin/wgss50.dll" "$out_base/system32/"
    run cp -Rdp "$odin_root/bin/wgss50.sym" "$out_base_sym/system32/"

    # DLLs
    cp_prg_file "$build_base/stage/bin/*.dll"           "system32/"

    # executables
    cp_prg_file "$build_base/stage/bin/odininst.exe"    "system32/"
    cp_prg_file "$build_base/stage/bin/pe.exe"          "system32/"
    cp_prg_file "$build_base/stage/bin//pec.exe"        "system32/"
    cp_prg_file "$build_base/stage/bin/regsvr32.exe"    "system32/"
    cp_prg_file "$build_base/stage/bin/xx2lx.exe"       "system32/"

    # Win32k
#    cp_prg_file "$build_base/win32k.sys"    "system32/"
#    run cp -Rdp "$build_base/win32k.ddp"    "$out_base/system32/"
#    cp_prg_file "$build_base/win32kCC.exe"  "system32/"
#    cp_prg_file "$build_base/kRx.exe"       "system32/"

    # docs
    run cp -Rdp \
        "$odin_root/ChangeLog" \
        "$odin_root/LICENSE.TXT" \
        "$odin_root/WGSS50.lic" \
        "$out_base/"
    run cp -Rdp \
        "$odin_root/doc/ChangeLog-"* \
        "$odin_root/doc/Readme.txt" \
        "$odin_root/doc/ReportingBugs.txt" \
        "$odin_root/doc/Logging.txt" \
        "$odin_root/doc/Odin.ini.txt" \
        "$odin_root/doc/odinuser.inf" \
        "$out_base/"

    # create ZIPs
    run cd "$out_dir"
    run zip -SrX9 "$name_base.zip" "$name_base"
    run mv "$name_base.zip" "$script_dir/"
    run zip -SrX9 "$name_base_sym.zip" "$name_base_sym"
    run mv "$name_base_sym.zip" "$script_dir/"
    run cd "$start_dir"

    cmd_cleanup

    echo "ALL DONE."
}

cmd_help()
{
    echo \
"
Usage:
  $0 <command> <odin_root>

<command> is one of:
  release   Create release ZIPs.
  debug     Create debug ZIPs.
  all       Do 'release' and 'debug' together.
  cleanup   Remove what is created by the above commands (except ZIPs).

<odin_root> is the full path to the Odin source tree. Note that the build
tree is expected to be found in the <odin_root>-build directory.
"
}

#
# Main
#

script_path=$(readlink -f $0)
script_dir=${script_path%/*}

start_dir=$(pwd)

# Get Odin version number

odin_root="$2"
[ -n "$2" ] || { cmd_help; exit 0; }

odinbuild_h="$odin_root/include/odinbuild.h"

[ -f "$odinbuild_h" ] || \
    die "Could not find file '$odinbuild_h'."

ver_major=$(sed -nre \
    "s/^#define ODIN32_VERSION_MAJOR[[:space:]]+([0-9]+).*$/\1/p" < "$odinbuild_h")
ver_minor=$(sed -nre \
    "s/^#define ODIN32_VERSION_MINOR[[:space:]]+([0-9]+).*$/\1/p" < "$odinbuild_h")
ver_build=$(sed -nre \
    "s/^#define ODIN32_BUILD_NR[[:space:]]+([0-9]+).*$/\1/p" < "$odinbuild_h")

[ -z "$ver_major" -o -z "$ver_minor" -o -z "$ver_build" ] && \
    die "Could not determine Odin version number in '$odinbuild_h.'"

ver_dots="$ver_major.$ver_minor.$ver_build"

# Parse arguments

case $1 in
    "--help" | "-?" | "-h" | "") cmd_help;;
    "cleanup") cmd_cleanup;;
    "release") cmd_create;;
    "debug") cmd_create "debug";;
    "all") cmd_create; cmd_create "debug";;
    *) cmd_help;;
esac

# end of story

exit 0

