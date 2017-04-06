# Note: this .spec is borrowed from http://pkgs.fedoraproject.org/cgit/rpms/git.git

# Pass --without docs to rpmbuild if you don't want the documentation (force it for now)
%define _without_docs 1

%global gitcoredir          %{_libexecdir}/git-core
%global noarch_sub          1
%global libcurl_devel       libcurl-devel
%global docbook_suppress_sp 0
%global enable_ipv6         0
%global use_prebuilt_docs   0

%global bashcompdir         %{_sysconfdir}/bash_completion.d
%global bashcomproot        %{bashcompdir}
%global use_systemd         0

Name:           git
Version:        2.11.0
Release:        2%{?dist}
Summary:        Fast Version Control System
License:        GPLv2
Group:          Development/Tools
URL:            https://git-scm.com/

%scm_source     svn http://svn.netlabs.org/repos/ports/git/trunk 2163

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if ! %{use_prebuilt_docs} && ! 0%{?_without_docs}
BuildRequires:  asciidoc >= 8.4.1
BuildRequires:  xmlto
%endif
#BuildRequires:  emacs
BuildRequires:  expat-devel
BuildRequires:  gettext
BuildRequires:  %{libcurl_devel}
#BuildRequires:  pcre-devel
#BuildRequires:  perl-generators
#BuildRequires:  perl(Test)
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel >= 1.2
%if %{use_systemd}
# For macros
BuildRequires:  systemd
%endif

Requires:       git-core = %{version}-%{release}
Requires:       git-core-doc = %{version}-%{release}
#Requires:       perl(Error)
%if ! %{defined perl_bootstrap}
# TODO Doesn't exist on OS/2 yet.
#Requires:       perl(Term::ReadKey)
%endif
Requires:       perl-Git = %{version}-%{release}

# Obsolete git-arch
Obsoletes:      git-arch < %{version}-%{release}

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git rpm installs common set of tools which are usually using with
small amount of dependencies. To install all git packages, including
tools for integrating with other SCMs, install the git-all meta-package.

%package all
Summary:        Meta-package to pull in all git tools
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
Requires:       git-cvs = %{version}-%{release}
Requires:       git-email = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       git-p4 = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}
%if ! %{defined perl_bootstrap}
# TODO Doesn't exist on OS/2 yet.
#Requires:       perl(Term::ReadKey)
%endif
#Requires:       emacs-git = %{version}-%{release}
Obsoletes:      git <= 1.5.4.3

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package core
Summary:        Core package of git with minimal funcionality
Group:          Development/Tools
Requires:       less
#Requires:       openssh-clients
#Requires:       rsync
Requires:       zlib >= 1.2
%description core
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-core rpm installs really the core tools with minimal
dependencies. Install git package for common set of tools.
To install all git packages, including tools for integrating with
other SCMs, install the git-all meta-package.

%package core-doc
Summary:        Documentation files for git-core
Group:          Development/Tools
Requires:       git-core = %{version}-%{release}

%description core-doc
Documentation files for git-core package including man pages.

%package daemon
Summary:        Git protocol dæmon
Group:          Development/Tools
Requires:       git = %{version}-%{release}
%if %{use_systemd}
Requires:       systemd
Requires(post): systemd
Requires(preun):  systemd
Requires(postun): systemd
%else
#Requires:       xinetd
%endif
%description daemon
The git dæmon for supporting git:// access to git repositories

%if 0
%package -n gitweb
Summary:        Simple web interface to git repositories
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}

%description -n gitweb
Simple web interface to track changes in git repositories
%endif

%package p4
Summary:        Git tools for working with Perforce depots
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
BuildRequires:  python
Requires:       git = %{version}-%{release}
%description p4
%{summary}.

%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools
Requires:       git = %{version}-%{release}, subversion
Requires:       perl(Digest::MD5)
%if ! %{defined perl_bootstrap}
# TODO Doesn't exist on OS/2 yet.
#Requires:       perl(Term::ReadKey)
%endif
%description svn
Git tools for importing Subversion repositories.

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, cvs
Requires:       cvsps
Requires:       perl(DBD::SQLite)
%description cvs
Git tools for importing CVS repositories.

%package email
Summary:        Git tools for sending email
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, perl-Git = %{version}-%{release}
Requires:       perl(Authen::SASL)
Requires:       perl(Net::SMTP::SSL)
%description email
Git tools for sending email.

%if 0

%package gui
Summary:        Git GUI tool
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, tk >= 8.4
Requires:       gitk = %{version}-%{release}
%description gui
Git GUI tool.

%package -n gitk
Summary:        Git revision tree visualiser
Group:          Development/Tools
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, tk >= 8.4
%description -n gitk
Git revision tree visualiser.

%endif

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
%if %{noarch_sub}
BuildArch:      noarch
%endif
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
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Git-SVN
Perl interface to Git.

%if 0

%package -n emacs-git
Summary:        Git version control system support for Emacs
Group:          Applications/Editors
Requires:       git = %{version}-%{release}
%if %{noarch_sub}
BuildArch:      noarch
Requires:       emacs(bin) >= %{_emacs_version}
%else
Requires:       emacs-common
%endif

%description -n emacs-git
%{summary}.

%package -n emacs-git-el
Summary:        Elisp source files for git version control system support for Emacs
Group:          Applications/Editors
%if %{noarch_sub}
BuildArch:      noarch
%endif
Requires:       emacs-git = %{version}-%{release}

%description -n emacs-git-el
%{summary}.

%endif

%debug_package

%prep
%scm_setup

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
cat << \EOF > config.mak
V = 1
CFLAGS = %{optflags}
#LDFLAGS = %{__global_ldflags}
#BLK_SHA1 = 1
#NEEDS_CRYPTO_WITH_SSL = 1
#USE_LIBPCRE = 1
ETC_GITCONFIG = %{_sysconfdir}/gitconfig
DESTDIR = %{buildroot}
INSTALL = %{_bindir}/install -p
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

# Filter bogus perl requires
# packed-refs comes from a comment in contrib/hooks/update-paranoid
%{?perl_default_filter}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(packed-refs\\)
%if ! %{defined perl_bootstrap}
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(Term::ReadKey\\)
%endif

%build
make %{?_smp_mflags} all
%if ! %{use_prebuilt_docs} && ! 0%{?_without_docs}
make %{?_smp_mflags} doc
%endif

%if 0
make -C contrib/emacs
%endif

make -C contrib/subtree/

# Remove shebang from bash-completion script
sed -i '/^#!bash/,+1 d' contrib/completion/git-completion.bash

%install
rm -rf %{buildroot}
make %{?_smp_mflags} INSTALLDIRS=vendor install
%if ! %{use_prebuilt_docs} && ! 0%{?_without_docs}
make %{?_smp_mflags} INSTALLDIRS=vendor install-doc
%else
%if %{use_prebuilt_docs}
cp -a prebuilt_docs/man/* %{buildroot}%{_mandir}
cp -a prebuilt_docs/html/* Documentation/
%endif
%endif

%if 0

%global elispdir %{_emacs_sitelispdir}/git
make -C contrib/emacs install \
    emacsdir=%{buildroot}%{elispdir}
for elc in %{buildroot}%{elispdir}/*.elc ; do
    install -pm 644 contrib/emacs/$(basename $elc .elc).el \
    %{buildroot}%{elispdir}
done
install -Dpm 644 %{SOURCE10} \
    %{buildroot}%{_emacs_sitestartdir}/git-init.el

%endif

make -C contrib/subtree install
%if ! %{use_prebuilt_docs} && ! 0%{?_without_docs}
make -C contrib/subtree install-doc
%endif
# it's ugly hack, but this file don't need to be copied to this directory
# it's already part of git-core-doc and it's alone here
rm -f %{buildroot}%{?_pkgdocdir}%{!?_pkgdocdir:%{_docdir}/%{name}-%{version}}/git-subtree.html

%if 0
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -pm 0644 %{SOURCE12} %{buildroot}%{_sysconfdir}/httpd/conf.d/git.conf
sed "s|@PROJECTROOT@|%{_var}/lib/git|g" \
    %{SOURCE14} > %{buildroot}%{_sysconfdir}/gitweb.conf
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
%if %{use_systemd}
mkdir -p %{buildroot}%{_unitdir}
cp -a %{SOURCE15} %{SOURCE16} %{buildroot}%{_unitdir}
%else
%if 0
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
    %{SOURCE11} > %{buildroot}%{_sysconfdir}/xinetd.d/git
%endif
%endif

# Setup bash completion
install -Dpm 644 contrib/completion/git-completion.bash %{buildroot}%{bashcompdir}/git
ln -s git %{buildroot}%{bashcompdir}/gitk

# Install tcsh completion
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-completion.tcsh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

# Move contrib/hooks out of %%docdir and make them executable
mkdir -p %{buildroot}%{_datadir}/git-core/contrib
mv contrib/hooks %{buildroot}%{_datadir}/git-core/contrib
chmod +x %{buildroot}%{_datadir}/git-core/contrib/hooks/*
ln -s %{buildroot}%{_datadir}/git-core/contrib/hooks contrib/

# Install git-prompt.sh
mkdir -p %{buildroot}%{_datadir}/git-core/contrib/completion
install -pm 644 contrib/completion/git-prompt.sh \
    %{buildroot}%{_datadir}/git-core/contrib/completion/

%if 0
# install git-gui .desktop file
desktop-file-install \
%if %{desktop_vendor_tag}
  --vendor fedora \
%endif
  --dir=%{buildroot}%{_datadir}/applications %{SOURCE13}
%endif

# find translations
%find_lang %{name} %{name}.lang
cat %{name}.lang >> bin-man-doc-files

# quiet some rpmlint complaints
chmod -R g-w %{buildroot}
find %{buildroot} -name git-mergetool--lib | xargs chmod a-x
# rm -f {Documentation/technical,contrib/emacs,contrib/credential/gnome-keyring}/.gitignore
# These files probably are not needed
find . -name .gitignore -delete
chmod a-x Documentation/technical/api-index.sh
find contrib -type f | xargs chmod -x

# Split core files
not_core_re="git-(add--interactive|am|credential-netrc|difftool|instaweb|relink|request-pull|send-mail|submodule)|gitweb|prepare-commit-msg|pre-rebase"
grep -vE "$not_core_re|\/man\/" bin-man-doc-files > bin-files-core
%if %{use_prebuilt_docs} || ! 0%{?_without_docs}
grep -vE "$not_core_re" bin-man-doc-files | grep "\/man\/" > man-doc-files-core
%endif
grep -E "$not_core_re" bin-man-doc-files > bin-man-doc-git-files


%clean
rm -rf %{buildroot}

%if %{use_systemd}
%post daemon
%systemd_post git@.service

%preun daemon
%systemd_preun git@.service

%postun daemon
%systemd_postun_with_restart git@.service
%endif

%files -f bin-man-doc-git-files
%defattr(-,root,root)
%if 0
%{elispdir}
%{_emacs_sitestartdir}/git-init.el
%endif
%{_datadir}/git-core/contrib/hooks/update-paranoid
%{_datadir}/git-core/contrib/hooks/setgitperms.perl
#%{_datadir}/git-core/*
#%doc Documentation/*.txt
#%{!?_without_docs: %doc Documentation/*.html}
#%{!?_without_docs: %doc Documentation/howto/* Documentation/technical/*}

%files core -f bin-files-core
%defattr(-,root,root)
%{!?_licensedir:%global license %doc}
%license COPYING
# exlude is best way here because of troubels with symlinks inside git-core/
%exclude %{_datadir}/git-core/contrib/hooks/update-paranoid
%exclude %{_datadir}/git-core/contrib/hooks/setgitperms.perl
%{bashcomproot}
%{_datadir}/git-core/

%if %{use_prebuilt_docs} || ! 0%{?_without_docs}
%files core-doc -f man-doc-files-core
%else
%files core-doc
%endif
%defattr(-,root,root)
%doc README.md Documentation/*.txt Documentation/RelNotes contrib/
%{!?_without_docs: %doc Documentation/*.html Documentation/docbook-xsl.css}
%{!?_without_docs: %doc Documentation/howto Documentation/technical}
%if ! %{use_prebuilt_docs}
%{!?_without_docs: %doc contrib/subtree/git-subtree.html}
%endif

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
%if "%{gitcoredir}" != "%{_bindir}"
%{_bindir}/git-cvsserver
%endif
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
%{_unitdir}/git@.service
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

%changelog
* Thu Apr 6 2017 Dmitriy Kuminov <coding@dmik.org> 2.11.0-2
- Make git add --interactive output use CRLFs on DOS-like platforms.
- Remove a lot of outdated OS/2-specific code.
- Make the .git directory truly hidden on OS/2.
- Enable mmap support on OS/2.
- Change vendor to bww bitwise works GmbH.

* Tue Dec 13 2016 Dmitriy Kuminov <coding@dmik.org> 2.11.0-1
- Update git to version 2.11.0.
- Increase stack size to 8 MB to fix crashes when cloning huge repos.
- Link against LIBCx 0.4 (this brings EXCEPTQ TRP report generator).
- Rebuild against LIBC 0.6.6 and GCC 4.9.2.
- Enable %lang definitions.

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
