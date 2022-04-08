%undefine _debugsource_packages

Name:		dooble
Version:	2.1.9.4
Release:	1
Summary:	A colorful Web browser
Group:		System/Libraries
License:	GPLv2
URL:		https://textbrowser.github.io/dooble/
Source0:	https://github.com/textbrowser/dooble/archive/%{version}.tar.gz#/%{name}-%{version}.tar.gz
BuildRequires:	qt5-qtbase-devel
#BuildRequires:  libgcrypt-devel
#BuildRequires:  libgpg-error-devel
#BuildRequires:  desktop-file-utils
#BuildRequires:  gcc-c++
#BuildRequires:  sqlite-devel

%description
Dooble the finest browser known today.

%prep
%setup -q -n %{name}-%{version}/2.x
sed -i 's|/usr/local|/usr/libexec|g' dooble.desktop dooble.sh Qt/qt.conf
sed -i '10i export QT_QPA_PLATFORM_PLUGIN_PATH=%{_libdir}/qt5/plugins/platforms' dooble.sh
sed -i '1i #include <QWebEngineCertificateError>' Source/dooble_web_engine_page.cc
sed -i 's|-Werror||' %{name}.pro

%build
qmake-qt5
make
lrelease-qt5 Translations/*.ts

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_libexecdir}/%{name}
cp -a Data Dictionaries Documentation Dooble dooble.sh qtwebengine_dictionaries Translations %{buildroot}%{_libexecdir}/%{name}
rm %{buildroot}%{_libexecdir}/%{name}/Translations/*.ts
cp Icons/Logo/%{name}.png %{buildroot}%{_libexecdir}/%{name}
mkdir -p %{buildroot}%{_bindir}
ln -s ../libexec/%{name}/%{name}.sh %{buildroot}%{_bindir}/%{name}
install -Dm644 dooble.desktop %{buildroot}%{_datadir}/applications/%{name}.desktop
ln -s %{_libdir}/qt5/plugins/platforms %{buildroot}%{_libexecdir}/%{name}/Lib

#cd %{buildroot}%{_libexecdir}/%{name}
#rm -rf %{name}.pro Makefile %{name}.doxygen DEBIAN/ Doxygen/ Source/ temp/ Windows/ Translations/*.ts Qt/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README ../LICENSE
%{_libexecdir}/%{name}
%{_bindir}/%{name}
%{_datadir}/applications/%{name}.desktop

%changelog
* Thu Dec 20 2018 Wei-Lun Chao <bluebat@member.fsf.org> - 2.1.9.4
- Rebuilt for Fedora
* Mon Dec  5 2011 Bernd Stramm <bernd.stramm@gmail.com> - 1.26
- rpm packaging
