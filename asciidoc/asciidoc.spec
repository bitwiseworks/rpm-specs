%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}

%global with_vim 0
%global with_latex 0
%global with_music 0

%if %{with_vim}
%global vimdir %{_datadir}/vim/vimfiles
%endif

Summary: Text based document generation
Name: asciidoc
Version: 8.6.10
Release: 1%{?dist}
# The python code does not specify a version.
# The javascript example code is GPLv2+.
License: GPL+ and GPLv2+

Vendor: bww bitwise works GmbH
URL: http://www.methods.co.nz/asciidoc/
%scm_source github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: python-devel
%if %{with_latex}
BuildRequires: dblatex
BuildRequires: texlive-dvipng-bin
%endif
#BuildRequires: graphviz
BuildRequires: libxslt
%if %{with_music}
BuildRequires: lilypond
%endif
BuildRequires: source-highlight
%if %{with_vim}
BuildRequires: vim-filesystem
%endif
#BuildRequires: symlinks


Requires: python >= 2.4
Requires: docbook-style-xsl
#Requires: graphviz
Requires: libxslt
Requires: source-highlight
%if %{with_vim}
Requires: vim-filesystem
%endif

BuildArch: noarch

%description
AsciiDoc is a text document format for writing short documents,
articles, books and UNIX man pages. AsciiDoc files can be translated
to HTML and DocBook markups using the asciidoc(1) command.

%package doc
Summary:  Additional documentation and examples for asciidoc
Requires: %{name} = %{version}-%{release}

%description doc
%{summary}.

%if %{with_latex}
%package latex
Summary:  Support for asciidoc latex output
Requires: %{name} = %{version}-%{release}
Requires: dblatex
Requires: texlive-dvipng-bin

%description latex
%{summary}.
%endif

%if %{with_music}
%package music
Summary:  Support for asciidoc music output
Requires: %{name} = %{version}-%{release}
Requires: lilypond

%description music
%{summary}.
%endif


%prep
%scm_setup
autoreconf -fvi

# Fix line endings on COPYRIGHT file
sed -i "s/\r//g" COPYRIGHT

# Convert README and dict files to utf-8
for file in README.asciidoc doc/*.dict examples/website/*.dict; do
    iconv -f ISO-8859-1 -t UTF-8 $file >$file.new && \
    touch -r $file $file.new && \
    mv $file.new $file
done

%build
%configure

%install
make install docs DESTDIR=%{buildroot}

install -dm 755 %{buildroot}%{_datadir}/asciidoc/
# real conf data goes to sysconfdir, rest to datadir; symlinks so asciidoc works
for d in dblatex docbook-xsl images javascripts stylesheets; do
    mv -v %{buildroot}%{_sysconfdir}/asciidoc/$d \
          %{buildroot}%{_datadir}/asciidoc/
    # absolute symlink into buildroot is intentional, see below
    ln -s %{_datadir}/%{name}/$d %{buildroot}%{_sysconfdir}/%{name}/
done

# Python API
install -Dpm 644 asciidocapi.py %{buildroot}%{python_sitelib}/asciidocapi.py

# Make it easier to %exclude these with both rpm < and >= 4.7
for file in %{buildroot}%{_bindir}/*.py %{buildroot}%{_sysconfdir}/asciidoc/filters/*/*.py; do
    touch ${file}c
    touch ${file}o
done

%if %{with_vim}
mkdir -p %{buildroot}%{vimdir}/{ftdetect,syntax}
for file in $(cd vim; find * -type f); do
    install -m 0644 vim/$file %{buildroot}%{vimdir}/$file
done
%endif

# Clean up no needed doc files
rm -f %{buildroot}/%{_docdir}/%{name}/INSTALL.txt

%check
export PATH="../;$PATH"
cd tests
rm asciidocapi.py
ln -s ../asciidocapi.py asciidocapi.py
python testasciidoc.py update
python testasciidoc.py run

%files
%doc BUGS.txt CHANGELOG.txt COPYING COPYRIGHT README.asciidoc
%doc %{_mandir}/man1/a2x.1*
%doc %{_mandir}/man1/asciidoc.1*
%config(noreplace) %{_sysconfdir}/asciidoc/
%{_bindir}/a2x
%{_bindir}/a2x.py
%{_bindir}/asciidoc
%{_bindir}/asciidoc.py
%{_datadir}/asciidoc/
%{python_sitelib}/asciidocapi.py*
%if %{with_vim}
%{vimdir}/ftdetect/asciidoc_filetype.vim
%{vimdir}/syntax/asciidoc.vim
%endif
%exclude %{_bindir}/*.pyc
%exclude %{_bindir}/*.pyo
%exclude %{_sysconfdir}/asciidoc/filters/*/*.pyc
%exclude %{_sysconfdir}/asciidoc/filters/*/*.pyo
%exclude %{_sysconfdir}/asciidoc/filters/latex
%exclude %{_sysconfdir}/asciidoc/filters/music


%files doc
%{_docdir}/%{name}
%exclude %{_docdir}/%{name}/COPYING
%exclude %{_docdir}/%{name}/COPYRIGHT
%exclude %{_docdir}/%{name}/README.asciidoc
%exclude %{_docdir}/%{name}/BUGS.txt
%exclude %{_docdir}/%{name}/CHANGELOG.txt

%if %{with_latex}
%files latex
%dir %{_sysconfdir}/asciidoc/filters/latex
%{_sysconfdir}/asciidoc/filters/latex/*.py
%{_sysconfdir}/asciidoc/filters/latex/*.conf
%endif

%if %{with_music}
%files music
%dir %{_sysconfdir}/asciidoc/filters/music
%{_sysconfdir}/asciidoc/filters/music/*.conf
%{_sysconfdir}/asciidoc/filters/music/*.py
%endif

%changelog
* Fri Nov 01 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 8.6.10-1
- initial port
