Name: metastore
Version: 0.0
Release: 1%{?dist}

Summary: Metastore stores metadata for git
License: GPL2
Group: Development/Other
Url: git://git.hardeman.nu/metastore.git
Source: %name-%version.zip
Patch1: metastore.diff

Packager: Evgenii Terechkov <evg@altlinux.org>

# Automatically added by buildreq on Wed Jan 02 2008
#BuildRequires: libattr-devel

%description
Metastore stores metadata for git

%prep
%setup -c
%patch1 -p1 -b .os2~

%build
export RPM_CFLAGS="%{optflags}"
make prefix=%_prefix mandir=%_mandir

%install
mkdir -p %{RPM_BUILD_ROOT}/%{_mandir} %{RPM_BUILD_ROOT}/%{_bindir}
make install DESTDIR=${RPM_BUILD_ROOT} prefix=%_prefix mandir=%_mandir

%files
%_bindir/%name.exe
%_mandir/*

%doc README examples

%changelog
