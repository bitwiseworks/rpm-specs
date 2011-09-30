#!/bih/sh

#
# Qt Creator distribution RPM archive creator.
#
# NOTE: This script requires the basic set of unix tools such as cp, mkdir,
# pwd, readlink, find etc.
#

#
# Defaults
#

spec_file=qtcreator.spec

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

cmd_all()
{
    run $env_cmd rpmbuild \
        -D "master_mode 1" \
        -D "create_zips_script $start_dir/CreateZIPs.sh" \
        -ba $spec_file
}

cmd_build()
{
    local src_base="$1"
    local src_base_arg=
    [ -n "$src_base" ] && src_base_arg=-D "SOURCE_TREE $src_base"

    run $env_cmd rpmbuild $src_base_arg \
        -D "master_mode 1" \
        -D "skip_prep_export 1" -D "skip_prep_clean 1" -D "skip_clean 1" \
        --short-circuit -bc $spec_file
}

cmd_install()
{
    local src_base="$1"
    local src_base_arg=
    [ -n "$src_base" ] && src_base_arg=-D "SOURCE_TREE $src_base"

    run $env_cmd rpmbuild $src_base_arg \
        -D "master_mode 1" \
        -D "skip_prep_export 1" -D "skip_prep_clean 1" -D "skip_clean 1" \
        --short-circuit -bi $spec_file
}

cmd_rpm()
{
    run $env_cmd rpmbuild \
        -D "master_mode 1" \
        -D "skip_prep_export 1" -D "skip_prep_clean 1" -D "skip_clean 1" \
        -D "skip_build 1" -D "skip_install 1" \
        --short-circuit -bb $spec_file
}

#
# Main
#

script_path=$(readlink -e $0)
script_dir=${script_path%/*}
script_name=$(basename $0)

start_dir=$(pwd)

[ -f "$start_dir/env.sh" ] && . "$start_dir/env.sh"

env_cmd=
[ -f "$start_dir/env.cmd" ] && env_cmd="cmd /c env.cmd"

# Parse arguments

cmd_help()
{
    echo \
"
Usage:
  $script_name all                Do everything (RPM, SRPM, ZIP)
  $script_name build [<srcdir>]   Build product (in BUILD/<product>)
  $script_name install [<srcdir>] Install product (to BUILDROOT/<product>)
  $script_name rpm                Build RPMs only

Options:
  <srcdir>      Source tree location (default is BUILD/<product>)
"
}

case "$1" in
    build|install)
        if [ -n "$2" ]; then
            [ -d "$2" ] || die "'$2' is not a directory."
        fi
        cmd_$1 $(echo "$2" | tr '\\' '/');;
    all|rpm) cmd_$1;;
    -h|-?|--help|*) cmd_help;;
esac

# end of story

exit 0
