%define _without_docs 1

# Pass --without docs to rpmbuild if you don't want the documentation
%if 0%{?rhel} && 0%{?rhel} <= 5
%global gitcoredir %{_bindir}
%else
%global gitcoredir %{_libexecdir}/git-core
%endif

Name:           git
Version:        1.7.6.1
Release:        7%{?dist}
Summary:        Fast Version Control System
License:        GPLv2
Group:          Development/Tools
URL:            http://git-scm.com/

Source0:        http://kernel.org/pub/software/scm/git/%{name}-%{version}.tar.bz2
Source1:        git-os2.zip

Patch0:         git-os2.diff

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  desktop-file-utils
%if 0%{?fedora}
BuildRequires:  emacs >= 22.2
BuildRequires:  libcurl-devel
%else
BuildRequires:  curl-devel
%endif
#BuildRequires:  expat-devel
BuildRequires:  gettext
BuildRequires:  openssl-devel
BuildRequires:  zlib-devel >= 1.2
#%{!?_without_docs:BuildRequires: asciidoc > 6.0.3, xmlto}

#Requires:       less
#Requires:       openssh-clients
%if 0%{?fedora} || 0%{?rhel} >= 5
Requires:       perl(Error)
%endif
#Requires:       perl-Git = %{version}-%{release}
#Requires:       rsync
Requires:       zlib >= 1.2

Provides:       git-core = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 5
Obsoletes:      git-core <= 1.5.4.3
%else
# EL-4 has 1.5.4.7-3.el4.  We don't support this, but no point making it more
# difficult than it needs to be (folks stuck on EL-4 have it bad enough ;).
Obsoletes:      git-core <= 1.5.4.7-4
%endif

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
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
Requires:       git-svn = %{version}-%{release}
Requires:       git-cvs = %{version}-%{release}
Requires:       git-email = %{version}-%{release}
Requires:       gitk = %{version}-%{release}
Requires:       git-gui = %{version}-%{release}
Requires:       perl-Git = %{version}-%{release}
%if 0%{?fedora}
Requires:       emacs-git = %{version}-%{release}
Requires:       git-arch = %{version}-%{release}
%endif
%if 0%{?fedora} || 0%{?rhel} >= 5
Obsoletes:      git <= 1.5.4.3
%else
# EL-4 has 1.5.4.7-3.el4.  We don't support this, but no point making it more
# difficult than it needs to be (folks stuck on EL-4 have it bad enough ;).
Obsoletes:      git <= 1.5.4.7-4
%endif

%description all
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

This is a dummy package which brings in all subpackages.

%package daemon
Summary:        Git protocol dæmon
Group:          Development/Tools
Requires:       git = %{version}-%{release}
#Requires:       xinetd
%description daemon
The git dæmon for supporting git:// access to git repositories

%package -n gitweb
Summary:        Simple web interface to git repositories
Group:          Development/Tools
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}

%description -n gitweb
Simple web interface to track changes in git repositories


%package svn
Summary:        Git tools for importing Subversion repositories
Group:          Development/Tools
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, subversion, perl(Term::ReadKey)
%description svn
Git tools for importing Subversion repositories.

%package cvs
Summary:        Git tools for importing CVS repositories
Group:          Development/Tools
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, cvs
%if 0%{?fedora} || 0%{?rhel} >= 5
Requires:       cvsps
%endif
%description cvs
Git tools for importing CVS repositories.

%if 0%{?fedora}
%package arch
Summary:        Git tools for importing Arch repositories
Group:          Development/Tools
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, tla
%description arch
Git tools for importing Arch repositories.
%endif

%package email
Summary:        Git tools for sending email
Group:          Development/Tools
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, perl-Git = %{version}-%{release}
Requires:       perl(Authen::SASL)
%if 0%{?fedora} || 0%{?rhel} >= 5
Requires:       perl(Net::SMTP::SSL)
%endif
%description email
Git tools for sending email.

%package gui
Summary:        Git GUI tool
Group:          Development/Tools
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, tk >= 8.4
Requires:       gitk = %{version}-%{release}
%description gui
Git GUI tool.

%package -n gitk
Summary:        Git revision tree visualiser
Group:          Development/Tools
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, tk >= 8.4
%description -n gitk
Git revision tree visualiser.

%package -n perl-Git
Summary:        Perl interface to Git
Group:          Development/Libraries
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}
%if 0%{?fedora} || 0%{?rhel} >= 5
BuildRequires:  perl(Error), perl(ExtUtils::MakeMaker)
Requires:       perl(Error)
%endif
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Git
Perl interface to Git.

%if 0%{?fedora}
%package -n emacs-git
Summary:        Git version control system support for Emacs
Group:          Applications/Editors
%if 0%{?fedora} >= 10
BuildArch:      noarch
%endif
Requires:       git = %{version}-%{release}, emacs-common >= 22.2

%description -n emacs-git
%{summary}.
%endif

%prep
%setup -q -a 1
%patch0 -p1

# Use these same options for every invocation of 'make'.
# Otherwise it will rebuild in %%install due to flags changes.
cat << \EOF > config.mak
V = 1
CFLAGS = %{optflags}
BLK_SHA1 = 1
NEEDS_CRYPTO_WITH_SSL = 1
NO_PYTHON = 1
ETC_GITCONFIG = %{_sysconfdir}/gitconfig
DESTDIR = %{buildroot}
INSTALL = install -p
GITWEB_PROJECTROOT = %{_var}/lib/git
htmldir = %{_docdir}/%{name}-%{version}
prefix = %{_prefix}
EOF

%if 0%{?fedora}
cat << \EOF >> config.mak
ASCIIDOC8 = 1
ASCIIDOC_NO_ROFF = 1
EOF
%endif

%if 0%{?rhel} && 0%{?rhel} <= 5
echo gitexecdir = %{_bindir} >> config.mak
%endif

# Filter bogus perl requires
# packed-refs comes from a comment in contrib/hooks/update-paranoid
cat << \EOF > %{name}-req
#!/bin/sh
%{__perl_requires} $* |\
sed -e '/perl(packed-refs)/d'
EOF

%global __perl_requires %{_builddir}/%{name}-%{version}/%{name}-req
chmod +x %{__perl_requires}

%build
export MAKESHELL=/@unixroot/usr/bin/sh
export CONFIG_SHELL=/@unixroot/usr/bin/sh
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zexe -Zargs-wild -Zargs-resp"
export LIBS="-lurpo"
%configure \
	--without-tcltk \
        "--cache-file=%{_topdir}/cache/%{name}-%{_target_cpu}.cache"

make %{?_smp_mflags} all %{!?_without_docs: doc}

%if 0%{?fedora}
make -C contrib/emacs
%endif

# Remove shebang from bash-completion script
sed -i '/^#!bash/,+1 d' contrib/completion/git-completion.bash

%install
export MAKESHELL=/@unixroot/usr/bin/sh
rm -rf %{buildroot}
make %{?_smp_mflags} INSTALLDIRS=vendor install %{!?_without_docs: install-doc}

%if 0%{?fedora}
make -C contrib/emacs install \
    emacsdir=%{buildroot}%{_datadir}/emacs/site-lisp
for elc in %{buildroot}%{_datadir}/emacs/site-lisp/*.elc ; do
    install -pm 644 contrib/emacs/$(basename $elc .elc).el \
    %{buildroot}%{_datadir}/emacs/site-lisp
done
install -Dpm 644 %{SOURCE1} \
    %{buildroot}%{_datadir}/emacs/site-lisp/site-start.d/git-init.el
%endif

mkdir -p %{buildroot}%{_var}/www/git
#install -pm 644 gitweb/*.css %{buildroot}%{_var}/www/git
#install -pm 644 gitweb/*.js %{buildroot}%{_var}/www/git
#install -pm 644 gitweb/*.png %{buildroot}%{_var}/www/git
#install -pm 755 gitweb/gitweb.cgi %{buildroot}%{_var}/www/git
#mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
#install -pm 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/httpd/conf.d/git.conf
#sed "s|@PROJECTROOT@|%{_var}/lib/git|g" \
#    %{SOURCE5} > %{buildroot}%{_sysconfdir}/gitweb.conf

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'

%if ! 0%{?fedora}
find %{buildroot} Documentation -type f -name 'git-archimport*' -exec rm -f {} ';'
%endif

(find %{buildroot}%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^%{buildroot}@@) > bin-man-doc-files
(find %{buildroot}%{_libexecdir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^%{buildroot}@@) >> bin-man-doc-files
#(find %{buildroot}%{perl_vendorlib} -type f | sed -e s@^%{buildroot}@@) >> perl-files
%if %{!?_without_docs:1}0
(find %{buildroot}%{_mandir} -type f | grep -vE "archimport|svn|git-cvs|email|gitk|git-gui|git-citool|git-daemon" | sed -e s@^%{buildroot}@@ -e 's/$/*/' ) >> bin-man-doc-files
%else
rm -rf %{buildroot}%{_mandir}
%endif

mkdir -p %{buildroot}%{_var}/lib/git
mkdir -p %{buildroot}%{_sysconfdir}/xinetd.d
# On EL <= 5, xinetd does not enable IPv6 by default
enable_ipv6="        # xinetd does not enable IPv6 by default
        flags           = IPv6"
perl -p \
    -e "s|\@GITCOREDIR\@|%{gitcoredir}|g;" \
    -e "s|\@BASE_PATH\@|%{_var}/lib/git|g;" \
%if 0%{?rhel} && 0%{?rhel} <= 5
    -e "s|^}|$enable_ipv6\n$&|;" \
%endif
    %{SOURCE2} > %{buildroot}%{_sysconfdir}/xinetd.d/git

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -pm 644 contrib/completion/git-completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/git

# Move contrib/hooks out of %%docdir and make them executable
#mkdir -p %{buildroot}%{_datadir}/git-core/contrib
#mv contrib/hooks %{buildroot}%{_datadir}/git-core/contrib
#chmod +x %{buildroot}%{_datadir}/git-core/contrib/hooks/*
#pushd contrib > /dev/null
#ln -s ../../../git-core/contrib/hooks
#popd > /dev/null

# install git-gui .desktop file
#desktop-file-install \
#%if 0%{?rhel} && 0%{?rhel} <= 5
#    --vendor fedora \
#%endif
#    --dir=%{buildroot}%{_datadir}/applications %{SOURCE4}

# quiet some rpmlint complaints
chmod -R g-w %{buildroot}
find %{buildroot} -name git-mergetool--lib | xargs chmod a-x
rm -f {Documentation/technical,contrib/emacs}/.gitignore
chmod a-x Documentation/technical/api-index.sh
find contrib -type f | xargs chmod -x


%clean
rm -rf %{buildroot}


%files -f bin-man-doc-files
%defattr(-,root,root)
%{_datadir}/git-core/
%dir %{gitcoredir}
%doc README COPYING Documentation/*.txt contrib/
%{!?_without_docs: %doc Documentation/*.html Documentation/docbook-xsl.css}
%{!?_without_docs: %doc Documentation/howto Documentation/technical}
%{_sysconfdir}/bash_completion.d


%files svn
%defattr(-,root,root)
%{gitcoredir}/*svn*
#%doc Documentation/*svn*.txt
%{!?_without_docs: %{_mandir}/man1/*svn*.1*}
%{!?_without_docs: %doc Documentation/*svn*.html }

%files cvs
%defattr(-,root,root)
#%doc Documentation/*git-cvs*.txt
%{_bindir}/git-cvsserver
%{gitcoredir}/*cvs*
%{!?_without_docs: %{_mandir}/man1/*cvs*.1*}
%{!?_without_docs: %doc Documentation/*git-cvs*.html }

%if 0%{?fedora}
%files arch
%defattr(-,root,root)
%doc Documentation/git-archimport.txt
%{gitcoredir}/git-archimport
%{!?_without_docs: %{_mandir}/man1/git-archimport.1*}
%{!?_without_docs: %doc Documentation/git-archimport.html }
%endif

%files email
%defattr(-,root,root)
#%doc Documentation/*email*.txt
%{gitcoredir}/*email*
%{!?_without_docs: %{_mandir}/man1/*email*.1*}
%{!?_without_docs: %doc Documentation/*email*.html }

%files gui
%defattr(-,root,root)
#%{gitcoredir}/git-gui*
#%{gitcoredir}/git-citool
#%{_datadir}/applications/*git-gui.desktop
#%{_datadir}/git-gui/
#%{!?_without_docs: %{_mandir}/man1/git-gui.1*}
#%{!?_without_docs: %doc Documentation/git-gui.html}
#%{!?_without_docs: %{_mandir}/man1/git-citool.1*}
#%{!?_without_docs: %doc Documentation/git-citool.html}

%files -n gitk
%defattr(-,root,root)
#%doc Documentation/*gitk*.txt
#%{_bindir}/*gitk*
#%{_datadir}/gitk
#%{!?_without_docs: %{_mandir}/man1/*gitk*.1*}
#%{!?_without_docs: %doc Documentation/*gitk*.html }

%files -n perl-Git
# -f perl-files
%defattr(-,root,root)
%if 0%{?fedora}
%files -n emacs-git
%defattr(-,root,root)
%doc contrib/emacs/README
%{_datadir}/emacs/site-lisp/*git*.el*
%{_datadir}/emacs/site-lisp/site-start.d/git-init.el
%endif

%files daemon
%defattr(-,root,root)
%doc Documentation/*daemon*.txt
%config(noreplace)%{_sysconfdir}/xinetd.d/git
%{gitcoredir}/git-daemon.exe
%{_var}/lib/git
%{!?_without_docs: %{_mandir}/man1/*daemon*.1*}
%{!?_without_docs: %doc Documentation/*daemon*.html}

%files -n gitweb
%defattr(-,root,root)
#%doc gitweb/INSTALL gitweb/README
#%config(noreplace)%{_sysconfdir}/gitweb.conf
#%config(noreplace)%{_sysconfdir}/httpd/conf.d/git.conf
%{_var}/www/git/


%files all
# No files for you!

%changelog
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
