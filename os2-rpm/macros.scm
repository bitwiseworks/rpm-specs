#------------------------------------------------------------------------------
# Macros to automatically take sources from SCM rather than from archives

%__scm_info_file .rpmbuild-info

# SVN

%__scm_source_svn\
BuildRequires: subversion gawk\
%{nil}

%__scm_setup_rev_id_svn\
__source_rev_id=$(LC_ALL=C svn info %{?__source_rev:-r '%{__source_rev}'} '%{__source_url}' |\
gawk -F': ' '/^Revision: / { have_rev_id=1; print $2; exit }\
END { if (!have_rev_id) exit 1 }')\
%{__cat} >> %{__scm_info_file}.new <<EOF\
RevID: $__source_rev_id\
EOF\
%{nil}

%__scm_setup_svn\
if test -f '%SOURCE0' ; then\
  unzip -oqq '%SOURCE0'\
else\
  svn export -r "$__source_rev_id" '%{__source_url}' source --force\
  zip %{-A:%{-A*}}%{!-A:-rX9} '%SOURCE0' source\
fi\
%{nil}

# Git

%__scm_source_git\
BuildRequires: git\
%{nil}

%__scm_setup_rev_id_git\
%global __source_url_git_path %{lua:
  local url = rpm.expand("%{__source_url}")
  local path, count = url:gsub("^file://", "")
  print((count == 1 or url:match("^[A-Za-z]:")) and path or "")
}\
%if "%{__source_url_git_path}" != ""\
__source_rev_id=$(git -C '%{__source_url_git_path}' rev-parse --verify '%{?__source_rev}%{!?__source_rev:HEAD}^{commit}')\
%else\
__source_rev_id=$(git ls-remote --exit-code '%{__source_url}' '%{?__source_rev}%{!?__source_rev:HEAD}')\
__source_rev_id="${__source_rev_id%%%%[[:space:]]*}"\
%endif\
%{__cat} >> %{__scm_info_file}.new <<EOF\
RevID: $__source_rev_id\
EOF\
%{nil}

%__scm_setup_git\
if ! test -f '%SOURCE0' ; then\
%if "%{__source_url_git_path}" != ""\
git -C '%{__source_url_git_path}' archive --format zip --output '%SOURCE0' --prefix source/ "$__source_rev_id"\
%else\
git archive --format zip --output '%SOURCE0' --prefix source/ --remote '%{__source_url}' '%{?__source_rev}%{!?__source_rev:HEAD}'\
test "$__source_rev_id" = "$(unzip -zq '%SOURCE0')"\
%endif\
fi\
unzip -oqq '%SOURCE0'\
%{nil}

# GitHub

%__scm_source_github\
%{!?__source_rev:%{error:%0: Revision in %%scm_source is required for GitHub}%{quit}}\
BuildRequires: curl gawk\
%{nil}

%__scm_setup_rev_id_github\
%global __source_url_github_api %{lua:
  local func = rpm.expand("%0")
  local url = rpm.expand("%{__source_url}")
  local count
  url, count = url:gsub("^https?://github.com/", "https://api.github.com/repos/")
  assert(count == 1, func .. ": GitHub URL must start with http[s]://github.com/")
  print(url)
}\
__source_rev_id=$(curl -K - -fsSL '%{__source_url_github_api}/commits/%{__source_rev}' <<'EOF' |\
%{?github_user:user = "%{github_user}:%{?github_password:%{github_password}}"}\
%{?github_token:header = "Authorization: token %{github_token}"}\
EOF\
gawk -F'"' '/^[[:space:]]*"sha":/ { have_commit_sha=1; print $4; exit }\
END { if (!have_commit_sha) exit 1 }')\
%{__cat} >> %{__scm_info_file}.new <<EOF\
RevID: $__source_rev_id\
EOF\
%{nil}

%__scm_setup_github\
if ! test -f '%SOURCE0' ; then\
  curl -K - -fsSL '%{__source_url}/archive/'"${__source_rev_id}.zip" -o '%SOURCE0' <<'EOF'\
%{?github_user:user = "%{github_user}:%{?github_password:%{github_password}}"}\
%{?github_token:header = "Authorization: token %{github_token}"}\
write-out = "curl: Downloaded \%{size_download} B / \%{time_total} s [\%{response_code}]"\
EOF\
fi\
unzip -oqq '%SOURCE0'\
%{nil}

# User-level macros

# Sets parameters for scm_setup macro, arguments: SCM URL [REV]
# SCM - SCM type (svn, git, github)
# URL - Repository URL
# REV - Revision/reference/commit (may be empty for local SVN/Git URLs)
# NOTE: the __scm_defined was needed for noarch only spec
%scm_source()\
%{!?__scm_defined:\
%global __scm_defined 1\
%{?SOURCE0:%{error:%0: Source tag is already set to '%SOURCE0'}%{quit}}\
%{?1:%global __source_scm %1}\
%{?2:%global __source_url %2}\
%{?3:%global __source_rev %3}\
%{!?__source_url:%{error:%0: Missing URL}%{quit}}\
%{expand:%%{!?__scm_source_%1:%%{error:%0: Invalid SCM type: '%{?1}'}%{quit}}}\
%{expand:%%{!?__scm_setup_%1:%%{error:%0: Missing %%__scm_setup_%1 macro}%{quit}}}\
%{expand:%%{!?__scm_setup_rev_id_%1:%%{error:%0: Missing %%__scm_setup_rev_id_%1 macro}%{quit}}}\
BuildRequires: zip unzip\
%global __source_dir %{name}\
Source: %{__source_dir}.zip\
%{expand:%%{__scm_source_%1}}\
}\
%{nil}

# Performs source setup via SCM using scm_setup values, arguments: [-A OPTS]
# OPTS - Options for zip (-rx9 by default, currently used only for SVN SCM type)
%scm_setup(A:)\
%{!?__scm_defined:%{error:%0: Missing %%scm_source specification}%{quit}}\
%setup -n "%{__source_dir}" -Tc\
%{__cat} > %{__scm_info_file}.new <<'EOF'\
SCM: %{__source_scm}\
URL: %{__source_url}\
EOF\
%{expand:%%{__scm_setup_rev_id_%{__source_scm}}}\
if test -f '%SOURCE0' ; then\
  unzip -oqq '%SOURCE0' %{__scm_info_file} 2>/dev/null || :\
  if test -f %{__scm_info_file} &&\
    test "$(%{__cat} %{__scm_info_file})" = "$(%{__cat} %{__scm_info_file}.new)" ; then\
    %{__rm} %{__scm_info_file}.new\
  else\
    %{__rm} -rf '%SOURCE0'\
  fi\
fi\
%{expand:%%{__scm_setup_%{__source_scm}}}\
if test -f %{__scm_info_file}.new ; then\
  test -f %{__scm_info_file} || %{__cat} %{__scm_info_file}.new\
  %{__mv} %{__scm_info_file}.new %{__scm_info_file}\
  zip -X '%SOURCE0' %{__scm_info_file}\
fi\
set -- */\
test $# -eq 1 && test -d "$1"\
test "$1" = source/ || %{__mv} "$1" source\
%setup -n "%{__source_dir}/source" -DT\
%{nil}
