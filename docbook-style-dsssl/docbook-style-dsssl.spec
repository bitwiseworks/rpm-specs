Name: docbook-style-dsssl
Version: 1.79
Release: 1%{?dist}

Summary: Norman Walsh's modular stylesheets for DocBook

License: DMIT
URL: http://docbook.sourceforge.net/
BuildRequires: perl-generators
BuildRequires: make

Requires: docbook-dtds
%if !0%{?os2_version}
Requires: openjade
%endif
Requires: sgml-common
Requires(post): sgml-common
Requires(preun): sgml-common

BuildArch: noarch
Source0: http://prdownloads.sourceforge.net/docbook/docbook-dsssl-%{version}.tar.gz
Source1: %{name}.Makefile


%description
These DSSSL stylesheets allow to convert any DocBook document to another
printed (for example, RTF or PostScript) or online (for example, HTML) format.
They are highly customizable.

%prep
%setup -q -n docbook-dsssl-%{version}
cp %{SOURCE1} Makefile


%build

%install
DESTDIR=$RPM_BUILD_ROOT
make install BINDIR=$DESTDIR%{_bindir} DESTDIR=$DESTDIR%{_datadir}/sgml/docbook/dsssl-stylesheets-%{version} MANDIR=$DESTDIR%{_mandir}
cd ..
ln -s dsssl-stylesheets-%{version} $DESTDIR%{_datadir}/sgml/docbook/dsssl-stylesheets

%files
%doc BUGS README ChangeLog WhatsNew
%{_bindir}/collateindex.pl
%{_mandir}/man1/collateindex.pl.1*
%{_datadir}/sgml/docbook/dsssl-stylesheets-%{version}
%{_datadir}/sgml/docbook/dsssl-stylesheets


%post
for centralized in %{_sysconfdir}/sgml/*-docbook-*.cat
do
  %{_bindir}/install-catalog --add $centralized \
    %{_datadir}/sgml/docbook/dsssl-stylesheets-%{version}/catalog \
    > /dev/null 2>/dev/null
done


%preun
if [ "$1" = "0" ]; then
  for centralized in %{_sysconfdir}/sgml/*-docbook-*.cat
  do
    %{_bindir}/install-catalog --remove $centralized %{_datadir}/sgml/docbook/dsssl-stylesheets-%{version}/catalog > /dev/null 2>/dev/null
  done
fi
exit 0

%changelog
* Wed Mar 23 2022 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.79-1
- first OS/2 rpm
