# Note: this .spec is borrowed from git-2.1.0-1.fc22.src.rpm

# Pass --without docs to rpmbuild if you don't want the documentation (force it for now)
%define _without_docs 1

%global gitcoredir          %{_libexecdir}/git-core
%global libcurl_devel       libcurl-devel
%global docbook_suppress_sp 0
%global enable_ipv6         0

%global use_systemd         0

Name:           git
Version:        2.0.0
Release:        2%{?dist}
Summary:        Fast Version Control System
License:        GPLv2
Group:          Development/Tools
URL:            http://git-scm.com/
#Source0:        http://www.kernel.org/pub/software/scm/git/%{name}-%{version}.tar.gz

%define svn_url     http://svn.netlabs.org/repos/ports/git/branches/2.0
%define svn_rev     864

Source: %{name}-%{version}-r%{svn_rev}.zip

BuildRequires: gcc make subversion zip

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if ! 0%{?_without_docs}
BuildRequires:  asciidoc >= 8.4.1
BuildRequires:  xmlto
%endif
#BuildRequires:  emacs
BuildRequires:  expat-devel
BuildRequires:  gettext
BuildRequires:  libcurl-devel
#BuildRequires:  pcre-devel
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel >= 1.2

#Requires:       less
#Requires:       openssh-clients
#Requires:       perl(Error)
#Requires:       perl(Term::ReadKey)
Requires:       perl-Git = %{version}-%{release}
#Requires:       rsync
Requires:       zlib >= 1.2

Provides:       git-core = %{version}-%{release}

# Obsolete git-arch
Obsoletes:      git-arch < %{version}-%{release}

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs the core tools with minimal dependencies.  To
install all git packages, including tools for integrating with other
SCMs, install the git-all meta-package.

%package all
Summary:        Meta-package to pull in all git tools
Group:          Development/Tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       git-cvs = %{version}-%{release}
Requires:       git-email = %{version}-%{release}
#Requires:       git-gui = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       git-p4 = %{version}-%{release}
#Requires:       gitk = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}
#Requires:       emacs-git = %{version}-%{release}
Obsoletes:      git <= 1.5.4.3

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package bzr
Summary:        Git tools for working with bzr repositories
Group:          Development/Tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       bzr

%description bzr
%{summary}.

%package daemon
Summary:        Git protocol dæmon
Group:          Development/Tools
Requires:       git = %{version}-%{release}
#%if %{use_systemd}
#Requires:	systemd
#Requires(post): systemd
#Requires(preun): systemd
#Requires(postun): systemd
#%else
#Requires:       xinetd
#%endif
%description daemon
The git dæmon for supporting git:// access to git repositories

%if 0
%package -n gitweb
Summary:        Simple web interface to git repositories
Group:          Development/Tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}

%description -n gitweb
Simple web interface to track changes in git repositories
%endif

%package hg
Summary:        Git tools for working with mercurial repositories
Group:          Development/Tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       mercurial >= 1.8

%description hg
%{summary}.

%package p4
Summary:        Git tools for working with Perforce depots
Group:          Development/Tools
BuildArch:      noarch
BuildRequires:  python
Requires:       git = %{version}-%{release}
%description p4
%{summary}.

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools
Requires:       git = %{version}-%{release}, subversion, subversion-perl
#Requires:       perl(Term::ReadKey)
%description svn
Git tools for importing Subversion repositories.

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}, cvs
Requires:       cvsps
Requires:	perl-DBD-SQLite
%description cvs
Git tools for importing CVS repositories.

%package email
Summary:        Git tools for sending email
Group:          Development/Tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}, perl-Git = %{version}-%{release}
Requires:       perl(Authen::SASL)
Requires:       perl(Net::SMTP::SSL)
%description email
Git tools for sending email.

%if 0

%package gui
Summary:        Git GUI tool
Group:          Development/Tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}, tk >= 8.4
Requires:       gitk = %{version}-%{release}
%description gui
Git GUI tool.

%package -n gitk
Summary:        Git revision tree visualiser
Group:          Development/Tools
BuildArch:      noarch
Requires:       git = %{version}-%{release}, tk >= 8.4
%description -n gitk
Git revision tree visualiser.

%endif

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
BuildArch:      noarch
Requires:       git = %{version}-%{release}
#BuildRequires:  perl(Error)
BuildRequires:  perl(ExtUtils::MakeMaker)
#Requires:       perl(Error)
#Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Git
Perl interface to Git.

%package -n perl-Git-SVN
Summary:        Perl interface to Git::SVN
Group:          Development/Libraries
BuildArch:      noarch
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Git-SVN
Perl interface to Git.

%if 0

%package -n emacs-git
Summary:        Git version control system support for Emacs
Group:          Applications/Editors
Requires:       git = %{version}-%{release}
BuildArch:      noarch
Requires:       emacs(bin) >= %{_emacs_version}

%description -n emacs-git
%{summary}.

%package -n emacs-git-el
Summary:        Elisp source files for git version control system support for Emacs
Group:          Applications/Editors
BuildArch:      noarch
Requires:       emacs-git = %{version}-%{release}

%description -n emacs-git-el
%{summary}.

%endif

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.


%prep
%if %(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export -r %{svn_rev} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" "%{name}-%{version}")
%endif

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
cat << \EOF > config.mak
V = 1
CFLAGS = %{optflags}
#BLK_SHA1 = 1
#NEEDS_CRYPTO_WITH_SSL = 1
#USE_LIBPCRE = 1
ETC_GITCONFIG = %{_sysconfdir}/gitconfig
DESTDIR = %{buildroot}
INSTALL = install -p
GITWEB_PROJECTROOT = %{_var}/lib/git
GNU_ROFF = 1
htmldir = %{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}
prefix = %{_prefix}
gitwebdir = %{_var}/www/git
EOF

%if "%{gitcoredir}" == "%{_bindir}"
echo gitexecdir = %{_bindir} >> config.mak
%endif

%if %{docbook_suppress_sp}
# This is needed for 1.69.1-1.71.0
echo DOCBOOK_SUPPRESS_SP = 1 >> config.mak
%endif

%build
make %{?_smp_mflags} all
%if ! 0%{?_without_docs}
make doc
%endif

%if 0
make -C contrib/emacs
%endif

make -C contrib/subtree/

# Remove shebang from bash-completion script
sed -i '/^#!bash/,+1 d' contrib/completion/git-completion.bash

%install
rm -rf %{buildroot}
make INSTALLDIRS=vendor install
%if ! 0%{?_without_docs}
make INSTALLDIRS=vendor install-doc
%endif

%if 0

%global elispdir %{_emacs_sitelispdir}/git
make -C contrib/emacs install \
    emacsdir=%{buildroot}%{elispdir}
for elc in %{buildroot}%{elispdir}/*.elc ; do
    install -pm 644 contrib/emacs/$(basename $elc .elc).el \
    %{buildroot}%{elispdir}
done
install -Dpm 644 %{SOURCE2} \
    %{buildroot}%{_emacs_sitestartdir}/git-init.el

%endif

make -C contrib/subtree install
%if ! 0%{?_without_docs}
make -C contrib/subtree install-doc
%endif

%if 0
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -pm 0644 %{SOURCE4} %{buildroot}%{_sysconfdir}/httpd/conf.d/git.conf
sed "s|@PROJECTROOT@|%{_var}/lib/git|g" \
    %{SOURCE6} > %{buildroot}%{_sysconfdir}/gitweb.conf
%else
rm -rf %{buildroot}%{_var}/www/git/
%endif

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'

# git-archimport is not supported
find %{buildroot} Documentation -type f -name 'git-archimport*' -exec rm -f {} ';'

exclude_re="archimport|email|git-citool|git-cvs|git-daemon|git-gui|git-remote-bzr|git-remote-hg|gitk|p4|svn"
(find %{buildroot}%{_bindir} %{buildroot}%{_libexecdir} -type f | grep -vE "$exclude_re" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}%{_bindir} %{buildroot}%{_libexecdir} -mindepth 1 -type d | grep -vE "$exclude_re" | sed -e 's@^%{buildroot}@%dir @') >> bin-man-doc-files
(find %{buildroot}%{perl_vendorlib} -type f | sed -e s@^%{buildroot}@@) > perl-git-files
(find %{buildroot}%{perl_vendorlib} -mindepth 1 -type d | sed -e 's@^%{buildroot}@%dir @') >> perl-git-files
# Split out Git::SVN files
grep Git/SVN perl-git-files > perl-git-svn-files
sed -i "/Git\/SVN/ d" perl-git-files
%if %{!?_without_docs:1}0
(find %{buildroot}%{_mandir} -type f | grep -vE "$exclude_re|Git" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf %{buildroot}%{_mandir}
%endif

mkdir -p %{buildroot}%{_var}/lib/git
%if 0
%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
cp -a %{SOURCE12} %{SOURCE13} %{buildroot}%{_unitdir}
%else
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d
# On EL <= 5, xinetd does not enable IPv6 by default
enable_ipv6="        # xinetd does not enable IPv6 by default
        flags           = IPv6"
perl -p \
    -e "s|\@GITCOREDIR\@|%{gitcoredir}|g;" \
    -e "s|\@BASE_PATH\@|%{_var}/lib/git|g;" \
%if %{enable_ipv6}
    -e "s|^}|$enable_ipv6\n$&|;" \
%endif
    %{SOURCE3} > %{buildroot}%{_sysconfdir}/xinetd.d/git
%endif
%endif

# Install bzr and hg remote helpers from contrib
install -pm 755 contrib/remote-helpers/git-remote-* %{buildroot}%{gitcoredir}

# Setup bash completion
mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 contrib/completion/git-completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/git

# Install tcsh completion
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-completion.tcsh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# Move contrib/hooks out of %%docdir and make them executable
mkdir -p %{buildroot}%{_datadir}/git-core/contrib
mv contrib/hooks %{buildroot}%{_datadir}/git-core/contrib
chmod +x %{buildroot}%{_datadir}/git-core/contrib/hooks/*
ln -s ../../../git-core/contrib/hooks contrib/

# Install git-prompt.sh
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-prompt.sh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# find translations
%if 0
%find_lang %{name} %{name}.lang
cat %{name}.lang >> bin-man-doc-files
%else
find %{buildroot}%{_datadir}/locale/* -type f | sed -e s@^%{buildroot}@@ >> bin-man-doc-files
%endif

# quiet some rpmlint complaints
chmod -R g-w %{buildroot}
find %{buildroot} -name git-mergetool--lib | xargs chmod a-x
rm -f {Documentation/technical,contrib/emacs,contrib/credential/gnome-keyring}/.gitignore
chmod a-x Documentation/technical/api-index.sh
find contrib -type f | xargs chmod -x


%clean
rm -rf %{buildroot}

%if %{use_systemd}
%post daemon
%systemd_post git.service

%preun daemon
%systemd_preun git.service

%postun daemon
%systemd_postun_with_restart git.service
%endif

%files -f bin-man-doc-files
%defattr(-,root,root)
%{_datadir}/git-core/
%doc README COPYING Documentation/*.txt Documentation/RelNotes contrib/
%{!?_without_docs: %doc Documentation/*.html Documentation/docbook-xsl.css}
%{!?_without_docs: %doc Documentation/howto Documentation/technical}
%{_sysconfdir}/bash_completion.d

%files bzr
%defattr(-,root,root)
%{gitcoredir}/git-remote-bzr

%files hg
%defattr(-,root,root)
%{gitcoredir}/git-remote-hg

%files p4
%defattr(-,root,root)
%{gitcoredir}/*p4*
%{gitcoredir}/mergetools/p4merge
%doc Documentation/*p4*.txt
%{!?_without_docs: %{_mandir}/man1/*p4*.1*}
%{!?_without_docs: %doc Documentation/*p4*.html }

%files svn
%defattr(-,root,root)
%{gitcoredir}/*svn*
%doc Documentation/*svn*.txt
%{!?_without_docs: %{_mandir}/man1/*svn*.1*}
%{!?_without_docs: %doc Documentation/*svn*.html }

%files cvs
%defattr(-,root,root)
%doc Documentation/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{gitcoredir}/*cvs*
%{!?_without_docs: %{_mandir}/man1/*cvs*.1*}
%{!?_without_docs: %doc Documentation/*git-cvs*.html }

%files email
%defattr(-,root,root)
%doc Documentation/*email*.txt
%{gitcoredir}/*email*
%{!?_without_docs: %{_mandir}/man1/*email*.1*}
%{!?_without_docs: %doc Documentation/*email*.html }

%if 0

%files gui
%defattr(-,root,root)
%{gitcoredir}/git-gui*
%{gitcoredir}/git-citool
%{_datadir}/applications/*git-gui.desktop
%{_datadir}/git-gui/
%{!?_without_docs: %{_mandir}/man1/git-gui.1*}
%{!?_without_docs: %doc Documentation/git-gui.html}
%{!?_without_docs: %{_mandir}/man1/git-citool.1*}
%{!?_without_docs: %doc Documentation/git-citool.html}

%files -n gitk
%defattr(-,root,root)
%doc Documentation/*gitk*.txt
%{_bindir}/*gitk*
%{_datadir}/gitk
%{!?_without_docs: %{_mandir}/man1/*gitk*.1*}
%{!?_without_docs: %doc Documentation/*gitk*.html }

%endif

%files -n perl-Git -f perl-git-files
%defattr(-,root,root)
%{!?_without_docs: %exclude %{_mandir}/man3/*Git*SVN*.3pm*}
%{!?_without_docs: %{_mandir}/man3/*Git*.3pm*}

%files -n perl-Git-SVN -f perl-git-svn-files
%defattr(-,root,root)
%{!?_without_docs: %{_mandir}/man3/*Git*SVN*.3pm*}

%if 0

%files -n emacs-git
%defattr(-,root,root)
%doc contrib/emacs/README
%dir %{elispdir}
%{elispdir}/*.elc
%{_emacs_sitestartdir}/git-init.el

%files -n emacs-git-el
%defattr(-,root,root)
%{elispdir}/*.el

%endif

%files daemon
%defattr(-,root,root)
%doc Documentation/*daemon*.txt
%if %{use_systemd}
%{_unitdir}/git.socket
%{_unitdir}/git.service
%else
%if 0
%config(noreplace)%{_sysconfdir}/xinetd.d/git
%endif
%endif
%{gitcoredir}/git-daemon*
%{_var}/lib/git
%{!?_without_docs: %{_mandir}/man1/*daemon*.1*}
%{!?_without_docs: %doc Documentation/*daemon*.html}

%if 0
%files -n gitweb
%defattr(-,root,root)
%doc gitweb/INSTALL gitweb/README
%config(noreplace)%{_sysconfdir}/gitweb.conf
%config(noreplace)%{_sysconfdir}/httpd/conf.d/git.conf
%{_var}/www/git/
%endif

%files all
# No files for you!

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg
%{gitcoredir}/*.dbg

%changelog
* Wed Sep 10 2014 yd
- added debug package with symbolic info for exceptq.

* Wed Sep 10 2014 Dmitriy Kuminov <coding@dmik.org> 2.0.0-1
- Update git to version 2.0.0.
- Fix cloning and pushing over HTTP(S).
- Remove many old unneeded patches to have less OS/2-dependent code.

* Sat Dec 17 2011 yd
- rebuild due to gcc 4.4.6 bug.

* Sun Nov 27 2011 yd
- use /@unixroot/usr/bin shell.

* Wed Sep 28 2011 yd
- fixed build patches.
- fixed expat support.

* Sat Sep 24 2011 yd
- symlink script files to exe, so execvp can find them.
- ignore CR while reading CRLF terminated text files.

* Tue Sep 20 2011 yd
- disable broken_path_fix macro.

* Mon Sep 19 2011 yd
- use bigger stack for threads; use socketpair instead of pipes.
