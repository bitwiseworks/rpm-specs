Summary: Timezone data
Name: tzdata
Version: 2025c
%define tzdata_version 2025c
%define tzcode_version 2025c
Release: 1%{?dist}
License: LicenseRef-Fedora-Public-Domain AND (GPL-2.0-only WITH ClassPath-exception-2.0)
URL: https://www.iana.org/time-zones
%if !0%{?os2_version}
Source0: ftp://ftp.iana.org/tz/releases/tzdata%{tzdata_version}.tar.gz
Source1: ftp://ftp.iana.org/tz/releases/tzcode%{tzcode_version}.tar.gz

Patch002: 0002-Fix-have-snprintf-error.patch
Patch003: 0003-continue-to-ship-posixrules.patch
%else
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires: make
BuildRequires: gcc
%if !0%{?os2_version}
BuildRequires: gawk, glibc, perl-interpreter
BuildRequires: java-25-devel
BuildRequires: glibc-common >= 2.5.90-7
Conflicts: glibc-common <= 2.3.2-63
%else
BuildRequires: gawk, perl
%endif
BuildArchitectures: noarch
ExcludeArch: i686

# Using '--with vanguard' will change the data format to the new vanguard form.
%bcond_with vanguard

%description
This package contains data files with rules for various timezones around
the world.

%if !0%{?os2_version}
%package java
Summary: Timezone data for Java
Source3: javazic-1.8-37392f2f5d59.tar.xz
Source4: ZoneTest.java
Patch100: 8051641.patch
Patch101: javazic-harden-links.patch

%description java
This package contains timezone information for use by Java runtimes.
%endif

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q -c -a 1

%patch -p1 -P 2
%if 0%{?rhel}
%patch -p1 -P 3
%endif
%else
%scm_setup
# we need to create zic first, as we don't use the one from glibc
make VERSION=%{version} ZFLAGS="-b fat" zic LDLIBS="-Zomf -Zexe -lcx -lintl"
%endif

# zic now defaults to "-b slim" to control data bloat.
# This can cause build issues for some packages.
# For now, build with ZFLAGS="-b fat" for backward compatibitliy.

# tzdata-2018g introduced 25:00 transition times.  This breaks OpenJDK.
# Use rearguard for java
mkdir rearguard
make VERSION=%{version} ZFLAGS="-b fat" tzdata%{version}-rearguard.tar.gz.t
mv tzdata%{version}-rearguard.tar.gz rearguard
%if !0%{?os2_version}
pushd rearguard
%else
cd rearguard
%endif
tar zxf tzdata%{version}-rearguard.tar.gz
%if !0%{?os2_version}
popd
%else
cd ..
%endif

%if 0%{?rhel}
# Use rearguard for rhel (overwrite default dataform)
tar zxf rearguard/tzdata%{version}-rearguard.tar.gz
%endif

%if !0%{?os2_version}
tar xf %{SOURCE3}
%patch -P 100
%patch -p1 -P 101
%endif

echo "%{name}%{tzdata_version}" >> VERSION

%build
# Run make to create the tzdata.zi file
rm tzdata.zi
%if %{with vanguard}
make VERSION=%{version} ZFLAGS="-b fat" DATAFORM=vanguard tzdata.zi
%elif 0%{?rhel}
make VERSION=%{version} ZFLAGS="-b fat" DATAFORM=rearguard tzdata.zi
%else
make tzdata.zi
%endif

FILES="africa antarctica asia australasia europe northamerica southamerica
       etcetera backward factory"

%if !0%{?os2_version}
mkdir zoneinfo/{,posix,right}
%else
mkdir zoneinfo
mkdir zoneinfo/posix
mkdir zoneinfo/right
%endif
zic -b fat -y ./yearistype -d zoneinfo -L /dev/null -p America/New_York $FILES
zic -b fat -y ./yearistype -d zoneinfo/posix -L /dev/null $FILES
zic -b fat -y ./yearistype -d zoneinfo/right -L leapseconds $FILES

# grep -v tz-art.htm tz-link.htm > tz-link.html

%if !0%{?os2_version}
# tzdata-2018g introduced 25:00 which breaks java - use the rearguard files for java
JAVA_FILES="rearguard/africa rearguard/antarctica rearguard/asia \
      rearguard/australasia rearguard/europe rearguard/northamerica \
      rearguard/southamerica rearguard/etcetera \
      rearguard/backward"

# Java 8 tzdata
pushd javazic-1.8
javac -source 1.8 -target 1.8 -classpath . `find . -name \*.java`
popd

java -classpath javazic-1.8 build.tools.tzdb.TzdbZoneRulesCompiler \
    -srcdir . -dstfile tzdb.dat \
    -verbose \
    $JAVA_FILES javazic-1.8/tzdata_jdk/gmt javazic-1.8/tzdata_jdk/jdk11_backward
%endif

%install
rm -fr $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}
cp -prd zoneinfo $RPM_BUILD_ROOT%{_datadir}
install -p -m 644 zone.tab zone1970.tab iso3166.tab leap-seconds.list leapseconds tzdata.zi $RPM_BUILD_ROOT%{_datadir}/zoneinfo
%if !0%{?os2_version}
mkdir -p $RPM_BUILD_ROOT%{_datadir}/javazi-1.8
install -p -m 644 tzdb.dat $RPM_BUILD_ROOT%{_datadir}/javazi-1.8/
%endif

%check
echo ============TESTING===============
%if !0%{?os2_version}
/usr/bin/env LANG=C make -k VALIDATE=':' check && true
%else
/@unixroot/usr/bin/env LANG=C make -k VALIDATE=':' check LDLIBS="-Zomf -Zexe -lcx -lintl" && true
%endif

%if !0%{?os2_version}
# Create a custom JAVA_HOME, where we can replace tzdb.dat with the
# one just built, for testing.
system_java_home=$(dirname $(readlink -f $(which java)))/..
mkdir -p java_home
cp -Lr $system_java_home/* java_home/.
for tzdb in $(find java_home -name tzdb.dat) ; do
    rm $tzdb
    cp $RPM_BUILD_ROOT%{_datadir}/javazi-1.8/tzdb.dat $tzdb
done
# Compile the smoke test and run it.
cp %{SOURCE4} .
javac ZoneTest.java
java_home/bin/java ZoneTest
%endif
echo ============END TESTING===========

%files
%{_datadir}/zoneinfo
%license LICENSE
%doc README
%doc theory.html
%doc tz-link.html
%doc tz-art.html

%if !0%{?os2_version}
%files java
%{_datadir}/javazi-1.8
%endif

%changelog
* Wed Feb 25 2026 Silvan Scherrer <silvan.scherrer@aroa.ch> - 2025c-1
- first OS/2 rpm
