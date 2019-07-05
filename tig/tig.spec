# Based on http://pkgs.fedoraproject.org/cgit/rpms/tig.git/tree/tig.spec?id=5d56685605a3a91f698586130cdd619652b49add

%global bash_completion_dir %(pkg-config --variable=completionsdir bash-completion || echo %{_sysconfdir}/bash_completion.d)/

Name:           tig
Version:        2.2.1
Release:        1%{?dist}
Summary:        Text-mode interface for the git revision control system

License:        GPLv2+
URL:            http://jonas.nitro.dk/tig

%scm_source     github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2

BuildRequires:  git
BuildRequires:  ncurses-devel
# TODO don't have these on OS/2 yet.
%if 0
BuildRequires:  xmlto
BuildRequires:  asciidoc
BuildRequires:  bash-completion
%endif
Requires:       git

%description
Tig is a repository browser for the git revision control system that
additionally can act as a pager for output from various git commands.

When browsing repositories, it uses the underlying git commands to present the
user with various views, such as summarized revision log and showing the commit
with the log message, diffstat, and the diff.

Using it as a pager, it will display input from stdin and colorize it.

%debug_package


%prep
%scm_setup
# Generate configure & friends
autogen.sh

%build
export LDFLAGS="-Zomf -Zmap -Zhigh-mem -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure
# TODO don't have these on OS/2 yet (doc-man doc-html won't work).
# TODO %make_build requires rpm 4.13.0.1 to fix make -O flag
#make_build all doc-man doc-html
%{__make} %{_smp_mflags} all

#Convert to unix line endings
# TODO don't have these on OS/2 yet (doc-man doc-html won't work).
#sed -i -e 's/\r//' *.html

# Remove shebang from bash-completion script
sed -i '/^#!bash/,+1 d' contrib/%{name}-completion.bash


%install
# TODO don't have these on OS/2 yet (install-doc-man).
#make_install install-doc-man
%make_install

# Setup bash completion
install -Dpm 644 contrib/%{name}-completion.bash %{buildroot}%{bash_completion_dir}/%{name}


%files
%license COPYING
# TODO don't have these on OS/2 yet (doc-man doc-html won't work).
#doc COPYING NEWS.adoc README.adoc *.html
%doc COPYING NEWS.adoc README.adoc
%{_bindir}/tig.exe
%{bash_completion_dir}
%config(noreplace) %{_sysconfdir}/%{name}rc
# TODO don't have these on OS/2 yet (doc-man doc-html won't work).
%if 0
%{_mandir}/man1/tig.1*
%{_mandir}/man5/tigrc.5*
%{_mandir}/man7/tigmanual.7*
%endif


%changelog
* Mon Apr 10 2017 Dmitriy Kuminov <coding@dmik.org> 2.2.1-1
- Initial package.
