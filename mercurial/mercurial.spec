%{!?python_sitearch: %define python_sitearch %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib(1)")}

Summary: A fast, lightweight distributed source control management system 
Name: mercurial
Version: 2.5.2
Release: 1%{?dist}
License: GPLv2+
Group: Development/Tools
URL: http://www.selenic.com/mercurial/
Source0: http://www.selenic.com/mercurial/release/%{name}-%{version}.tar.gz
Source1: python-wrapper.zip

Patch0: mercurial-os2.diff

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: python python-devel
#BuildRequires: emacs emacs-el pkgconfig
BuildRequires: pkgconfig
Provides: hg = %{version}-%{release}

Requires: python
Requires: python(abi) = %{python_version}

%description
Mercurial is a fast, lightweight source control management system designed
for efficient handling of very large distributed projects.

Quick start: http://www.selenic.com/mercurial/wiki/index.cgi/QuickStart
Tutorial: http://www.selenic.com/mercurial/wiki/index.cgi/Tutorial
Extensions: http://www.selenic.com/mercurial/wiki/index.cgi/CategoryExtension

%define pkg mercurial

#%package -n emacs-%{pkg}
#Summary:	Mercurial version control system support for Emacs
#Group:		Applications/Editors
#Requires:	hg = %{version}-%{release}, emacs-common
#Requires:       emacs(bin) >= %{emacs_version}
#Obsoletes:	%{pkg}-emacs

#%description -n emacs-%{pkg}
#Contains byte compiled elisp packages for %{pkg}.
#To get started: start emacs, load hg-mode with M-x hg-mode, and show 
#help with C-c h h

#%package -n emacs-%{pkg}-el
#Summary:        Elisp source files for %{pkg} under GNU Emacs
#Group:          Applications/Editors
#Requires:       emacs-%{pkg} = %{version}-%{release}

#%description -n emacs-%{pkg}-el
#This package contains the elisp source files for %{pkg} under GNU Emacs. You
#do not need to install this package to run %{pkg}. Install the emacs-%{pkg}
#package to use %{pkg} with GNU Emacs.

%package hgk
Summary:	Hgk interface for mercurial
Group:		Development/Tools
Requires:	hg = %{version}-%{release}, tk


%description hgk
A Mercurial extension for displaying the change history graphically
using Tcl/Tk.  Displays branches and merges in an easily
understandable way and shows diffs for each revision.  Based on
gitk for the git SCM.

Adds the "hg view" command.  See 
http://www.selenic.com/mercurial/wiki/index.cgi/UsingHgk for more
documentation.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.

%prep
%setup -q -a 1
%patch0 -p1

%build
export SHELL="/@unixroot/usr/bin/sh.exe"
export EMXSHELL="cmd.exe"
# Building docs is broken due to missing python-docutils package, skip this step
#make SHELL=sh all
make build

%install
export EMXSHELL="cmd.exe"
rm -rf $RPM_BUILD_ROOT
%{__python} setup.py install -O1 --root $RPM_BUILD_ROOT --prefix %{_prefix} --record=%{name}.files
# As we can't build docs (see above) disable it for now (only affects man)
#make install-doc SHELL=sh DESTDIR=$RPM_BUILD_ROOT MANDIR=%{_mandir}

grep -v 'hgk.py*' < %{name}.files > %{name}-base.files
grep 'hgk.py*' < %{name}.files > %{name}-hgk.files

#install -D contrib/hgk       $RPM_BUILD_ROOT%{_libexecdir}/mercurial/hgk
install contrib/hg-ssh       $RPM_BUILD_ROOT%{_bindir}

bash_completion_dir=$RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
mkdir -p $bash_completion_dir
install -m 644 contrib/bash_completion $bash_completion_dir/mercurial.sh

zsh_completion_dir=$RPM_BUILD_ROOT%{_datadir}/zsh/site-functions
mkdir -p $zsh_completion_dir
install -m 644 contrib/zsh_completion $zsh_completion_dir/_mercurial

#mkdir -p $RPM_BUILD_ROOT%{emacs_lispdir}

#pushd contrib
#for file in mercurial.el mq.el; do
#  emacs -batch -l mercurial.el --no-site-file -f batch-byte-compile $file
#  install -p -m 644 $file ${file}c $RPM_BUILD_ROOT%{emacs_lispdir}
#  rm ${file}c
#done
#popd



mkdir -p $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

#mkdir -p $RPM_BUILD_ROOT%{emacs_startdir} && install -m644 %SOURCE1 $RPM_BUILD_ROOT%{emacs_startdir}

#cat >hgk.rc <<EOF
#[extensions]
## enable hgk extension ('hg help' shows 'view' as a command)
#hgk=
#
#[hgk]
#path=%{_libexecdir}/mercurial/hgk
#EOF
#install hgk.rc $RPM_BUILD_ROOT/%{_sysconfdir}/mercurial/hgrc.d

install contrib/mergetools.hgrc $RPM_BUILD_ROOT%{_sysconfdir}/mercurial/hgrc.d/mergetools.rc

#build exe wrapper
gcc -g -Zomf %optflags -DPYTHON_EXE=\"python%{python_version}.exe\" -o $RPM_BUILD_ROOT/%{_bindir}/hg.exe exec-py.c


%clean
rm -rf $RPM_BUILD_ROOT

%files
# -f %{name}-base.files
%defattr(-,root,root,-)
%doc CONTRIBUTORS COPYING doc/README doc/hg*.txt doc/hg*.html *.cgi contrib/*.fcgi
# As we can't build docs (see above) disable it for now (only affects man)
#%doc %attr(644,root,root) %{_mandir}/man?/hg*
%doc %attr(644,root,root) contrib/*.svg contrib/sample.hgrc
%{_sysconfdir}/bash_completion.d/mercurial.sh
%{_datadir}/zsh/site-functions/_mercurial
%{_bindir}/hg
%{_bindir}/hg.exe
%{_bindir}/hg-ssh
%{_libdir}/*
%dir %{_sysconfdir}/bash_completion.d/
%dir %{_datadir}/zsh/site-functions/
%dir %{_sysconfdir}/mercurial
%dir %{_sysconfdir}/mercurial/hgrc.d
%config(noreplace) %{_sysconfdir}/mercurial/hgrc.d/mergetools.rc
#%dir %{python_sitearch}/mercurial
#%dir %{python_sitearch}/hgext

#%files -n emacs-%{pkg}
#%{emacs_lispdir}/*.elc
#%{emacs_startdir}/*.el

#%files -n emacs-%{pkg}-el
#%{emacs_lispdir}/*.el

#%files hgk -f %{name}-hgk.files
#%{_libexecdir}/mercurial/
#%{_sysconfdir}/mercurial/hgrc.d/hgk.rc

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg

##%%check
##cd tests && %{__python} run-tests.py

%changelog
* Wed Apr 09 2014 yd
- build for python 2.7.
- added debug package with symbolic info for exceptq.

* Sat Mar 30 2013 Dmitriy Kuminov <coding@dmik.org> - 2.5.2-1
- Update to version 2.5.2 from vendor.
