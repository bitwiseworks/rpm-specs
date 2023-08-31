%if !0%{?os2_version}
%bcond_without check
%else
%bcond_with check
%endif

Name:           libarchive
Version:        3.7.1
Release:        1%{?dist}
Summary:        A library for handling streaming archive formats

License:        BSD 2-Clause License AND BSD 2-clause NetBSD License BSD 2-Clause License
URL:            https://www.libarchive.org/
%if !0%{?os2_version}
Source0:        https://libarchive.org/downloads/%{name}-%{version}.tar.gz
%else
Vendor: bww bitwise works GmbH
%scm_source     github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2
%endif

BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  bison
BuildRequires:  bzip2-devel
%if !0%{?os2_version}
BuildRequires:  e2fsprogs-devel
%endif
BuildRequires:  gcc
%if !0%{?os2_version}
BuildRequires:  libacl-devel
BuildRequires:  libattr-devel
%endif
BuildRequires:  libtool
BuildRequires:  libxml2-devel
BuildRequires:  libzstd-devel
%if !0%{?os2_version}
BuildRequires:  lz4-devel
%else
BuildRequires:  cmake
%endif
# According to libarchive maintainer, linking against liblzo violates
# LZO license.
# See https://github.com/libarchive/libarchive/releases/tag/v3.3.0
#BuildRequires:  lzo-devel
BuildRequires:  openssl-devel
%if !0%{?os2_version}
BuildRequires:  sharutils
%endif
BuildRequires:  xz-devel
BuildRequires:  zlib-devel
BuildRequires: make

# When configured against OpenSSL 1.1, the RIPEMD-160 support was not detected,
# so it was not compiled in previously. With OpenSSL 3.0, it's now detected as
# being available, but it only actually works when the legacy provider is
# loaded, which breaks the RIPEMD-160 test. This patch disables the RIPEMD-160
# support explicitly.
%if !0%{?os2_version}
Patch0001: 0001-Drop-rmd160-from-OpenSSL.patch
%endif

%description
Libarchive is a programming library that can create and read several different
streaming archive formats, including most popular tar variants, several cpio
formats, and both BSD and GNU ar variants. It can also write shar archives and
read ISO9660 CDROM images and ZIP archives.


%package devel
Summary:        Development files for %{name}
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package -n bsdtar
Summary:        Manipulate tape archives
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description -n bsdtar
The bsdtar package contains standalone bsdtar utility split off regular
libarchive packages.


%package -n bsdcpio
Summary:        Copy files to and from archives
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description -n bsdcpio
The bsdcpio package contains standalone bsdcpio utility split off regular
libarchive packages.


%package -n bsdcat
Summary:        Expand files to standard output
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description -n bsdcat
The bsdcat program typically takes a filename as an argument or reads standard
input when used in a pipe.  In both cases decompressed data it written to
standard output.

%package -n bsdunzip
Summary:        Extract files from a ZIP archive
%if !0%{?os2_version}
Requires:       %{name}%{?_isa} = %{version}-%{release}
%else
Requires:       %{name} = %{version}-%{release}
%endif

%description -n bsdunzip
The bsdunzip package contains standalone bsdunzip utility split off regular
libarchive packages. It is designed to provide an interface compatible with Info-ZIP's.


%if 0%{?os2_version}
%debug_package
%endif


%prep
%if !0%{?os2_version}
%autosetup -p1
%else
%scm_setup
%endif

%build
%if !0%{?os2_version}
autoreconf -ifv
%configure --disable-static LT_SYS_LIBRARY_PATH=%_libdir
%make_build
%else
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
export VENDOR="%{vendor}"
%cmake
%cmake_build
%endif


%install
%if !0%{?os2_version}
%make_install
%else
%cmake_install
rm -f $RPM_BUILD_ROOT%{_libdir}/archive.a
%endif
find $RPM_BUILD_ROOT -name '*.la' -exec rm -f {} ';'

# rhbz#1294252
replace ()
{
    filename=$1
    file=`basename "$filename"`
    binary=${file%%.*}
    pattern=${binary##bsd}

    awk '
        # replace the topic
        /^.Dt ${pattern^^} 1/ {
            print ".Dt ${binary^^} 1";
            next;
        }
        # replace the first occurence of \"$pattern\" by \"$binary\"
        !stop && /^.Nm $pattern/ {
            print ".Nm $binary" ;
            stop = 1 ;
            next;
        }
        # print remaining lines
        1;
    ' "$filename" > "$filename.new"
    mv "$filename".new "$filename"
}

for manpage in bsdtar.1 bsdcpio.1
do
    installed_manpage=`find "$RPM_BUILD_ROOT" -name "$manpage"`
    replace "$installed_manpage"
done


%check
%if %{with check}
logfiles ()
{
    find -name '*_test.log' -or -name test-suite.log
}

tempdirs ()
{
    cat `logfiles` \
        | awk "match(\$0, /[^[:space:]]*`date -I`[^[:space:]]*/) { print substr(\$0, RSTART, RLENGTH); }" \
        | sort | uniq
}

cat_logs ()
{
    for i in `logfiles`
    do
        echo "=== $i ==="
        cat "$i"
    done
}

run_testsuite ()
{
    rc=0
    %make_build check -j1 || {
        # error happened - try to extract in koji as much info as possible
        cat_logs

        for i in `tempdirs`; do
            if test -d "$i" ; then
                find $i -printf "%p\n    ~> a: %a\n    ~> c: %c\n    ~> t: %t\n    ~> %s B\n"
                cat $i/*.log
            fi
        done
        return 1
    }
    cat_logs
}

# On a ppc/ppc64 is some race condition causing 'make check' fail on ppc
# when both 32 and 64 builds are done in parallel on the same machine in
# koji.  Try to run once again if failed.
%ifarch ppc
run_testsuite || run_testsuite
%else
run_testsuite
%endif
%endif


%files
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%if !0%{?os2_version}
%{_libdir}/libarchive.so.13*
%else
%{_libdir}/archiv*.dll
%endif
%{_mandir}/*/cpio.*
%{_mandir}/*/mtree.*
%{_mandir}/*/tar.*

%files devel
%{_includedir}/*.h
%{_mandir}/*/archive*
%{_mandir}/*/libarchive*
%if !0%{?os2_version}
%{_libdir}/libarchive.so
%else
%{_libdir}/*_dll.a
%endif
%{_libdir}/pkgconfig/libarchive.pc

%files -n bsdtar
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%if !0%{?os2_version}
%{_bindir}/bsdtar
%else
%{_bindir}/bsdtar.exe
%endif
%{_mandir}/*/bsdtar*

%files -n bsdcpio
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%if !0%{?os2_version}
%{_bindir}/bsdcpio
%else
%{_bindir}/bsdcpio.exe
%endif
%{_mandir}/*/bsdcpio*

%files -n bsdcat
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%if !0%{?os2_version}
%{_bindir}/bsdcat
%else
%{_bindir}/bsdcat.exe
%endif
%{_mandir}/*/bsdcat*

%files -n bsdunzip
%{!?_licensedir:%global license %%doc}
%license COPYING
%doc NEWS README.md
%if !0%{?os2_version}
%{_bindir}/bsdunzip
%else
%{_bindir}/bsdunzip.exe
%endif
%{_mandir}/*/bsdunzip*


%changelog
* Wed Aug 30 2023 Silvan Scherrer <silvan.scherrer@aroa.ch> - 3.7.1-1
- First RPM for OS/2 and OS/2 based systems
