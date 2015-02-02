#define svn_url     F:/rd/klibc/trunk/ash
%define svn_url     https://svn.netlabs.org/repos/libc/trunk/
%define svn_rev     3845

%define kmk_dist out/os2.x86/release/dist

Summary: A smaller version of the Bourne shell (sh).
Name: ash
Version: 0.0.0
Release: 11%{?dist}
License: BSD
Group: System Environment/Shells

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

Provides: /@unixroot/bin/sh

%description
A shell is a basic system program that interprets keyboard and mouse
commands. The ash shell is a clone of Berkeley's Bourne shell
(sh). Ash supports all of the standard sh shell commands, but is
considerably smaller than sh. The ash shell lacks some Bourne shell
features (for example, command-line histories), but it uses a lot less
memory.

You should install ash if you need a lightweight shell with many of
the same capabilities as the sh shell.

%package debug
Summary: HLL debug data for exception handling support.

%description debug
HLL debug data for exception handling support.


%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -n "%{name}-%{version}" -T -c
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url}ash ash --force
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url}Config.kmk --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif


%build
export KCFLAGS="%{optflags}"
kmk -C ash
kmk -C ash install


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_mandir}/man1

cp %{kmk_dist}/bin/ash.exe %{buildroot}%{_bindir}/sh.exe
ln -s %{_bindir}/sh.exe %{buildroot}%{_bindir}/sh
cp -p ash/sh.1 %{buildroot}%{_mandir}/man1/sh.1


%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/sh
%{_bindir}/sh.exe
%{_mandir}/man1/*

%files debug
%defattr(-,root,root)
%{_bindir}/*.dbg

%changelog
* Mon Feb 02 2015 yd <yd@os2power.com> 0.0.0-11
- r3845, rebuilt from sources with gcc 4.9.2.

* Fri Feb 03 2012 yd
- added Provides for virtual /@unixroot/bin/sh file.

* Thu Feb 02 2012 yd
- Remove symlinks from /bin.

* Tue Dec 13 2011 yd
- provides also /usr/bin/sh for compatibility with new scripts.

* Wed Nov 16 2011 yd
- keep all executables to /usr/bin and place symlinks in /bin
