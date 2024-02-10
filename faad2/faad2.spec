# option to compile without XMMS plugin
%if %{?without_xmms:1}%{!?without_xmms:0}
 %define _without_xmms --without-xmms
%else
 %define _with_xmms --with-xmms
%endif

# this has been taken from http://www.hyperborea.org/software/dillo/dillo.spec
#################################################################################
# Identify which distribution we're building on.
# This will determine any changes in menu structure or release number (i.e. .mdk)
# Eventually, need to make this configurable from the rpmbuild command line.

%define freedesktop %(if [ -e /usr/share/applications ]; then echo 1; else echo 0; fi;)
%define conectiva %(if [ -e /etc/conectiva-release ]; then echo 1; else echo 0; fi;)
%define mdk  %(if [ -e /etc/mandrake-release ]; then echo 1; else echo 0; fi;)
%define suse %(if [ -e /etc/SuSE-release ]; then echo 1; else echo 0; fi;)
%define oldsuse 0
%if %{suse}
	%define oldsuse %(if [ `grep VERSION /etc/SuSE-release | sed -e "s/VERSION = //"` \\< 8.0 ]; then echo 1; else echo 0; fi;)
%endif

%define oldredhat %(if [ -e /etc/redhat-release ]; then echo 1; else echo 0; fi;) && !%{mdk} && !%{suse} && !%{conectiva} && !%{freedesktop}
%define plain !%{mdk} && !%{suse} && !%{conectiva} && !%{oldredhat} && !%{freedesktop}

Summary:    C library and frontend for decoding MPEG2/4 AAC
Name:       faad2
Version:    2.8.8
Release:    1
License:    GPL
Group:      Applications/Multimedia
#Source0:    http://download.sourceforge.net/faad/%{name}-%{version}.tar.gz
#Patch:                faad2-%{version}.patch
%scm_source github https://github.com/komh/faad2-os2 master
BuildRequires: autoconf, automake, libtool, gcc

%if %{?_with_xmms:1}%{!?_with_xmms:0}
#BuildRequires: xmms-devel
%endif

URL:        http://www.audiocoding.com/
#################################################################################
%if %{?_with_xmms:1}%{!?_with_xmms:0}
# GTK Dependencies
%if %{mdk}
#BuildRequires: libgtk+-devel >= 1.2.0
%endif
%if %{suse}
BuildRequires: gtk-devel >= 1.2.0
%endif
%if !%{suse} && !%{mdk}
#BuildRequires: gtk+-devel >= 1.2.0
%endif
%endif

BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root
Packager:   a.kurpiers@nt.tu-darmstadt.de

%description
FAAD 2 is a LC, MAIN and LTP profile, MPEG2 and MPEG-4 AAC decoder, completely
written from scratch. FAAD 2 is licensed under the GPL.

Includes libmp4ff, a Quicktime library for UNIX in a freely redistributable,
statically linkable library.

%package devel
Summary: Development libraries the FAAD 2 AAC decoder.
Group: Development/Libraries
Requires: %{name}

%description devel
Header files and development documentation for libfaad.

%if %{?_with_xmms:1}%{!?_with_xmms:0}
%package xmms
Group: Applications/Multimedia
Summary: AAC and MP4 input plugin for xmms
Requires: %{name}, xmms

%description xmms
The AAC xmms input plugin for xmms recognizes AAC files by an
.aac extension.
This MP4 xmms plugin reads AAC files with and without ID3 tags (version 2.x).
AAC files are MPEG2 or MPEG4 files that can be found in MPEG4 audio files
(.mp4). MPEG4 files with AAC inside can be read by RealPlayer or Quicktime.
%endif

%prep
%scm_setup
autoreconf -vif

%build
#sh bootstrap
export LDFLAGS="-Zhigh-mem -Zomf -Zargs-wild -Zargs-resp"
export LIBS="-lcx"
./configure --with-drm %{?_without_xmms} --prefix=/@unixroot/usr

make %{?_smp_mflags}

%install
rm -rf %{buildroot}
# Hack to work around a problem with DESTDIR in libtool 1.4.x
LIBRARY_PATH="%{buildroot}/usr/lib:${LIBRARY_PATH}" make install DESTDIR=%{buildroot}
# install libmp4ff
install -m 755 common/mp4ff/libmp4ff.a %{buildroot}%{_libdir}
install common/mp4ff/mp4ff.h %{buildroot}%{_includedir}
rm -f $RPM_BUILD_ROOT%{_libdir}/*.la

#%post -p /sbin/ldconfig

#%postun -p /sbin/ldconfig

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, root)
%doc AUTHORS COPYING ChangeLog NEWS README TODO
%{_bindir}/*
%{_libdir}/faad*.dll

%files devel
%defattr(-, root, root)
#%{_libdir}/faad*.dll
%{_libdir}/faad*.a
#%{_libdir}/libfaad.la
%{_includedir}/faad.h
%{_includedir}/neaacdec.h
%{_includedir}/mp4ff.h
%{_libdir}/libmp4ff.a
%{_datadir}/man/man1/*.1.gz

#%if %{?_with_xmms:1}%{!?_with_xmms:0}
#%files xmms
#%defattr(-,root,root)
#%doc plugins/xmms/README
#_libdir/xmms/Input/*
#%endif

%changelog
* Wed Oct 09 2019 Elbert Pol <elbert.pol@gmail.com> - 2.8.8-1
- First rpm for OS2
- Thankz KO Myung-Hun for the OS2 source

* Tue Jan 24 2006 Alexander Kurpiers <a.kurpiers@nt.tu-darmstadt.de>
- fix wrong function declaration in mp4ffint.h
