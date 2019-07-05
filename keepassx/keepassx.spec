Name:           keepassx
Version:        2.0.3
Release:        1%{?dist}
Summary:        Cross-platform password manager
Group:          User Interface/Desktops
License:        GPLv2+
URL:            http://www.keepassx.org

Vendor:		bww bitwise works GmbH
%scm_source     github https://github.com/ydario/keepassx keepassx-2.0.3-os2
#scm_source git file://f:/rd/ports/keepassx/keepassx keepassx-2.0.3-os2

BuildRequires:  libqt4-devel > 4.1
BuildRequires:  cmake
BuildRequires:  libgcrypt-devel

%description
KeePassX is an application for people with extremly high demands on secure
personal data management.
KeePassX saves many different information e.g. user names, passwords, urls,
attachemts and comments in one single database. For a better management
user-defined titles and icons can be specified for each single entry.
Furthermore the entries are sorted in groups, which are customizable as well.
The integrated search function allows to search in a single group or the
complete database.
KeePassX offers a little utility for secure password generation. The password
generator is very customizable, fast and easy to use. Especially someone who
generates passwords frequently will appreciate this feature.
The complete database is always encrypted either with AES (alias Rijndael) or
Twofish encryption algorithm using a 256 bit key. Therefore the saved
information can be considered as quite safe. KeePassX uses a database format
that is compatible with KeePass Password Safe for MS Windows.

%debug_package

%prep
%scm_setup

%build
mkdir build
cd build

pwd

%cmake \
    -DCMAKE_BUILD_TYPE=RelWithDebInfo \
    -DWITH_GUI_TESTS=OFF \
    -DWITH_TESTS=OFF \
    ..

make %{?_smp_mflags}

%install
cd build
make install DESTDIR=%{buildroot}

%post
%wps_object_create_begin
KEEPASSX_PROG:WPProgram|KeePassX/2|<WP_DESKTOP>|EXENAME=((%{_bindir}/keepassx.exe));STARTUPDIR=%{getenv:HOME};ICONFILE=((%{_bindir}/keepassx.exe));TITLE=KeePassX/2;
%wps_object_create_end

%postun
if [ "$1" = "0" ]; then
  %wps_object_delete_all
fi

%files
%doc CHANGELOG INSTALL COPYING LICENSE*
%{_bindir}/keepassx.exe
%{_datadir}/keepassx

%changelog
* Fri Nov 24 2017 yd <yd@os2power.com> 2.0.3-1
- initial rpm build
