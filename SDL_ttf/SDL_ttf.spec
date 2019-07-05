%define svn_url http://svn.netlabs.org/repos/ports/sdl_ttf/trunk
%define svn_rev 1421

%define name SDL_ttf
%define version 2.0.11
%define release 2

Name:		%{name}
Version:	%{version}
Release:	%{release}%{?dist}
Summary:	Simple DirectMedia Layer TrueType Font library

Group:		System Environment/Libraries
License:	LGPLv2+
URL:		http://www.libsdl.org/projects/SDL_ttf/
#Source0:	http://www.libsdl.org/projects/%{name}/release/%{name}-%{version}.tar.gz
Source0:        %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
Patch0:         sdl_ttf-os2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires:	SDL-devel >= 1.2.4
BuildRequires:	freetype-devel >= 2.0
BuildRequires:	zlib-devel

%description
This library allows you to use TrueType fonts to render text in SDL
applications.


%package devel
Summary:	Development files for %{name}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	SDL-devel >= 1.2.4

%description devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.

%debug_package

%prep
%if %{?svn_rev:%(sh -c 'if test -f "%{_sourcedir}/%{name}-%{version}-r%{svn_rev}.zip" ; then echo 1 ; else echo 0 ; fi')}%{!?svn_rev):0}
%setup -q
%else
%setup -q -n "%{name}-%{version}" -Tc
svn export %{?svn_rev:-r %{svn_rev}} %{svn_url} . --force
rm -f "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip"
(cd .. && zip -SrX9 "%{_sourcedir}/%{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip" "%{name}-%{version}")
%endif

#%patch0 -p1

libtoolize -fci
./autogen.sh

%build
export CFLAGS="-g -DBUILD_SDL" LDFLAGS="-g -Zhigh-mem"

%configure \
	--disable-static

%{__make} %{?_smp_mflags}

%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# create import libs
emximp -o %{buildroot}%{_libdir}/SDL_ttf_dll.lib %{buildroot}%{_libdir}/SDL_t200.dll
emximp -o %{buildroot}%{_libdir}/SDL_ttf200_dll.lib %{buildroot}%{_libdir}/SDL_t200.dll
emximp -o %{buildroot}%{_libdir}/SDL_ttf_dll.a %{buildroot}%{_libdir}/SDL_t200.dll
emximp -o %{buildroot}%{_libdir}/SDL_ttf200_dll.a %{buildroot}%{_libdir}/SDL_t200.dll

# create forwarder
cat << EOF >%{buildroot}%{_libdir}/sdlttf.def
LIBRARY SDLttf
DESCRIPTION '@#libsdl org:1.2.15#@##1## 2016-03-16               dtp::::::@@SDL_ttf (alternative port) forwarder'
IMPORTS
    TTF_Linked_Version=SDL_t200.TTF_Linked_Version
    TTF_ByteSwappedUNICODE=SDL_t200.TTF_ByteSwappedUNICODE
    TTF_Init=SDL_t200.TTF_Init
    TTF_OpenFontIndexRW=SDL_t200.TTF_OpenFontIndexRW
    TTF_OpenFontRW=SDL_t200.TTF_OpenFontRW
    TTF_OpenFontIndex=SDL_t200.TTF_OpenFontIndex
    TTF_OpenFont=SDL_t200.TTF_OpenFont
    TTF_CloseFont=SDL_t200.TTF_CloseFont
    TTF_FontHeight=SDL_t200.TTF_FontHeight
    TTF_FontAscent=SDL_t200.TTF_FontAscent
    TTF_FontDescent=SDL_t200.TTF_FontDescent
    TTF_FontLineSkip=SDL_t200.TTF_FontLineSkip
    TTF_GetFontKerning=SDL_t200.TTF_GetFontKerning
    TTF_SetFontKerning=SDL_t200.TTF_SetFontKerning
    TTF_FontFaces=SDL_t200.TTF_FontFaces
    TTF_FontFaceIsFixedWidth=SDL_t200.TTF_FontFaceIsFixedWidth
    TTF_FontFaceFamilyName=SDL_t200.TTF_FontFaceFamilyName
    TTF_FontFaceStyleName=SDL_t200.TTF_FontFaceStyleName
    TTF_GlyphIsProvided=SDL_t200.TTF_GlyphIsProvided
    TTF_GlyphMetrics=SDL_t200.TTF_GlyphMetrics
    TTF_SizeText=SDL_t200.TTF_SizeText
    TTF_SizeUTF8=SDL_t200.TTF_SizeUTF8
    TTF_SizeUNICODE=SDL_t200.TTF_SizeUNICODE
    TTF_RenderText_Solid=SDL_t200.TTF_RenderText_Solid
    TTF_RenderUTF8_Solid=SDL_t200.TTF_RenderUTF8_Solid
    TTF_RenderUNICODE_Solid=SDL_t200.TTF_RenderUNICODE_Solid
    TTF_RenderGlyph_Solid=SDL_t200.TTF_RenderGlyph_Solid
    TTF_RenderText_Shaded=SDL_t200.TTF_RenderText_Shaded
    TTF_RenderUTF8_Shaded=SDL_t200.TTF_RenderUTF8_Shaded
    TTF_RenderUNICODE_Shaded=SDL_t200.TTF_RenderUNICODE_Shaded
    TTF_RenderGlyph_Shaded=SDL_t200.TTF_RenderGlyph_Shaded
    TTF_RenderText_Blended=SDL_t200.TTF_RenderText_Blended
    TTF_RenderUTF8_Blended=SDL_t200.TTF_RenderUTF8_Blended
    TTF_RenderUNICODE_Blended=SDL_t200.TTF_RenderUNICODE_Blended
    TTF_RenderGlyph_Blended=SDL_t200.TTF_RenderGlyph_Blended
    TTF_SetFontStyle=SDL_t200.TTF_SetFontStyle
    TTF_GetFontStyle=SDL_t200.TTF_GetFontStyle
    TTF_SetFontOutline=SDL_t200.TTF_SetFontOutline
    TTF_GetFontOutline=SDL_t200.TTF_GetFontOutline
    TTF_SetFontHinting=SDL_t200.TTF_SetFontHinting
    TTF_GetFontHinting=SDL_t200.TTF_GetFontHinting
    TTF_Quit=SDL_t200.TTF_Quit
    TTF_WasInit=SDL_t200.TTF_WasInit
EXPORTS
    TTF_Linked_Version                          @1
    TTF_ByteSwappedUNICODE                      @2
    TTF_Init                                    @3
    TTF_OpenFontIndexRW                         @4
    TTF_OpenFontRW                              @5
    TTF_OpenFontIndex                           @6
    TTF_OpenFont                                @7
    TTF_CloseFont                               @8
    TTF_FontHeight                              @9
    TTF_FontAscent                              @10
    TTF_FontDescent                             @11
    TTF_FontLineSkip                            @12
    TTF_GetFontKerning                          @13
    TTF_SetFontKerning                          @14
    TTF_FontFaces                               @15
    TTF_FontFaceIsFixedWidth                    @16
    TTF_FontFaceFamilyName                      @17
    TTF_FontFaceStyleName                       @18
    TTF_GlyphIsProvided                         @19
    TTF_GlyphMetrics                            @20
    TTF_SizeText                                @21
    TTF_SizeUTF8                                @22
    TTF_SizeUNICODE                             @23
    TTF_RenderText_Solid                        @24
    TTF_RenderUTF8_Solid                        @25
    TTF_RenderUNICODE_Solid                     @26
    TTF_RenderGlyph_Solid                       @27
    TTF_RenderText_Shaded                       @28
    TTF_RenderUTF8_Shaded                       @29
    TTF_RenderUNICODE_Shaded                    @30
    TTF_RenderGlyph_Shaded                      @31
    TTF_RenderText_Blended                      @32
    TTF_RenderUTF8_Blended                      @33
    TTF_RenderUNICODE_Blended                   @34
    TTF_RenderGlyph_Blended                     @35
    TTF_SetFontStyle                            @36
    TTF_GetFontStyle                            @37
    TTF_SetFontOutline                          @38
    TTF_GetFontOutline                          @39
    TTF_SetFontHinting                          @40
    TTF_GetFontHinting                          @41
    TTF_Quit                                    @42
    TTF_WasInit                                 @43
EOF
echo "">%{buildroot}%{_libdir}/dummy.c
gcc -Zomf -o %{buildroot}%{_libdir}/dummy.o -c %{buildroot}%{_libdir}/dummy.c
gcc -Zomf -Zdll -o %{buildroot}%{_libdir}/SDLttf.dll \
	%{buildroot}%{_libdir}/sdlttf.def %{buildroot}%{_libdir}/dummy.o
rm -rf %{buildroot}%{_libdir}/dummy.* %{buildroot}%{_libdir}/sdlttf.def

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%doc README CHANGES COPYING
%{_libdir}/SDL*.dll

%files devel
%defattr(-,root,root)
%{_libdir}/SDL*.a
%exclude %{_libdir}/lib*.la*
%{_libdir}/SDL*.lib
%{_libdir}/pkgconfig/*.pc
%{_includedir}/SDL/

%changelog
* Thu Apr 14 2016 Valery V.Sedletski <_valerius@mail.ru> - 2.0.11-2
- Made the .spec in accordance with Fedora version, renamed to SDL_ttf

* Tue Mar 15 2016 Valery V.Sedletski <_valerius@mail.ru> - 2.0.11-1
- Initial OS/2 packaging

