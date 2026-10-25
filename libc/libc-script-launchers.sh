#!/@unixroot/usr/bin/sh

# Manage LIBCn script launchers registered by RPM packages.

launcher="@SCRIPT_LAUNCHER@"
launcher_dir="@SCRIPT_LAUNCHER_DIR@"
stub_version="@SCRIPT_LAUNCHER_STUB_VERSION@"

usage()
{
  echo "Usage: ${0##*/} --update [--force] [PACKAGE]...
       ${0##*/} --install PACKAGE SCRIPT [SCRIPT]...
       ${0##*/} --remove PACKAGE" >&2
  exit 1
}

check_package()
{
  case "$1" in
    ''|.*|-*|*[!a-zA-Z0-9_+.-]*)
      echo "${0##*/}: Invalid package name: $1" >&2
      return 1 ;;
  esac
}

update_list()
{
  if [ ! -f "$1" ]; then
    echo "${0##*/}: No launcher registration: $1" >&2
    return 1
  fi
  list_failed=0
  while IFS= read -r script || [ -n "$script" ]; do
    [ -n "$script" ] || continue
    "$launcher" --force --install "$script" || list_failed=1
  done < "$1" || list_failed=1
  return "$list_failed"
}

[ "$#" -gt 0 ] || usage
command=$1
shift
case "$command" in
  --install)
    [ "$#" -ge 2 ] || usage
    check_package "$1" || exit 1
    package=$1
    shift
    mkdir -p "$launcher_dir" || exit 1
    launcher_list="$launcher_dir/$package"
    # Hidden temporary files are not registrations and are ignored by --update.
    list_tmp="$launcher_dir/.$package.tmp.$$"
    if printf '%s\n' "$@" > "$list_tmp" && mv -f "$list_tmp" "$launcher_list"; then
      "$launcher" --force --install "$@"
      exit $?
    fi
    rm -f "$list_tmp"
    exit 1 ;;
  --remove)
    [ "$#" -eq 1 ] || usage
    check_package "$1" || exit 1
    rm -f "$launcher_dir/$1"
    exit $? ;;
  --update)
    force=0
    if [ "$1" = "--force" ]; then
      force=1
      shift
    fi
    for package in "$@"; do
      check_package "$package" || exit 1
    done ;;
  *) usage ;;
esac

installed_stub_version=
if [ -f "$launcher_dir/.stub-version" ]; then
  installed_stub_version=$(cat "$launcher_dir/.stub-version") || installed_stub_version=
fi
if [ "$force" -eq 0 ] && [ "$installed_stub_version" = "$stub_version" ]; then
  exit 0
fi

launcher_failed=0
if [ "$#" -gt 0 ]; then
  for package in "$@"; do
    update_list "$launcher_dir/$package" || launcher_failed=1
  done
  # Updating a subset cannot certify that all launchers use the current stub.
  exit "$launcher_failed"
fi

for launcher_list in "$launcher_dir"/*; do
  [ -f "$launcher_list" ] || continue
  update_list "$launcher_list" || launcher_failed=1
done

# Keep the previous version on failure so the next invocation retries.
[ "$launcher_failed" -eq 0 ] || exit 1
mkdir -p "$launcher_dir" || exit 1
if printf '%s\n' "$stub_version" > "$launcher_dir/.stub-version.tmp.$$" &&
   mv -f "$launcher_dir/.stub-version.tmp.$$" "$launcher_dir/.stub-version"; then
  exit 0
fi
rm -f "$launcher_dir/.stub-version.tmp.$$"
exit 1
