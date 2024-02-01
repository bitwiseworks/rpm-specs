Name:		libssh2
Version:	1.11.0
Release:	1%{?dist}
Summary:	A library implementing the SSH2 protocol
License:	BSD-3-Clause
URL:		https://www.libssh2.org/
%if !0%{?os2_version}
Source0:	https://libssh2.org/download/libssh2-%{version}.tar.gz
Source1:	https://libssh2.org/download/libssh2-%{version}.tar.gz.asc
# Daniel Stenberg's GPG keys; linked from https://daniel.haxx.se/address.html
Source2:	https://daniel.haxx.se/mykey.asc
Patch1:		libssh2-1.11.0-strict-modes.patch
Patch2:		libssh2-1.11.0-ssh-rsa-test.patch
%else
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
Vendor:         bww bitwise works GmbH
%endif

BuildRequires:	coreutils
BuildRequires:	findutils
BuildRequires:	gcc
%if !0%{?os2_version}
BuildRequires:	gnupg2
%endif
BuildRequires:	make
BuildRequires:	openssl-devel > 1:1.0.2
BuildRequires:	pkgconfig
BuildRequires:	sed
BuildRequires:	zlib-devel
%if !0%{?os2_version}
BuildRequires:	/usr/bin/man
%else
BuildRequires:	/@unixroot/usr/bin/man.exe
%endif

# Test suite requirements
# Full groff (not just groff-base) needed for the mansyntax check
BuildRequires:	groff
# We run the OpenSSH server and try to connect to it
BuildRequires:	openssh-server
# Need a valid locale to run the mansyntax check
%if 0%{?fedora} > 23 || 0%{?rhel} > 7
BuildRequires:	glibc-langpack-en
%endif

%description
libssh2 is a library implementing the SSH2 protocol as defined by
Internet Drafts: SECSH-TRANS(22), SECSH-USERAUTH(25),
SECSH-CONNECTION(23), SECSH-ARCH(20), SECSH-FILEXFER(06)*,
SECSH-DHGEX(04), and SECSH-NUMBERS(10).

%package	devel
Summary:	Development files for libssh2
%if !0%{?os2_version}
Requires:	%{name}%{?_isa} = %{version}-%{release}
%else
Requires:	%{name} = %{version}-%{release}
%endif
Requires:	pkgconfig

%description	devel
The libssh2-devel package contains libraries and header files for
developing applications that use libssh2.

%package	docs
Summary:	Documentation for libssh2
Requires:	%{name} = %{version}-%{release}
BuildArch:	noarch

%description	docs
The libssh2-docs package contains man pages and examples for
developing applications that use libssh2.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%{gpgverify} --keyring='%{SOURCE2}' --signature='%{SOURCE1}' --data='%{SOURCE0}'
%setup -q

# Group-writeable directories in the hierarchy above where we
# run the tests from can cause failures due to openssh's strict
# permissions checks. Adding this option helps the tests to run
# more reliably on a variety of build systems.
%patch -P 1

# In 8.8 OpenSSH disabled sha1 rsa-sha keys out of the box,
# so we need to re-enable them as a workaround for the test
# suite until upstream updates the tests.
# See: https://github.com/libssh2/libssh2/issues/630
%if 0%{?fedora} > 33 || 0%{?rhel} > 8
%patch -P 2
%endif

# Replace hard wired port number in the test suite to avoid collisions
# between 32-bit and 64-bit builds running on a single build-host
sed -i s/4711/47%{?__isa_bits}/ tests/{openssh_fixture.c,test_ssh{2.c,d.test}}
%else
%scm_setup
autoreconf -fvi
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
export VENDOR="%{vendor}"
# Set BUILDLEVEL to be embedded to all DLLs built with Libtool.
export LT_BUILDLEVEL="@#%{vendor}:%{version}-%{release}#@##1## `LANG=C date +'%%d %%b %%Y %%H:%%M:%%S'`     `uname -n`::::0::"
%endif
# Test suite fails to compile if we use --disable-static
# https://github.com/libssh2/libssh2/issues/1056
%configure \
%if 0%{?os2_version}
	--disable-rpath \
%endif
	--disable-silent-rules \
	--enable-shared \
	--disable-docker-tests
%{make_build}

%install
%{make_install} INSTALL="install -p"
find %{buildroot} -name '*.la' -delete

# Remove static library that we only built for testing
%if !0%{?os2_version}
rm -v %{buildroot}%{_libdir}/libssh2.a
%else
rm -v %{buildroot}%{_libdir}/ssh2.a
%endif

# Clean things up a bit for packaging
make -C example clean
find example/ -type f \
	'(' -name '*.am' -o -name '*.in' -o -name CMakeLists.txt ')' \
	-print -delete

# Remove redundant references to libdir in pkg-config file
sed -i	-e 's|-L%{_libdir} ||g' \
	-e 's|-L[$]{libdir} ||g' %{buildroot}%{_libdir}/pkgconfig/libssh2.pc

# Avoid multilib conflict on libssh2-devel
%if !0%{?os2_version}
mv -v example example.%{_arch}
%endif

%check
%if !0%{?os2_version}
LC_ALL=en_US.UTF-8 make -C tests check
%endif

%if !0%{?os2_version}
%ldconfig_scriptlets
%endif

%files
%license COPYING
%doc docs/AUTHORS README RELEASE-NOTES
%if !0%{?os2_version}
%{_libdir}/libssh2.so.1
%{_libdir}/libssh2.so.1.*
%else
%{_libdir}/ssh2*.dll
%endif

%files docs
%doc docs/BINDINGS.md docs/HACKING.md docs/TODO NEWS
%{_mandir}/man3/libssh2_*.3*

%files devel
%if !0%{?os2_version}
%doc example.%{_arch}/
%else
%doc example/
%endif
%{_includedir}/libssh2.h
%{_includedir}/libssh2_publickey.h
%{_includedir}/libssh2_sftp.h
%if !0%{?os2_version}
%{_libdir}/libssh2.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/libssh2.pc

%changelog
* Thu Feb 01 2024 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.11.0-1
- first OS/2 version
