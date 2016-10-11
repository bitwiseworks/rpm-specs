#define svn_url     e:/trees/libpaper/trunk
%define svn_url     http://svn.netlabs.org/repos/ports/libpaper/trunk
%define svn_rev     1732

Name:		libpaper
Version:	1.1.24
Release:	1%{?dist}
Summary:	Library and tools for handling papersize
Group:		System Environment/Libraries
License:	GPLv2
URL:		http://packages.qa.debian.org/libp/libpaper.html
Vendor:		bww bitwise works GmbH
Source:		%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires:	libtool, gettext, gawk
BuildRequires:	autoconf
BuildRequires:	automake

%description
The paper library and accompanying files are intended to provide a 
simple way for applications to take actions based on a system- or 
user-specified paper size. This release is quite minimal, its purpose 
being to provide really basic functions (obtaining the system paper name 
and getting the height and width of a given kind of paper) that 
applications can immediately integrate.


%package devel
Summary:	Headers/Libraries for developing programs that use libpaper
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains headers and libraries that programmers will need 
to develop applications which use libpaper.


%debug_package


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

autoreconf -fiv


%build
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
%configure --disable-static

make %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rm $RPM_BUILD_ROOT%{_libdir}/*.la
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}
echo '# Simply write the paper name. See papersize(5) for possible values' > $RPM_BUILD_ROOT%{_sysconfdir}/papersize

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/libpaper.d
for i in cs da de es fr gl hu it ja nl pt_BR sv tr uk vi; do
	mkdir -p $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/;
	msgfmt debian/po/$i.po -o $RPM_BUILD_ROOT%{_datadir}/locale/$i/LC_MESSAGES/%{name}.mo;
done

%find_lang %{name}

%clean
rm -rf $RPM_BUILD_ROOT


#%post -p /sbin/ldconfig


#%postun -p /sbin/ldconfig


%files -f %{name}.lang
%doc COPYING ChangeLog README
%config(noreplace) %{_sysconfdir}/papersize
%{_bindir}/paperconf.exe
%{_libdir}/paper*.dll
%{_sbindir}/paperconfig
%{_mandir}/man1/*
%{_mandir}/man5/*
%{_mandir}/man8/*


%files devel
%{_includedir}/paper.h
%{_libdir}/paper*.a
%{_mandir}/man3/*


%changelog
* Tue Oct 11 2016 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.24-1
- initial version
