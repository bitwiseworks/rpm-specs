%global openjadever 1.3.2
%global version_list "3.0-sgml 3.1-sgml 4.0-sgml 4.1-sgml 4.1.2-xml 4.2-sgml 4.3-sgml 4.4-sgml 4.5-sgml 4.2-xml 4.3-xml 4.4-xml 4.5-xml 4.2-rng 4.3-rng 4.4-rng 4.5-rng 4.2-xsd 4.3-xsd 4.4-xsd 4.5-xsd"
%global catalog_list "3.0-sgml 3.1-sgml 4.0-sgml 4.1-sgml 4.1.2-xml 4.2-sgml 4.3-sgml 4.4-sgml 4.5-sgml 4.2-xml 4.3-xml 4.4-xml 4.5-xml"
%{!?_pkgdocdir: %global _pkgdocdir %{_docdir}/%{name}-%{version}}

Name: docbook-dtds
Version: 1.0
Release: 1%{?dist}
Group: Applications/Text

Summary: SGML and XML document type definitions for DocBook

License: Copyright only
URL: http://www.oasis-open.org/docbook/

Obsoletes: docbook-dtd30-sgml < %{version}-%{release}
Obsoletes: docbook-dtd31-sgml < %{version}-%{release}
Obsoletes: docbook-dtd40-sgml < %{version}-%{release}
Obsoletes: docbook-dtd41-sgml < %{version}-%{release}
Obsoletes: docbook-dtd412-xml < %{version}-%{release}
Provides: docbook-dtd-xml = %{version}-%{release}
Provides: docbook-dtd-sgml = %{version}-%{release}
Provides: docbook-dtd30-sgml = %{version}-%{release}
Provides: docbook-dtd31-sgml = %{version}-%{release}
Provides: docbook-dtd40-sgml = %{version}-%{release}
Provides: docbook-dtd41-sgml = %{version}-%{release}
Provides: docbook-dtd412-xml = %{version}-%{release}
Provides: docbook-dtd42-sgml = %{version}-%{release}
Provides: docbook-dtd42-xml = %{version}-%{release}
Provides: docbook-dtd43-sgml = %{version}-%{release}
Provides: docbook-dtd43-xml = %{version}-%{release}
Provides: docbook-dtd44-sgml = %{version}-%{release}
Provides: docbook-dtd44-xml = %{version}-%{release}
Provides: docbook-dtd45-sgml = %{version}-%{release}
Provides: docbook-dtd45-xml = %{version}-%{release}

Requires(post): /@unixroot/usr/bin/xmlcatalog.exe
Requires(postun): /@unixroot/usr/bin/xmlcatalog.exe
Requires(post): /@unixroot/usr/bin/chmod.exe
Requires(post): sed
Requires(postun): sed
Requires: sgml-common
Requires: xml-common

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildArch: noarch
Source0: http://www.oasis-open.org/docbook/sgml/3.0/docbk30.zip
Source1: http://www.oasis-open.org/docbook/sgml/3.1/docbk31.zip
Source2: http://www.oasis-open.org/docbook/sgml/4.0/docbk40.zip
Source3: http://www.oasis-open.org/docbook/sgml/4.1/docbk41.zip
Source4: http://www.oasis-open.org/docbook/xml/4.1.2/docbkx412.zip
Source5: http://www.oasis-open.org/docbook/sgml/4.2/docbook-4.2.zip
Source6: http://www.oasis-open.org/docbook/xml/4.2/docbook-xml-4.2.zip
Source7: http://www.docbook.org/sgml/4.3/docbook-4.3.zip
Source8: http://www.docbook.org/xml/4.3/docbook-xml-4.3.zip
Source9: http://www.docbook.org/sgml/4.4/docbook-4.4.zip
Source10: http://www.docbook.org/xml/4.4/docbook-xml-4.4.zip
Source11: http://www.docbook.org/sgml/4.5/docbook-4.5.zip
Source12: http://www.docbook.org/xml/4.5/docbook-xml-4.5.zip
Source13: http://www.docbook.org/rng/4.2/docbook-rng-4.2.zip
Source14: http://www.docbook.org/rng/4.3/docbook-rng-4.3.zip
Source15: http://www.docbook.org/rng/4.4/docbook-rng-4.4.zip
#compressed from http://www.docbook.org/rng/4.5/ upstream archive unavailable
Source16: docbook-rng-4.5.zip
Source17: http://www.docbook.org/xsd/4.2/docbook-xsd-4.2.zip
Source18: http://www.docbook.org/xsd/4.3/docbook-xsd-4.3.zip
Source19: http://www.docbook.org/xsd/4.4/docbook-xsd-4.4.zip
#compressed from http://www.docbook.org/xsd/4.5/ upstream archive unavailable
Source20: docbook-xsd-4.5.zip
#fix old catalog files
Patch0: docbook-dtd30-sgml-1.0.catalog.patch
Patch1: docbook-dtd31-sgml-1.0.catalog.patch
Patch2: docbook-dtd40-sgml-1.0.catalog.patch
Patch3: docbook-dtd41-sgml-1.0.catalog.patch
Patch4: docbook-dtd42-sgml-1.0.catalog.patch
#fix euro sign in 4.2 dtds
Patch5: docbook-4.2-euro.patch
#Fix ISO entities in 4.3/4.4/4.5 SGML
Patch6: docbook-dtds-ents.patch
#Use system rewrite for web URL's in sgml catalogs to prevent reading from the network(#478680)
Patch7: docbook-sgml-systemrewrite.patch
#use XML at the end of public identificators of XML 4.1.2 ISO entities
Patch8: docbook-dtd412-entities.patch
BuildRequires: unzip

%description
The DocBook Document Type Definition (DTD) describes the syntax of
technical documentation texts (articles, books and manual pages).
This syntax is XML-compliant and is developed by the OASIS consortium.
This package contains SGML and XML versions of the DocBook DTD.


%prep
%setup -c -T
eval mkdir %{version_list}
# DocBook V3.0
cd 3.0-sgml
unzip %{SOURCE0}
%patch0 -p0 -b docbook.cat
cd ..

# DocBook V3.1
cd 3.1-sgml
unzip %{SOURCE1}
%patch1 -p0 -b docbook.cat
cd ..

# DocBook V4.0
cd 4.0-sgml
unzip %{SOURCE2}
%patch2 -p0 -b docbook.cat
cd ..

# DocBook V4.1
cd 4.1-sgml
unzip %{SOURCE3}
%patch3 -p0 -b docbook.cat
cd ..

# DocBook XML V4.1.2
cd 4.1.2-xml
unzip %{SOURCE4}
cd ..

# DocBook V4.2
cd 4.2-sgml
unzip %{SOURCE5}
%patch4 -p0 -b docbook.cat
cd ..

# DocBook XML V4.2
cd 4.2-xml
unzip %{SOURCE6}
cd ..

# DocBook V4.3
cd 4.3-sgml
unzip %{SOURCE7}
cd ..

# DocBook XML V4.3
cd 4.3-xml
unzip %{SOURCE8}
cd ..

# DocBook V4.4
cd 4.4-sgml
unzip %{SOURCE9}
cd ..

# DocBook XML V4.4
cd 4.4-xml
unzip %{SOURCE10}
cd ..

# DocBook v4.5
cd 4.5-sgml
unzip %{SOURCE11}
cd ..

# DocBook XML v4.5
cd 4.5-xml
unzip %{SOURCE12}
cd ..

# Docbook RNG v4.2
cd 4.2-rng
unzip %{SOURCE13}
cd ..

# Docbook RNG v4.3
cd 4.3-rng
unzip %{SOURCE14}
cd ..

# Docbook RNG v4.4
cd 4.4-rng
unzip %{SOURCE15}
cd ..

# Docbook RNG v4.5
cd 4.5-rng
unzip %{SOURCE16}
cd ..

# Docbook XSD v4.2
cd 4.2-xsd
unzip %{SOURCE17}
cd ..

# Docbook XSD v4.3
cd 4.3-xsd
unzip %{SOURCE18}
cd ..

# Docbook XSD v4.4
cd 4.4-xsd
unzip %{SOURCE19}
cd ..

# Docbook XSD v4.5
cd 4.5-xsd
unzip %{SOURCE20}
cd ..

# Fix &euro; in SGML.
%patch5 -p1

# Fix ISO entities in 4.3/4.4/4.5 SGML
%patch6 -p1

# Rewrite SYSTEM to use local catalog instead web ones (#478680)
%patch7 -p1

# Add XML to the end of public identificators of 4.1.2 XML entities
%patch8 -p1

# Increase NAMELEN (bug #36058, bug #159382).
sed -e's,\(NAMELEN\s\+\)44\(\s\*\)\?,\1256,' -i.namelen */docbook.dcl

# fix of \r\n issue from rpmlint
sed -i 's/\r//' */*.txt


if [ `id -u` -eq 0 ]; then
#  chown -R root:root .
  chmod -R a+rX,g-w,o-w .
fi


%build


%install
rm -rf $RPM_BUILD_ROOT

# Symlinks
mkdir -p $RPM_BUILD_ROOT/@unixroot/etc/sgml
for fmt in sgml xml; do
  ln -s $fmt-docbook-4.5.cat \
     $RPM_BUILD_ROOT/@unixroot/etc/sgml/$fmt-docbook.cat
done

eval set %{version_list}
for dir
do
  cd $dir
  fmt=${dir#*-} ver=${dir%%-*}
  case $fmt in
    sgml)   DESTDIR=$RPM_BUILD_ROOT/@unixroot/usr/share/sgml/docbook/$fmt-dtd-$ver ;;
    xml)    DESTDIR=$RPM_BUILD_ROOT/@unixroot/usr/share/sgml/docbook/$fmt-dtd-$ver ;;
    rng)    DESTDIR=$RPM_BUILD_ROOT/@unixroot/usr/share/sgml/docbook/$fmt-$ver ;;
    xsd)    DESTDIR=$RPM_BUILD_ROOT/@unixroot/usr/share/sgml/docbook/$fmt-$ver ;;
  esac
  case $fmt in
    sgml)   mkdir -p $DESTDIR ; install *.dcl $DESTDIR ;;
    xml)    mkdir -p $DESTDIR/ent ; install ent/* $DESTDIR/ent ;;
    rng)    mkdir -p $DESTDIR ; install *.r* $DESTDIR ;;
    xsd)    mkdir -p $DESTDIR ; install *.xsd $DESTDIR;;
  esac
  cd ..
done

eval set %{catalog_list}
for dir
do
  cd $dir
  fmt=${dir#*-} ver=${dir%%-*}
  DESTDIR=$RPM_BUILD_ROOT/@unixroot/usr/share/sgml/docbook/$fmt-dtd-$ver
  install *.dtd *.mod $DESTDIR
  install docbook.cat $DESTDIR/catalog
  cd ..
  # File for %%ghost
  touch $RPM_BUILD_ROOT/@unixroot/etc/sgml/$fmt-docbook-$ver.cat
done

#workaround the missing support for --parents hack in rpm 4.11+
mkdir -p $RPM_BUILD_ROOT%{_pkgdocdir}
for i in */*.txt */ChangeLog */README
do
  cp -pr --parents $i $RPM_BUILD_ROOT%{_pkgdocdir}
done

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (0644,root,root,0755)
#in upstream tarballs there is a lot of files with 0755 permissions
#but they don't need to be, 0644 is enough for every file in tarball
%{_pkgdocdir}
/@unixroot/usr/share/sgml/docbook/*ml-dtd-*
/@unixroot/usr/share/sgml/docbook/rng-*
/@unixroot/usr/share/sgml/docbook/xsd-*
%config(noreplace) /@unixroot/etc/sgml/*ml-docbook.cat
%ghost %config(noreplace) /@unixroot/etc/sgml/*ml-docbook-*.cat

%post
catcmd='/@unixroot/usr/bin/xmlcatalog --noout'
xmlcatalog=/@unixroot/usr/share/sgml/docbook/xmlcatalog

## Clean up pre-docbook-dtds mess caused by broken trigger.
for v in 3.0 3.1 4.0 4.1 4.2
do
  if [ -f /@unixroot/etc/sgml/sgml-docbook-$v.cat ]
  then
    $catcmd --sgml --del /@unixroot/etc/sgml/sgml-docbook-$v.cat \
      /@unixroot/usr/share/sgml/openjade-1.3.1/catalog 2>/dev/null
  fi
done

# The STYLESHEETS/catalog command is for the case in which the style sheets
# were installed after another DTD but before this DTD
for STYLESHEETS in /@unixroot/usr/share/sgml/docbook/dsssl-stylesheets-*; do : ; done
case $STYLESHEETS in
  *-"*") STYLESHEETS= ;;
esac
eval set %{catalog_list}
for dir
do
  fmt=${dir#*-} ver=${dir%%-*}
  sgmldir=/@unixroot/usr/share/sgml/docbook/$fmt-dtd-$ver
  ## SGML catalog
  # Update the centralized catalog corresponding to this version of the DTD
  for cat_dir in /@unixroot/usr/share/sgml/sgml-iso-entities-8879.1986 $sgmldir $STYLESHEETS; do
    $catcmd --sgml --add /@unixroot/etc/sgml/$fmt-docbook-$ver.cat $cat_dir/catalog
  done
  ## XML catalog
  if [ $fmt = xml -a -w $xmlcatalog ]; then
    while read f desc; do
      case $ver in 4.[45]) f=`echo $f | sed 's/-//'` ;; esac
      $catcmd --add public "$desc" $sgmldir/$f $xmlcatalog
    done <<ENDENT
      ent/iso-pub.ent	ISO 8879:1986//ENTITIES Publishing//EN
      ent/iso-grk1.ent	ISO 8879:1986//ENTITIES Greek Letters//EN
      dbpoolx.mod	-//OASIS//ELEMENTS DocBook XML Information Pool V$ver//EN
      ent/iso-box.ent	ISO 8879:1986//ENTITIES Box and Line Drawing//EN
      docbookx.dtd	-//OASIS//DTD DocBook XML V$ver//EN
      ent/iso-grk3.ent	ISO 8879:1986//ENTITIES Greek Symbols//EN
      ent/iso-amsn.ent	ISO 8879:1986//ENTITIES Added Math Symbols: Negated Relations//EN
      ent/iso-num.ent	ISO 8879:1986//ENTITIES Numeric and Special Graphic//EN
      dbcentx.mod	-//OASIS//ENTITIES DocBook XML Character Entities V$ver//EN
      ent/iso-grk4.ent	ISO 8879:1986//ENTITIES Alternative Greek Symbols//EN
      dbnotnx.mod	-//OASIS//ENTITIES DocBook XML Notations V$ver//EN
      ent/iso-dia.ent	ISO 8879:1986//ENTITIES Diacritical Marks//EN
      ent/iso-grk2.ent	ISO 8879:1986//ENTITIES Monotoniko Greek//EN
      dbgenent.mod	-//OASIS//ENTITIES DocBook XML Additional General Entities V$ver//EN
      dbhierx.mod	-//OASIS//ELEMENTS DocBook XML Document Hierarchy V$ver//EN
      ent/iso-amsa.ent	ISO 8879:1986//ENTITIES Added Math Symbols: Arrow Relations//EN
      ent/iso-amso.ent	ISO 8879:1986//ENTITIES Added Math Symbols: Ordinary//EN
      ent/iso-cyr1.ent	ISO 8879:1986//ENTITIES Russian Cyrillic//EN
      ent/iso-tech.ent	ISO 8879:1986//ENTITIES General Technical//EN
      ent/iso-amsc.ent	ISO 8879:1986//ENTITIES Added Math Symbols: Delimiters//EN
      soextblx.dtd	-//OASIS//DTD XML Exchange Table Model 19990315//EN
      calstblx.dtd	-//OASIS//DTD DocBook XML CALS Table Model V$ver//EN
      ent/iso-lat1.ent	ISO 8879:1986//ENTITIES Added Latin 1//EN
      ent/iso-amsb.ent	ISO 8879:1986//ENTITIES Added Math Symbols: Binary Operators//EN
      ent/iso-lat2.ent	ISO 8879:1986//ENTITIES Added Latin 2//EN
      ent/iso-amsr.ent	ISO 8879:1986//ENTITIES Added Math Symbols: Relations//EN
      ent/iso-cyr2.ent	ISO 8879:1986//ENTITIES Non-Russian Cyrillic//EN
ENDENT
    for f in System URI; do
      $catcmd --add rewrite$f "http://www.oasis-open.org/docbook/xml/$ver" \
	$sgmldir $xmlcatalog
    done
  fi
done

# Historic versions of this scriptlet contained the following comment:
# <quote>
# Fix up SGML super catalog so that there isn't an XML DTD before an
# SGML one.  We need to do this (*sigh*) because xmlcatalog messes up
# the order of the lines, and SGML tools don't like to see XML things
# they aren't expecting.
# </quote>
# But the code that followed just found the first XML DTD and the first
# SGML DTD, swappinmg these two lines if the XML one preceded.
# But that only ensures that there is an SGML DTD before all XML ones.
# No one complained, so either this was enough, or the buggy SGML tools
# are long dead, or their users do not use bugzilla.
# Anyway, the following code, introduced in 1.0-46, does better: it ensures
# that all XML DTDs are after all SGML ones, by moving them to the end.
sed -ni '
  /xml-docbook/ H
  /xml-docbook/ !p
  $ {
          g
          s/^\n//p
  }
  ' /@unixroot/etc/sgml/catalog

# Finally, make sure everything in /etc/sgml is readable!
/@unixroot/usr/bin/chmod a+r /@unixroot/etc/sgml/*

%postun
# remove entries only on removal of package
if [ "$1" = 0 ]; then
  catcmd='/@unixroot/usr/bin/xmlcatalog --noout'
  xmlcatalog=/@unixroot/usr/share/sgml/docbook/xmlcatalog
  entities="
ent/iso-pub.ent
ent/iso-grk1.ent
dbpoolx.mod
ent/iso-box.ent
docbookx.dtd
ent/iso-grk3.ent
ent/iso-amsn.ent
ent/iso-num.ent
dbcentx.mod
ent/iso-grk4.ent
dbnotnx.mod
ent/iso-dia.ent
ent/iso-grk2.ent
dbgenent.mod
dbhierx.mod
ent/iso-amsa.ent
ent/iso-amso.ent
ent/iso-cyr1.ent
ent/iso-tech.ent
ent/iso-amsc.ent
soextblx.dtd
calstblx.dtd
ent/iso-lat1.ent
ent/iso-amsb.ent
ent/iso-lat2.ent
ent/iso-amsr.ent
ent/iso-cyr2.ent
  "
  eval set %{catalog_list}
  for dir
  do
    fmt=${dir#*-} ver=${dir%%-*}
    sgmldir=/@unixroot/usr/share/sgml/docbook/$fmt-dtd-$ver
    ## SGML catalog
    # Update the centralized catalog corresponding to this version of the DTD
    $catcmd --sgml --del /@unixroot/etc/sgml/catalog /@unixroot/etc/sgml/$fmt-docbook-$ver.cat
    rm -f /@unixroot/etc/sgml/$fmt-docbook-$ver.cat
    ## XML catalog
    if [ $fmt = xml -a -w $xmlcatalog ]; then
      for f in $entities; do
        case $ver in 4.[45]) f=`echo $f | sed 's/-//'` ;; esac
        $catcmd --del $sgmldir/$f $xmlcatalog
      done
      $catcmd --del $sgmldir $xmlcatalog
    fi
  done

  # See the comment attached to this command in the %%post scriptlet.
  sed -ni '
  /xml-docbook/ H
  /xml-docbook/ !p
  $ {
          g
          s/^\n//p
  }
    ' /@unixroot/etc/sgml/catalog
fi

%triggerin -- openjade >= %{openjadever}
eval set %{catalog_list}
for dir
do
  fmt=${dir#*-} ver=${dir%%-*}
  /@unixroot/usr/bin/xmlcatalog --sgml --noout --add /@unixroot/etc/sgml/$fmt-docbook-$ver.cat \
    /@unixroot/usr/share/sgml/openjade-%{openjadever}/catalog
done

%triggerun -- openjade >= %{openjadever}
[ $2 = 0 ] || exit 0
eval set %{catalog_list}
for dir
do
  fmt=${dir#*-} ver=${dir%%-*}
  /@unixroot/usr/bin/xmlcatalog --sgml --noout --del /@unixroot/etc/sgml/$fmt-docbook-$ver.cat \
    /@unixroot/usr/share/sgml/openjade-%{openjadever}/catalog
done

%changelog
* Thu May 04 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.0-1
- initial port

