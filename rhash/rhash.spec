Name:           rhash
Version:        1.4.5
Release:        1%{?dist}
Summary:        Great utility for computing hash sums

License:        MIT
URL:            https://github.com/rhash/RHash
%if !0%{?os2_version}
Source0:        https://github.com/rhash/RHash/archive/v%{version}/%{name}-%{version}.tar.gz
%else
Vendor:         bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 v%{version}-os2
%endif

BuildRequires: make
BuildRequires:  gcc

%description
RHash is a console utility for calculation  and verification of magnet links
and a wide range of hash sums like  CRC32,  MD4, MD5,  SHA1, SHA256, SHA512,
SHA3,   AICH,  ED2K,  Tiger,  DC++ TTH,  BitTorrent BTIH,   GOST R 34.11-94,
RIPEMD-160, HAS-160, EDON-R, Whirlpool and Snefru.

Hash sums are used to  ensure and verify integrity  of large volumes of data
for a long-term storing or transferring.

Features:
 * Output in a predefined (SFV, BSD-like) or a user-defined format.
 * Can calculate Magnet links.
 * Updating hash files (adding hash sums of files missing in the hash file).
 * Calculates several hash sums in one pass
 * Ability to process directories recursively.
 * Portability: the program works the same on Linux, *BSD or Windows.


%package        devel
Summary:        Development files for lib%{name}
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description    devel
LibRHash is a professional,  portable,  thread-safe  C library for computing
a wide variety of hash sums, such as  CRC32, MD4, MD5, SHA1, SHA256, SHA512,
SHA3,   AICH,  ED2K,  Tiger,  DC++ TTH,  BitTorrent BTIH,   GOST R 34.11-94,
RIPEMD-160, HAS-160, EDON-R, Whirlpool and Snefru.
Hash sums are used  to ensure and verify integrity of  large volumes of data
for a long-term storing or transferring.

Features:
 * Small and easy to learn interface.
 * Hi-level and Low-level API.
 * Allows calculating of several hash functions simultaneously.
 * Portability: the library works on Linux, *BSD and Windows.

The %{name}-devel package contains libraries and header files for
developing applications that use lib%{name}.


%if 0%{?os2_version}
%debug_package
%endif


%prep
%if !0%{?os2_version}
%setup -q -n RHash-%{version}
%else
%scm_setup
%endif
sed -i -e '/^INSTALL_SHARED/s/644/755/' librhash/Makefile


%build
%if 0%{?os2_version}
export VENDOR="%{vendor}"
%endif
INSTALL_INCDIR=%{_includedir} ./configure --sysconfdir=%{_sysconfdir} --exec-prefix=%{_prefix} --mandir=%{_mandir} --libdir=%{_libdir}
%make_build OPTFLAGS="%{optflags}" OPTLDFLAGS="-g %{?__global_ldflags}" build


%install
%make_install
%if !0%{?os2_version}
make DESTDIR=%{buildroot} -C librhash install-so-link install-lib-headers
%else
make DESTDIR=%{buildroot} -C librhash install-lib-headers
%endif


%check
make test-shared


%files
%license COPYING
%doc ChangeLog README.md
%config(noreplace) %{_sysconfdir}/rhashrc
%{_bindir}/*
%if !0%{?os2_version}
%{_libdir}/*.so.1*
%else
%{_libdir}/*.dll
%endif
%{_mandir}/man1/*.1*

%files devel
%{_includedir}/*
%if !0%{?os2_version}
%{_libdir}/*.so
%else
%{_libdir}/*_dll.a
%endif


%changelog
* Fri Mar 14 2025 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.4.5-1
- first OS/2 rpm
