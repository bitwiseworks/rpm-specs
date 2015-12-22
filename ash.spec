# Disable debug symbols stuff - makes no sense w/o EXCEPTQ support
# (also depends on http://trac.netlabs.org/rpm/ticket/134)
%define _strip_no_debuginfo 1

%define kmk_dist out/os2.x86/release/dist

Summary: A smaller version of the Bourne shell (sh).
Name: ash
Version: 0.0.1
Release: 1%{?dist}
License: BSD
Group: System Environment/Shells

%define svn_url     https://svn.netlabs.org/repos/libc/trunk/
%define svn_rev     3845

Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip

BuildRequires: gcc make subversion zip

# @todo when it's there:
#BuildRequires: yacc

%description
A shell is a basic system program that interprets keyboard and mouse
commands. The ash shell is a clone of Berkeley's Bourne shell
(sh). Ash supports all of the standard sh shell commands, but is
considerably smaller than sh. The ash shell lacks some Bourne shell
features (for example, command-line histories), but it uses a lot less
memory.

You should install ash if you need a lightweight shell with many of
the same capabilities as the sh shell.

%package sh
Summary:  Installs ASH as the system default POSIX shell.
Requires: ash
# @todo See http://trac.netlabs.org/rpm/ticket/137.
Provides: /@unixroot/bin/sh

%description sh
Virtual package that installs ash as the system default POSIX shell.


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

cp %{kmk_dist}/bin/%{name}.exe %{buildroot}%{_bindir}/
cp -p ash/sh.1 %{buildroot}%{_mandir}/man1/%{name}.1

# Create a symlink for the default shell
ln -s %{_bindir}/%{name}.exe %{buildroot}%{_bindir}/sh
cp -p %{buildroot}%{_bindir}/%{name}.exe %{buildroot}%{_bindir}/sh.exe
ln -s %{_mandir}/man1/%{name}.1 %{buildroot}%{_mandir}/man1/sh.1

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}.exe
%{_mandir}/man1/%{name}.1

%files sh
%{_bindir}/sh
%{_bindir}/sh.exe
%{_mandir}/man1/sh.1

%changelog
* Mon Apr 6 2015 Dmitriy Kuminov <coding@dmik.org> 0.0.1-1
- Change version to 0.0.1 to mark significant changes in package structure.
- Make `ash` provide `ash.exe` and put `sh` symlinks to `ash-sh`.
- Remove debug package (not needed w/o EXCEPTQ support).

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
