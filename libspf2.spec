# NOTE THAT THE TEST SUITE IS CURRENTLY BROKEN
# USE rpmbuild --with checks TO SEE THIS FOR YOURSELF

# Each change to the spec requires a bump to version/release of both library and perlmod
%global library_version 1.2.9
%global library_release 0%{?dist}
%global perlmod_version 0.01
%global perlmod_release 0%{?dist}

# Set to 1 for a compat-libspf2 package
%global compat 0

# graphviz needed to build API docs, only available from Fedora 3, RHEL 4
%if 0%{?fedora} >= 3 || 0%{?rhel} >= 4
%global build_apidocs 1
%else
%global build_apidocs 0
%endif
# Fedora 10, RHEL 6 onwards support noarch subpackages
%if 0%{?fedora} > 9 || 0%{?rhel} >= 6
%global build_apidocs_noarch 1
%endif

# Use rpmbuild --with checks to try running the broken test suite (disabled by default)
%{!?_without_checks:	%{!?_with_checks: %global _without_checks --without-checks}}
%{?_with_checks:	%global enable_checks 1}
%{?_without_checks:	%global enable_checks 0}

# Macros that need defining for older distributions
%{!?perl_vendorarch: %global perl_vendorarch %(eval "`%{__perl} -V:installvendorarch`"; echo $installvendorarch)}
%{!?__id_u: %global __id_u %([ -x /bin/id ]&&echo /bin/id||([ -x /usr/bin/id ]&&echo /usr/bin/id||echo /bin/true)) -u}

%if %{compat}
Name:		compat-libspf2
%else
Name:		libspf2
%endif
Version:	%{library_version}
Release:	%{library_release}
Summary:	An implementation of the SPF specification
License:	BSD or LGPLv2+
Group:		System Environment/Libraries
Url:		http://www.libspf2.org/
Source0:	http://www.libspf2.org/spf/libspf2-%{version}.tar.gz

Patch1: libspf2-os2.diff

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%if %{build_apidocs}
# For API docs
BuildRequires:	doxygen, graphviz
%endif
# For perl bindings (Makefile.PL claims Mail::SPF is needed, but it isn't)
#BuildRequires:	perl(ExtUtils::MakeMaker)
# For perl test suite
#BuildRequires:	perl(Test::Pod), perl(String::Escape)
# POD Coverage is non-existent, causes test suite to fail
#BuildConflicts:	perl(Test::Pod::Coverage)
# Perl module fails the standard test suite
#BuildConflicts:	perl(Mail::SPF::Test)
%if %{compat}
Provides:	libspf2 = %{version}-%{release}
%endif

%description
libspf2 is an implementation of the SPF (Sender Policy Framework)
specification as found at:
http://www.ietf.org/internet-drafts/draft-mengwong-spf-00.txt
SPF allows email systems to check SPF DNS records and make sure that
an email is authorized by the administrator of the domain name that
it is coming from. This prevents email forgery, commonly used by
spammers, scammers, and email viruses/worms.

A lot of effort has been put into making it secure by design, and a
great deal of effort has been put into the regression tests.

%if ! %{compat}
%package devel
Summary:	Development tools needed to build programs that use libspf2
Group:		Development/Libraries
Version:	%{library_version}
Release:	%{library_release}
Requires:	%{name} = %{version}-%{release}

%description devel
The libspf2-devel package contains the header files and static
libraries necessary for developing programs using the libspf2 (Sender
Policy Framework) library.

If you want to develop programs that will look up and process SPF records,
you should install libspf2-devel.

%if %{build_apidocs}
API documentation is in the separate libspf2-apidocs package.

%package apidocs
Summary:	API documentation for the libspf2 library
Group:		Documentation
Version:	%{library_version}
Release:	%{library_release}
%{?build_apidocs_noarch:BuildArch: noarch}

%description apidocs
The libspf2-apidocs package contains the API documentation for creating
applications that use the libspf2 (Sender Policy Framework) library.
%endif

%package -n perl-Mail-SPF_XS
Summary:	An XS implementation of Mail::SPF
Group:		Development/Libraries
License:	GPL+ or Artistic
Version:	%{perlmod_version}
Release:	%{perlmod_release}
Requires:	perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description -n perl-Mail-SPF_XS
This is an interface to the C library libspf2 for the purpose of
testing. While it can be used as an SPF implementation, you can also
use Mail::SPF, which is a little more perlish.

%package progs
Summary:	Programs for making SPF queries using libspf2
Group:		Applications/Internet
Version:	%{library_version}
Release:	%{library_release}
Requires:	%{name} = %{version}-%{release}

#Requires(post): /usr/sbin/alternatives
#Requires(preun): /usr/sbin/alternatives
#Requires(postun): /usr/sbin/alternatives, /usr/bin/readlink

%description progs
Programs for making SPF queries and checking their results using libspf2.
%endif

%prep
%setup -q -n libspf2-%{version}
%patch001 -p1 -b .os2~

%build
# The configure script checks for the existence of __ns_get16 and uses the
# system-supplied version if found, otherwise one from src/libreplace.
# However, this function is marked GLIBC_PRIVATE in recent versions of glibc
# and shouldn't be called even if the configure script finds it. So we make
# sure that the configure script always uses the version in src/libreplace.
# This prevents us getting an unresolvable dependency in the built RPM.
ac_cv_func___ns_get16=no
export ac_cv_func___ns_get16

export CONFIG_SHELL="/bin/sh" ; \
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
export LIBS="-lurpo -lmmap -lpthread" ; \
%configure \
    --enable-shared --disable-static \
    "--cache-file=%{_topdir}/cache/%{name}.cache"

# Kill bogus RPATHs
%{__sed} -i 's|^sys_lib_dlsearch_path_spec="/lib /usr/lib|sys_lib_dlsearch_path_spec="/%{_lib} %{_libdir}|' libtool

%{__make} %{?_smp_mflags} CFLAGS="%{optflags} -fno-strict-aliasing"

%if %{build_apidocs}
# Generate API docs
%{__sed} -i -e 's/\(SHORT_NAMES[[:space:]]*=[[:space:]]*\)NO/\1YES/' Doxyfile
/usr/bin/doxygen
%endif

%install
#PERL_INSTALL_ROOT=$(%{__grep} DESTDIR perl/Makefile &> /dev/null && echo "" || echo %{buildroot}) 
%{__rm} -rf %{buildroot}
%{__make} \
	DESTDIR=%{buildroot} \
	INSTALLDIRS=vendor \
	INSTALL="%{__install} -p" \
	install

cp src/libspf2/.libs/spf2.a %{buildroot}%{_libdir}

# Clean up after impure perl installation
#/usr/bin/find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -exec %{__rm} {} ';'
#/usr/bin/find %{buildroot} -type f -name '*.bs' -a -size 0 -exec %{__rm} -f {} ';'
#/usr/bin/find %{buildroot} -depth -type d -exec /bin/rmdir {} 2>/dev/null ';'
#%{__chmod} -R u+w %{buildroot}/*

# Don't want statically-linked binaries
%{__rm} -f %{buildroot}%{_bindir}/spf*_static.exe

# Rename binaries that will be accessed via alternatives
%{__mv} -f %{buildroot}%{_bindir}/spfquery.exe	%{buildroot}%{_bindir}/spfquery_libspf2.exe
%{__mv} -f %{buildroot}%{_bindir}/spfd.exe	%{buildroot}%{_bindir}/spfd_libspf2.exe

# Remove files not needed for compat package
%if %{compat}
%{__rm} -rf %{buildroot}%{_bindir}
%{__rm} -rf %{buildroot}%{_includedir}/spf2
%{__rm} -rf %{buildroot}%{_libdir}/*.a
%{__rm} -rf %{buildroot}%{_libdir}/*.la
%{__rm} -rf %{buildroot}%{_libdir}/*.so
%{__rm} -rf %{buildroot}%{_mandir}/man3
%{__rm} -rf %{buildroot}%{perl_vendorarch}
%endif

#%check
#%if %{enable_checks}
#%{__make} -C tests check
#%endif
#LD_PRELOAD=$(pwd)/src/libspf2/.libs/libspf2.so %{__make} -C perl test

%clean
%{__rm} -rf %{buildroot}

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%if ! %{compat}
%post progs
/usr/sbin/alternatives --install %{_bindir}/spfquery spf %{_bindir}/spfquery.libspf2 20 \
	--slave %{_bindir}/spfd spf-daemon %{_bindir}/spfd.libspf2
exit 0

#%preun progs
#if [ $1 = 0 ]; then
#	/usr/sbin/alternatives --remove spf %{_bindir}/spfquery.libspf2
#fi
#exit 0

#%postun progs
#if [ "$1" -ge "1" ]; then
#	spf=`readlink /etc/alternatives/spf`
#	if [ "$spf" == "%{_bindir}/spfquery.libspf2" ]; then
#		/usr/sbin/alternatives --set spf %{_bindir}/spfquery.libspf2
#	fi
#fi
#exit 0

#%triggerpostun -- libspf2-progs <= 1.0.4-3
#/usr/sbin/alternatives --auto spf
%endif

%files
%defattr(-,root,root,-)
%{_libdir}/spf2.dll
%doc README INSTALL LICENSES TODO
#%doc docs/*.txt

%if ! %{compat}
%files devel
%defattr(-,root,root,-)
%{_includedir}/spf2/spf*.h
%{_libdir}/spf2.a
%{_libdir}/spf2.dll

%if %{build_apidocs}
%files apidocs
%defattr(-,root,root,-)
%doc doxygen/html
%endif

%files progs
%defattr(-,root,root,-)
%{_bindir}/spfd_libspf2.exe
%{_bindir}/spfquery_libspf2.exe
%{_bindir}/spftest.exe
%{_bindir}/spf_example.exe

#%files -n perl-Mail-SPF_XS
#%defattr(-,root,root,-)
#%{perl_vendorarch}/Mail/
#%{perl_vendorarch}/auto/Mail/
#%{_mandir}/man3/Mail::SPF_XS.3pm*
%endif

%changelog
