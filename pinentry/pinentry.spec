
Name:    pinentry
Version: 1.1.0
Release: 1%{?dist}
Summary: Collection of simple PIN or passphrase entry dialogs

License: GPLv2+
URL:     http://www.gnupg.org/aegypten/
%if !0%{?os2_version}
Source0: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2
Source1: ftp://ftp.gnupg.org/gcrypt/pinentry/%{name}-%{version}.tar.bz2.sig

# borrowed from opensuse
Source10: pinentry-wrapper
%else
Vendor:  bww bitwise works GmbH
%scm_source github https://github.com/bitwiseworks/%{name}-os2 %{name}-%{version}-os2
%endif

BuildRequires: gcc
%if !0%{?os2_version}
BuildRequires: gcr-devel
BuildRequires: gtk2-devel
BuildRequires: libcap-devel
%endif
BuildRequires: ncurses-devel
BuildRequires: libgpg-error-devel
BuildRequires: libassuan-devel
%if !0%{?os2_version}
BuildRequires: libsecret-devel
%endif
BuildRequires: pkgconfig(Qt5Core) pkgconfig(Qt5Gui) pkgconfig(Qt5Widgets)

%if !0%{?os2_version}
Requires(pre): %{_sbindir}/update-alternatives
%endif

Provides: %{name}-curses = %{version}-%{release}

%description
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the curses (text) based version of the PIN entry dialog.

%if !0%{?os2_version}
%package gnome3
Summary: Passphrase/PIN entry dialog for GNOME 3
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
%description gnome3
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the GNOME 3 version of the PIN entry dialog.

%package gtk
Summary: Passphrase/PIN entry dialog based on GTK+
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
Provides: pinentry-gtk2 = %{version}-%{release}
%description gtk
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the GTK GUI based version of the PIN entry dialog.
%endif

%package qt
Summary: Passphrase/PIN entry dialog based on Qt5
Requires: %{name} = %{version}-%{release}
Provides: %{name}-gui = %{version}-%{release}
Obsoletes: pinentry-qt4 < 0.8.0-2
Provides:  pinentry-qt5 = %{version}-%{release}
%description qt
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the Qt4 GUI based version of the PIN entry dialog.

%package emacs
Summary: Passphrase/PIN entry dialog based on emacs
Requires: %{name} = %{version}-%{release}
%description emacs
Pinentry is a collection of simple PIN or passphrase entry dialogs which
utilize the Assuan protocol as described by the aegypten project; see
http://www.gnupg.org/aegypten/ for details.
This package contains the emacs based version of the PIN entry dialog.

%if 0%{?os2_version}
%debug_package
%endif

%prep
%if !0%{?os2_version}
%setup -q
%else
%scm_setup
autoreconf -fvi
%endif

%build
%if 0%{?os2_version}
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp -lcx"
%endif
%configure \
%if 0%{?os2_version}
  --enable-maintainer-mode \
%endif
  --disable-rpath \
  --disable-dependency-tracking \
  --without-libcap \
  --disable-pinentry-fltk \
%if !0%{?os2_version}
  --enable-pinentry-gnome3 \
  --enable-pinentry-gtk2 \
%endif
  --enable-pinentry-qt5 \
  --enable-pinentry-emacs \
%if !0%{?os2_version}
  --enable-libsecret
%endif

%if !0%{?os2_version}
%make_build
%else
make %{?_smp_mflags}
%endif

%install
%make_install

# Symlink for Backward compatibility
%if !0%{?os2_version}
ln -s pinentry-gtk-2 $RPM_BUILD_ROOT%{_bindir}/pinentry-gtk
ln -s pinentry-qt $RPM_BUILD_ROOT%{_bindir}/pinentry-qt4
%else
ln -s pinentry-qt.exe $RPM_BUILD_ROOT%{_bindir}/pinentry-qt4
%endif

%if !0%{?os2_version}
install -p -m755 -D %{SOURCE10} $RPM_BUILD_ROOT%{_bindir}/pinentry
%endif

# unpackaged files
rm -fv $RPM_BUILD_ROOT%{_infodir}/dir

%files
%license COPYING
%doc AUTHORS ChangeLog NEWS README THANKS TODO
%if !0%{?os2_version}
%{_bindir}/pinentry-curses
%else
%{_bindir}/pinentry-curses.exe
%endif
%{_bindir}/pinentry
%{_infodir}/pinentry.info*

%if !0%{?os2_version}
%files gnome3
%{_bindir}/pinentry-gnome3

%files gtk
%{_bindir}/pinentry-gtk-2
# symlink for backward compatibility
%{_bindir}/pinentry-gtk
%endif

%files qt
%if !0%{?os2_version}
%{_bindir}/pinentry-qt
%else
%{_bindir}/pinentry-qt.exe
%endif
# symlink for backward compatibility
%{_bindir}/pinentry-qt4

%files emacs
%if !0%{?os2_version}
%{_bindir}/pinentry-emacs
%else
%{_bindir}/pinentry-emacs.exe
%endif

%changelog
* Sat Jan 02 2021 Silvan Scherrer <silvan.scherrer@aroa.ch> - 1.1.0-1
- first public rpm build.
