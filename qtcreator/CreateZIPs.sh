#!/bih/sh

#
# Qt Creator distribution ZIP archive creator.
#
# NOTE: This script requires the basic set of unix tools such as cp, mkdir,
# pwd, readlink, find etc.
#

#
# Defaults
#

out_dir_base="."

cp="cp -Rdp"

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

cp_files()
{
    local src_base="$1" # source directory base
    local out_base="$2" # output directory base
    local path="$3"     # file path relative to $src_base, may be glob
    local tgt_path="$4" # target path if differs from path, if ends with slash
                        # only the dir part of path is changed
                        # [optional]
    local exclude="$5"  # exclude pattern (relative to $src_base),
                        # case syntax [optional]
    local ext="$6"      # additional extension of $path base to copy (e.g. .sym)
                        # [optional]

    [ -z "$src_base" -o -z "$out_base" -o -z "$path" ] && \
        die "cp_files: invalid arguments."

    local path_dir="${path%/*}"
    [ "$path_dir" = "$path" ] && path_dir=.
    local path_file="${path##*/}"

    if [ -n "$tgt_path" ]; then
        local tgt_path_dir="${tgt_path%/*}"
        [ "$tgt_path_dir" = "$tgt_path" ] && path_dir=.
        local tgt_path_file="${tgt_path##*/}"
        [ -z "$tgt_path_file" ] && tgt_path_file="$path_file"
    else
        local tgt_path_dir="$path_dir"
        local tgt_path_file="$path_file"
    fi

    [ -d "$out_base/$tgt_path_dir" ] || run mkdir -p "$out_base/$tgt_path_dir"

    # if path_file is a mask, reset tgt_path_file (to cp to just tgt_path_dir)
    case "$path_file" in
        *"*"*|*"?"*) tgt_path_file=;;
    esac

    # simple case?
    if [ -z "$exclude" -a -z "$ext" ]; then
        run $cp "$src_base/$path" "$out_base/$tgt_path_dir/$tgt_path_file"
        return
    fi

    # complex case with exclude pattern or with additional extension
    for f in $src_base/$path; do
        [ -z "$exclude" ] || \
            eval "case ${f#$src_base/} in $exclude) continue;; esac"
        run $cp "$f" "$out_base/$tgt_path_dir/"
        [ -z "$ext" ] || run $cp "${f%.*}.$ext" "$out_base/$tgt_path_dir/"
    done
}

cp_files_inst_out() cp_files "$inst_base" "$out_base" "$1" "$2" "$3" "$4"

cp_exe_files_inst_out() cp_files "$inst_base" "$out_base" "$1" "$2" "$3" "sym"

split_out_sym()
{
    local out_base="$1"
    local out_base_sym="$2"

    [ -z "$out_base" -o -z "$out_base_sym" ] && \
        die "create_zips: invalid arguments."

    run mkdir -p "$out_base_sym/"

    for f in $(cd "$out_base" && find -type f -name "*.sym"); do
        local fd="${f%/*}"/
        [ "$fd" = "$f/" ] && fd=
        [ -d "$out_base_sym/$fd" ] || run mkdir -p "$out_base_sym/$fd"
        run mv "$out_base/$f" "$out_base_sym/$fd"
    done

    run $cp "$script_dir/INSTALL.OS2.debuginfo" "$out_base_sym/"
}

parse_version()
{
    local spec_file="$start_dir/qtcreator.spec"

    # get the version info from .spec
    ver_major=$(sed -nre \
        "s/^%define ver_major[[:space:]]+([0-9]+).*$/\1/p" < "$spec_file")
    ver_minor=$(sed -nre \
        "s/^%define ver_minor[[:space:]]+([0-9]+).*$/\1/p" < "$spec_file")
    ver_patch=$(sed -nre \
        "s/^%define ver_patch[[:space:]]+([0-9]+).*$/\1/p" < "$spec_file")
    os2_release=$(sed -nre \
        "s/^%define os2_release[[:space:]]+([0-9]+).*$/\1/p" < "$spec_file")
    rpm_release=$(sed -nre \
        "s/^%define rpm_release[[:space:]]+([0-9]+).*$/\1/p" < "$spec_file")

    [ -z "$ver_major" -o -z "$ver_minor" -o -z "$ver_patch" -o \
      -z "$os2_release" -o -z "$rpm_release" ] && \
        die "Could not determine version number in '$spec_file'."

    ver_full_spec="$ver_major.$ver_minor.$ver_patch"
    [ "$os2_release" != "0" ] && ver_full_spec="ver_full_spec.$os2_release"
    ver_full_spec="$ver_full_spec-$rpm_release"

    ver_full="$ver_full_spec"
    [ -n "$build_num" ] && ver_full="${ver_full}_${build_num}"
}

create_zips()
{
    [ -z "$start_dir" -o -z "$out_dir" -o \
      -z "$pkg_name" -o -z "$full_pkg_name" -o -z "$out_base" ] && \
        die "create_zips: invalid arguments."

    local out_base_sym="$out_dir/$full_pkg_name-debuginfo/$pkg_name-$ver_full"

    # .SYM files
    split_out_sym "$out_base" "$out_base_sym"

    local cwd=$(pwd)

    run cd "$out_base/.."
    run zip -SrX9 "$full_pkg_name-$ver_full.zip" "$pkg_name-$ver_full"
    run mv "$full_pkg_name-$ver_full.zip" "$out_dir/.."

    run cd "$out_base_sym/.."
    run zip -SrX9 "$full_pkg_name-debuginfo-$ver_full.zip" "$pkg_name-$ver_full"
    run mv "$full_pkg_name-debuginfo-$ver_full.zip" "$out_dir/.."

    run cd "$cwd"
}

cmd_create()
{
    local inst_base="$1"
    local build_num="$2"

    [ -d "$inst_base" ] || die "'$inst_base' is not a directory."
    [ -d "$out_dir_base" ] || die "'$out_dir_base' is not a directory."

    parse_version
    [ -z "$ver_full" ] && die "Version is not defined."

    echo "Spec version: $ver_full_spec"
    echo "Full version: $ver_full"

    local out_dir="$out_dir_base/tmp-zip-qt4-$ver_full"

    run rm -rf "$out_dir"

    #--------------------------------------------------------------------------
    # commons
    #--------------------------------------------------------------------------

    local pkg_name="qtcreator"

    local designer_dlls="QtDsg*.dll"
    local designer_plugin_dirs="designer"

    usr="@unixroot/usr"

    #--------------------------------------------------------------------------
    # main package
    #--------------------------------------------------------------------------

    local full_pkg_name="qtcreator"
    local out_base="$out_dir/$full_pkg_name/$pkg_name-$ver_full"

    # Readmes
    cp_files_inst_out "$usr/share/doc/qtcreator/LGPL_EXCEPTION.TXT" "./"
    cp_files_inst_out "$usr/share/doc/qtcreator/LICENSE.LGPL" "./"
    cp_files_inst_out "$usr/share/doc/qtcreator/README" "./"
    run $cp "$script_dir/INSTALL.OS2" "$out_base/"

    # Everything (see notes in .spec in the %install section)
    cp_exe_files_inst_out "$usr/lib/qtcreator/bin/*.exe" "bin/"
    cp_exe_files_inst_out "$usr/lib/qtcreator/bin/*.dll" "bin/"
    cp_exe_files_inst_out "$usr/lib/qtcreator/lib/qtcreator/plugins/Nokia/*.dll" "lib/qtcreator/plugins/Nokia/"
    cp_files_inst_out "$usr/lib/qtcreator/lib/qtcreator/plugins/Nokia/*" "lib/qtcreator/plugins/Nokia/" "*.dll"
    cp_files_inst_out "$usr/lib/qtcreator/share/" "./"

    create_zips

    run rm -rf "$out_dir"

    echo "ALL DONE."
}

#
# Main
#

script_path=$(readlink -e $0)
script_dir=${script_path%/*}
script_name=$(basename $0)

start_dir=$(pwd)

[ -z "$out_dir_base" ] && out_dir_base="."
out_dir_base=$(readlink -m "$out_dir_base")

# Parse arguments

cmd_help()
{
    echo \
"
Usage:
  $script_name all [options]    Create ZIPs.

Options:
  <instdir>     (*) Qt installation tree location
  <outdir>          Destination directory for ZIPs [$out_dir_base]
  <bldnum>          Build number [none]
"
}

case "$1" in
    all)
        if [ -n "$2" ]; then
            [ -n "$3" ] && out_dir_base=$(echo "$3" | tr '\\' '/')
            cmd_create $(echo "$2" | tr '\\' '/') "$4"
        else
            cmd_help
        fi;;
    -h|-?|--help|*) cmd_help;;
esac

# end of story

exit 0
