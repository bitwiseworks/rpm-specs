Name: pcre
Version: 8.12
Release: 1%{?dist}
Summary: Perl-compatible regular expression library
URL: http://www.pcre.org/
Source: ftp://ftp.csx.cam.ac.uk/pub/software/programming/pcre/%{name}-%{version}.tar.gz
License: BSD
Group: System Environment/Libraries

Patch0: pcre-os2.diff

BuildRoot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
# New libtool to get rid of rpath
#BuildRequires: autoconf, automake, libtool

%description
Perl-compatible regular expression library.
PCRE has its own native API, but a set of "wrapper" functions that are based on
the POSIX API are also supplied in the library libpcreposix. Note that this
just provides a POSIX calling interface to PCRE: the regular expressions
themselves still follow Perl syntax and semantics. The header file
for the POSIX-style functions is called pcreposix.h.

%package devel
Summary: Development files for %{name}
Group: Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
Development files (Headers, libraries for dynamic linking, etc) for %{name}.

%package static
Summary: Static library for %{name}
Group: Development/Libraries

%description static
Library for static linking for %{name}.

%prep
%setup -q
# Get rid of rpath
%patch0 -p1 -b .os2~

#libtoolize --copy --force && autoreconf
# One contributor's name is non-UTF-8
#for F in ChangeLog; do
#    iconv -f latin1 -t utf8 "$F" >"${F}.utf8"
#    touch --reference "$F" "${F}.utf8"
#    mv "${F}.utf8" "$F"
#done

%build
export CONFIG_SHELL="/bin/sh"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp" ; \
%configure \
        --disable-shared --enable-static \
        --enable-newline-is-any \
        "--cache-file=%{_topdir}/cache/%{name}.cache"

make %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

cp .libs/pcre_s.a $RPM_BUILD_ROOT%{_libdir}
cp pcre*.dll $RPM_BUILD_ROOT%{_libdir}

# libpcre.so.*() needed by grep during system start (bug #41104)
#mkdir -p $RPM_BUILD_ROOT/%{_lib}
#mv $RPM_BUILD_ROOT%{_libdir}/libpcre.so.* $RPM_BUILD_ROOT/%{_lib}/
#pushd $RPM_BUILD_ROOT%{_libdir}
#ln -fs ../../%{_lib}/libpcre.so.0 libpcre.so
#popd

# get rid of unneeded *.la files
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

# These are handled by %%doc in %%files
rm -rf $RPM_BUILD_ROOT%{_docdir}/pcre

#%check
#make check

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%{_libdir}/*.dll
%{_mandir}/man1/*
%{_bindir}/pcregrep.exe
%{_bindir}/pcretest.exe
%doc AUTHORS COPYING LICENCE NEWS README ChangeLog

%files devel
%defattr(-,root,root)
%{_libdir}/*.dll
%{_libdir}/*.a
%{_libdir}/pkgconfig/*
%{_includedir}/*.h
%{_mandir}/man3/*
%{_bindir}/pcre-config
%doc doc/*.txt doc/html
%doc HACKING

%files static
%defattr(-,root,root)
%{_libdir}/pcre_s.a
%doc COPYING LICENCE 

%changelog
