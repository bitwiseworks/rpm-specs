Summary: The GNU data compression program
Name: gzip
Version: 1.8
Release: 1%{?dist}
# info pages are under GFDL license
License: GPLv3+ and GFDL
Group: Applications/File

Vendor: bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/gzip-os2 %{version}-os2

URL: http://www.gzip.org/
# Requires should not be added for gzip wrappers (eg. zdiff, zgrep,
# zless) of another tools, because gzip "extends" the tools by its
# wrappers much more than it "requires" them.
Requires: info
Requires: coreutils
BuildRequires: texinfo
BuildRequires: rexx_exe
Provides: /@unixroot/usr/bin/gunzip
Provides: /@unixroot/usr/bin/gzip
Provides: /@unixroot/usr/bin/zcat

%description
The gzip package contains the popular GNU gzip data compression
program. Gzipped files have a .gz extension.

Gzip should be installed on your system, because it is a
very commonly used data compression program.

%debug_package

%prep
%scm_setup

autoreconf -fvi

%build
export DEFS="NO_ASM"
export CPPFLAGS="-DHAVE_LSTAT"
export LDFLAGS="-Zhigh-mem -Zomf -Zexe -Zargs-wild -Zargs-resp"
%configure

make
#make gzip.info

%install
rm -rf ${RPM_BUILD_ROOT}
%make_install

# Tailor converter scripts to use the right path
for f in *.cmd ; do
  # Due to bug in sed 4.2.1-2 -i kills CRLF in processed files, so use redirection
  %{__sed} \
-e '/^Parse Source .*$/ d' \
-e 's|^helperpath = .*$|helperpath = value('UNIXROOT',,'OS2ENVIRONMENT')"\\usr\\bin\\"|' \
-e 's|@call|@|g' "$f" > "$f.new"
  %{__rm} "$f"
  %{__mv} "$f.new" "$f"
# Pack and install OS/2 Rexx scripts
  rexx2vio "$f" "%{buildroot}%{_bindir}/${f%.cmd}.exe"
done


gzip -9nf ${RPM_BUILD_ROOT}%{_infodir}/gzip.info*

# we don't ship it, so let's remove it from ${RPM_BUILD_ROOT}
rm -f ${RPM_BUILD_ROOT}%{_infodir}/dir
# uncompress is a part of ncompress package
rm -f ${RPM_BUILD_ROOT}%{_bindir}/uncompress

%clean
rm -rf ${RPM_BUILD_ROOT}

%post
if [ -f %{_infodir}/gzip.info* ]; then
    %{_sbindir}/install-info %{_infodir}/gzip.info.gz %{_infodir}/dir || :
fi

%preun
if [ $1 = 0 ]; then
    if [ -f %{_infodir}/gzip.info* ]; then
        %{_sbindir}/install-info --delete %{_infodir}/gzip.info.gz %{_infodir}/dir || :
    fi
fi

%files
%defattr(-,root,root)
%doc NEWS README AUTHORS ChangeLog THANKS TODO
%{!?_licensedir:%global license %%doc}
%license COPYING
%{_bindir}/*
%exclude %{_bindir}/*.dbg
%{_mandir}/*/*
%{_infodir}/gzip.info*

%changelog
* Thu Aug 24 2017 Silvan Scherrer <silvan.scherrer@aroa.ch> 1.8-1
- update vendor source to version 1.8
- move source from netlabs svn to github

* Thu Feb 02 2012 yd
- Remove symlinks from /bin.

* Fri Nov 18 2011 yd
- keep all executables to /usr/bin and place symlinks in /bin
