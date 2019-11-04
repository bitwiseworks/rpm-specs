%global bash 0

Summary: Produces a document with syntax highlighting
Name: source-highlight
Version: 3.1.9
Release: 2%{?dist}
License: GPLv3+
URL: http://www.gnu.org/software/src-highlite/
#BuildRequires: bison, flex, boost-devel
BuildRequires: bison, flex
#BuildRequires: help2man, ctags, chrpath, pkgconfig(bash-completion)
BuildRequires: help2man
BuildRequires: gcc
BuildRequires: dos2unix
#Requires: ctags

Vendor: bww bitwise works GmbH
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

%description
This program, given a source file, produces a document with syntax
highlighting. At the moment this package can handle:
Java, Javascript, C/C++, Prolog, Perl, Php3, Python, Flex, ChangeLog, Ruby,
Lua, Caml, Sml and Log as source languages, and HTML, XHTML and ANSI color
escape sequences as output format.


%package devel
Summary: Development files for source-highlight
Requires: %{name} = %{version}-%{release}
# For linking against source-higlight using pkgconfig
#Requires: boost-devel

%description devel
Development files for source-highlight


%debug_package


%prep
%scm_setup
autoreconf -fvi

%build
# !!the below values need to be adjusted and when we have a boost rpm those !! #
# !! are obsolete (if we ever get a boost rpm) !! #
export BOOST_CPPFLAGS="-IE:/Trees/boost/trunk"
export BOOST_ROOT="E:/Trees/boost/trunk"
export BOOST_LDFLAGS="-LE:/Trees/boost/trunk/stage/lib"
# !! end of boost hack !! #

export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx -lpthread"
export VENDOR="%{vendor}"

%configure --disable-static \
           --with-boost-regex=boost_regex
make

%install
%make_install

mv $RPM_BUILD_ROOT%{_datadir}/doc/ docs
%{__sed} -i 's/\r//' docs/source-highlight/*.css

rm -f $RPM_BUILD_ROOT%{_infodir}/dir
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
#find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

echo "\ncxx = cpp.lang" >> $RPM_BUILD_ROOT%{_datadir}/source-highlight/lang.map

%if %{bash}
bashcompdir=$(pkg-config --variable=completionsdir bash-completion)
mkdir -p $RPM_BUILD_ROOT$bashcompdir
mv $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d/source-highlight \
    $RPM_BUILD_ROOT$bashcompdir/
rmdir $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
%else
rm -rf $RPM_BUILD_ROOT%{_sysconfdir}/bash_completion.d
%endif

%files
%doc docs/source-highlight/*
%{_bindir}/cpp2html
%{_bindir}/java2html
%{_bindir}/source-highlight.exe
%{_bindir}/source-highlight-esc.sh
%{_bindir}/check-regexp.exe
%{_bindir}/source-highlight-settings.exe
%{_bindir}/src-hilite-lesspipe.sh
%if %{bash}
%{_datadir}/bash-completion/
%endif
%{_libdir}/srchili*.dll
%dir %{_datadir}/source-highlight
%{_datadir}/source-highlight/*
%{_mandir}/man1/*
%{_infodir}/source-highlight*.info*

%files devel
%dir %{_includedir}/srchilite
%{_libdir}/source-highlight*_dll.a
%{_libdir}/pkgconfig/source-highlight.pc
%{_includedir}/srchilite/*.h

%changelog
* Fri Nov 01 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.1.9-2
- fix a echo issue

* Wed Oct 30 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.1.9-1
- first release
