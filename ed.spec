Summary: The GNU line editor
Name: ed
Version: 1.15
Release: 1%{?dist}
License: GPLv3+ and GFDL
URL:     http://www.gnu.org/software/ed/
Vendor:  bww bitwise works GmbH
%scm_source  github http://github.com/bitwiseworks/%{name}-os2 %{version}-os2

BuildRequires: gcc
Requires(post): info
Requires(preun): info

%description
Ed is a line-oriented text editor, used to create, display, and modify
text files (both interactively and via shell scripts).  For most
purposes, ed has been replaced in normal usage by full-screen editors
(emacs and vi, for example).

Ed was the original UNIX editor, and may be used by some programs.  In
general, however, you probably don't need to install it and you probably
won't use it.

%debug_package

%prep
%scm_setup

%build
export EXEEXT=".exe"
%configure \
  LDFLAGS="-Zbin-files -Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx" \
  CFLAGS="%{optflags}"
make

%install
%make_install
rm -vrf %{buildroot}%{_infodir}/dir

%files
%license COPYING
%doc ChangeLog NEWS README TODO AUTHORS
%{_bindir}/ed.exe
%{_bindir}/red
%{_mandir}/man1/ed.1*
%{_mandir}/man1/red.1*
%{_infodir}/ed.info*

%changelog
* Tue May 21 2019 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.15-1
- first rpm version
