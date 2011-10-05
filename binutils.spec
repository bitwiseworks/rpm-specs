#disable lxlite strip
%define __os_install_post	%{nil}

# rpmbuild parameters:
# --define "binutils_target arm-linux-gnu" to create arm-linux-gnu-binutils.
# --with debug: Build without optimizations and without splitting the debuginfo.
# --without testsuite: Do not run the testsuite.  Default is to run it.
# --with testsuite: Run the testsuite.  Default --with debug is not to run it.

%bcond_with testsuite

%if 0%{!?binutils_target:1}
%define binutils_target %{_target_platform}
%define isnative 1
%define enable_shared 1
%else
%define cross %{binutils_target}-
%define isnative 0
%define enable_shared 0
%endif

Summary: A GNU collection of binary utilities
Name: %{?cross}binutils%{?_with_debug:-debug}
Version: 2.21
Release: 1%{?dist}
License: GPLv3+
Group: Development/Tools
URL: http://sources.redhat.com/binutils
Source: binutils-2.21-os2-20101212.zip

%define gold_arches %ix86 x86_64

%ifarch %gold_arches
%define build_gold	both
%else
%define build_gold	no
%endif

%if 0%{?_with_debug:1}
# Define this if you want to skip the strip step and preserve debug info.
# Useful for testing.
%define __debug_install_post : > %{_builddir}/%{?buildsubdir}/debugfiles.list
%define debug_package %{nil}
%define run_testsuite 0%{?_with_testsuite:1}
%else
%define run_testsuite 0%{!?_without_testsuite:1}
%endif

#Buildroot: %(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
#BuildRequires: texinfo >= 4.0, gettext, flex, bison, zlib-devel

# Required for: ld-bootstrap/bootstrap.exp bootstrap with --static
# It should not be required for: ld-elf/elf.exp static {preinit,init,fini} array
%if %{run_testsuite}
#BuildRequires: dejagnu, zlib-static, glibc-static, sharutils
%endif

Conflicts: gcc-c++ < 4.0.0
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
%ifarch ia64
Obsoletes: gnupro <= 1117-1
%endif

# The higher of these two numbers determines the default ld.
%{!?ld_bfd_priority: %define ld_bfd_priority	50}
%{!?ld_gold_priority:%define ld_gold_priority	30}

%if "%{build_gold}" == "both"
#Requires(post): coreutils
#Requires(post): %{_sbindir}/alternatives
#Requires(preun): %{_sbindir}/alternatives
%endif

# On ARM EABI systems, we do want -gnueabi to be part of the
# target triple.
%ifnarch %{arm}
%define _gnu %{nil}
%endif

%description
Binutils is a collection of binary utilities, including ar (for
creating, modifying and extracting from archives), as (a family of GNU
assemblers), gprof (for displaying call graph profile data), ld (the
GNU linker), nm (for listing symbols from object files), objcopy (for
copying and translating object files), objdump (for displaying
information from object files), ranlib (for generating an index for
the contents of an archive), readelf (for displaying detailed
information about binary files), size (for listing the section sizes
of an object or archive file), strings (for listing printable strings
from files), strip (for discarding symbols), and addr2line (for
converting addresses to file and line).

%package devel
Summary: BFD and opcodes dynamic libraries and header files
Group: System Environment/Libraries
#Conflicts: binutils < 2.17.50.0.3-4
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info
Requires: zlib-devel

%description devel
This package contains the generic BFD and opcodes dynamic libraries and
associated header files.  Developers starting new projects are encouraged
to consider using libelf instead of BFD.

%package static
Summary: BFD and opcodes static libraries
Group: System Environment/Libraries
#Requires(post): /sbin/install-info
#Requires(preun): /sbin/install-info

%description static
This package contains BFD and opcodes static libraries.  Developers
starting new projects are strongly encouraged to consider using
libelf instead of BFD.

%prep
%setup -q -c

%build

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_usr}
cp -p -r "binutils/*" %{buildroot}%{_usr}

rm  %{buildroot}%{_libdir}/*.la
rm  %{buildroot}%{_usr}/readme.os2
rm  %{buildroot}%{_infodir}/dir

%clean
rm -rf %{buildroot}

%post

%preun

%files
%defattr(-,root,root,-)
%doc binutils/readme.os2
%{_bindir}/*
%{_usr}/i386-pc-os2-emx/*
%{_mandir}/man1/*
%{_infodir}/[^b]*info*
%{_infodir}/binutils*info*

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_infodir}/bfd*info*

%files static
%defattr(-,root,root,-)
%{_libdir}/*.a

%changelog
