Summary: The GNU data compression program
Name: gzip
Version: 1.4
Release: 1%{?dist}
# info pages are under GFDL license
License: GPLv3+ and GFDL
Group: Applications/File
Source: http://ftp.gnu.org/gnu/gzip/gzip-%{version}.tar.gz

Patch0: gzip-1.3.12-openbsd-owl-tmp.patch
Patch1: gzip-1.3.5-zforce.patch
Patch2: gzip-1.3.9-stderr.patch
Patch3: gzip-1.3.10-zgreppipe.patch
Patch4: gzip-1.3.13-rsync.patch
Patch5: gzip-1.3.9-addsuffix.patch
Patch6: gzip-1.3.5-cve-2006-4338.patch
Patch7: gzip-1.3.13-cve-2006-4337.patch
Patch8: gzip-1.3.5-cve-2006-4337_len.patch
# Fixed in upstream code.
# http://thread.gmane.org/gmane.comp.gnu.gzip.bugs/378
Patch11: gzip-1.3.13-noemptysuffix.patch

Patch100: gzip-1.4-os2.diff

URL: http://www.gzip.org/
#Requires: /sbin/install-info
#Requires: mktemp less
#BuildRequires: texinfo
Buildroot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your system, because it is a
very commonly used data compression program.

%prep
%setup -q
%patch0 -p1 -b .owl-tmp~
%patch1 -p1 -b .zforce~
%patch2 -p1 -b .stderr~
%patch3 -p1 -b .nixi~
%patch4 -p1 -b .rsync~
%patch5 -p1 -b .addsuffix~
%patch6 -p1 -b .4338~
%patch7 -p1 -b .4337~
%patch8 -p1 -b .4337l~
%patch11 -p1 -b .noemptysuffix~

%patch100 -p1 -b .os2~

%build
export DEFS="NO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"
export LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zexe -Zargs-wild -Zargs-resp"
%configure \
        "--cache-file=%{_topdir}/cache/%{name}.cache"

make %{?smp_mflags}
#make gzip.info

%install
rm -rf ${RPM_BUILD_ROOT}
##makeinstall  bindir=${RPM_BUILD_ROOT}/usr/bin
make DESTDIR=${RPM_BUILD_ROOT} install

rm ${RPM_BUILD_ROOT}%{_libdir}/charset.alias

#mkdir -p ${RPM_BUILD_ROOT}%{_bindir}
cp ${RPM_BUILD_ROOT}%{_bindir}/gzip.exe ${RPM_BUILD_ROOT}%{_bindir}/gunzip.exe
cp ${RPM_BUILD_ROOT}%{_bindir}/gzip.exe ${RPM_BUILD_ROOT}%{_bindir}/uncomress.exe

#for i in  zcmp zegrep zforce zless znew gzexe zdiff zfgrep zgrep zmore ; do
#    mv ${RPM_BUILD_ROOT}/bin/$i ${RPM_BUILD_ROOT}%{_bindir}/$i
#done

gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/gzip.info*

# we don't ship it, so let's remove it from ${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
# uncompress is a part of ncompress package
rm -f ${RPM_BUILD_ROOT}/bin/uncompress

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
#if [ -f %{_infodir}/gzip.info* ]; then
#    /sbin/install-info %{_infodir}/gzip.info.gz %{_infodir}/dir || :
#fi

%preun
#if [ $1 = 0 ]; then
#    if [ -f %{_infodir}/gzip.info* ]; then
#        /sbin/install-info --delete %{_infodir}/gzip.info.gz %{_infodir}/dir || :
#    fi
#fi

%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog THANKS TODO
#/bin/*
%{_bindir}/*
%{_mandir}/*/*
%{_infodir}/gzip.info*

%changelog
