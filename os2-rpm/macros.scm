#------------------------------------------------------------------------------
# Macros to automatically take sources from SCM rather than from archives

%__scm_pre_pack\
[ -f RPMBUILD_SOURCE ] && mv RPMBUILD_SOURCE RPMBUILD_SOURCE.orig\
echo "SCM: %{__source_scm}\
URL: %{__source_url}\
Rev: %{?__source_rev}" >RPMBUILD_SOURCE\
%{nil}

# SVN

%__scm_source_svn\
Source: %{?main_name}%{!?main_name:%{name}}-svn%{?__source_rev:-r%{__source_rev}}.zip\
BuildRequires: subversion zip\
%{nil}

%__scm_setup_svn\
%if %{?__source_rev:%(if test -f "%SOURCE0" ; then echo 1 ; else echo 0 ; fi)}%{!?__source_rev:0}\
%setup -q\
%else\
%setup -n "%__source_dir" -Tc\
svn export %{?__source_rev:-r %{__source_rev}} %{__source_url} . --force\
%__scm_pre_pack\
%if %{defined __source_rev}\
(rm -f "%SOURCE0" && cd .. && zip %{-A:%{-A*}}%{!-A:-rX9} "%SOURCE0" "%__source_dir")\
%endif\
%endif\
%{nil}

# Git

%__scm_source_git\
Source: %{?main_name}%{!?main_name:%{name}}-git%{?__source_rev:-%{__source_rev}}.zip\
BuildRequires: git zip unzip\
%{nil}

%__scm_setup_git\
%if %{?__source_rev:%(if test -f "%SOURCE0" ; then echo 1 ; else echo 0 ; fi)}%{!?__source_rev:0}\
%setup -q\
%else\
%setup -n "%__source_dir" -Tc\
rm -f "%SOURCE0"\
git archive --format zip --output "%SOURCE0" --prefix "%__source_dir/" --remote "%{__source_url}" "%{?__source_rev}"\
unzip -qq "%SOURCE0" "%__source_dir"/RPMBUILD_SOURCE -d .. 2>/dev/null || :\
%__scm_pre_pack\
(cd .. && zip -mX "%SOURCE0" "%__source_dir"/RPMBUILD_SOURCE*)\
unzip -qq "%SOURCE0" -d ..\
%if %{undefined __source_rev}\
rm -f "%SOURCE0"\
%endif\
%endif

# GitHub

%__scm_source_github\
Source: %{?main_name}%{!?main_name:%{name}}-github%{?__source_rev:-%{__source_rev}}.zip\
BuildRequires: wget zip unzip\
%{nil}

%__scm_setup_github\
%{!?__source_rev:%{error:%0: Revision in %%scm_source is required for GitHub}exit 1}\
%global __source_url_github_name %(URL="%{__source_url}" ; echo ${URL##*/})\
%global __source_dir_github %{__source_url_github_name}-%{__source_rev}\
%if %{?__source_rev:%(if test -f "%SOURCE0" ; then echo 1 ; else echo 0 ; fi)}%{!?__source_rev:0}\
%setup -n "%__source_dir_github" -q\
%else\
%setup -n "%__source_dir_github" -Tc\
rm -f "%SOURCE0"\
wget -nv "%{__source_url}/archive/%{__source_rev}.zip" -O "%SOURCE0"\
unzip -qq "%SOURCE0" "%__source_dir_github"/RPMBUILD_SOURCE -d .. 2>/dev/null || :\
%__scm_pre_pack\
(cd .. && zip -mX "%SOURCE0" "%__source_dir_github"/RPMBUILD_SOURCE*)\
unzip -qq "%SOURCE0" -d ..\
%endif

# User-level macros

%scm_source()\
%{?SOURCE0:%{error:%0: Source tag is already set to '%SOURCE0'}%{quit}}\
%{?1:%global __source_scm %1}\
%{?2:%global __source_url %2}\
%{?3:%global __source_rev %3}\
%{expand:%%{!?__scm_source_%1:%%{error:%0: Invalid SCM type: %{?1}}%{quit}}}\
%{expand:%%{?__scm_source_%1}}\
%{nil}

%scm_setup(A:)\
%{!?__source_scm:%{error:%0: Missing %%scm_source specification}exit 1}\
%{!?__source_url:%{?__source_scm:%{error:%0: Missing URL in %%scm_source}exit 1}}\
%global __source_dir %{?main_name}%{!?main_name:%{name}}-%{?main_version}%{!?main_version:%{version}}\
%{expand:%%{?__scm_setup_%{__source_scm}}}\
%{nil}
