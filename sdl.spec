%define svn_url http://svn.netlabs.org/repos/ports/libsdl/trunk
%define svn_rev 1395

Summary: Simple DirectMedia Layer
Name: sdl
Version: 1.2.15
Release: 1%{?dist}
Source: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
#Source: https://www.libsdl.org/release/%{name}-%{version}.zip
Patch0:  SDL-os2.patch
URL: http://www.libsdl.org/
License: LGPL
Group: System Environment/Libraries
BuildRoot: %{_tmppath}/%{name}-%{version}-buildroot
Prefix: %{_prefix}
#%ifos os2
Provides: sdl12.dll
BuildRequires: os2tk45-libs os2tk45-headers nasm
#%endif

%define __defattr %defattr(-,root,root)
%define __soext dll

%description
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

%package  devel
Summary:  Libraries, includes and more to develop SDL applications.
Group:    Development/Libraries
Requires: %{name} = %{version}-%{release}

%description devel
This is the Simple DirectMedia Layer, a generic API that provides low
level access to audio, keyboard, mouse, and display framebuffer across
multiple platforms.

This is the libraries, include files and other resources you can use
to develop SDL applications.

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
export  CFLAGS="-g -DBUILD_SDL -DUSE_ASM_MIXER_VC -DICONV_INBUF_NONCONST -DUSE_DOSSETPRIORITY \
	-DSDL_AUDIO_DRIVER_DARTALT -DUSE_OS2_TOOLKIT_HEADERS -idirafter /@unixroot/usr/include/os2tk45" \
	CXXFLAGS="-g -DBUILD_SDL -DUSE_ASM_MIXER_VC -DICONV_INBUF_NONCONST -DUSE_DOSSETPRIORITY \
	-DSDL_AUDIO_DRIVER_DARTALT -DUSE_OS2_TOOLKIT_HEADERS -idirafter /@unixroot/usr/include/os2tk45" \
	LDFLAGS="-Zomf -Zhigh-mem -g -lmmpm2"

./configure \
	--prefix=%{prefix} \
        --enable-audio \
	--enable-video \
	--enable-events \
	--enable-joystick \
	--enable-cdrom \
	--enable-threads \
	--enable-timers \
	--enable-file \
	--enable-loadso \
	--enable-cpuinfo \
	--enable-assembly \
	--disable-static \
	--enable-shared

%{__make} %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
%makeinstall

# create OMF libs
emximp -o %{buildroot}%{_libdir}/SDL_dll.lib %{buildroot}%{_libdir}/SDL120.dll
emximp -o %{buildroot}%{_libdir}/SDL120_dll.lib %{buildroot}%{_libdir}/SDL120.dll
emximp -o %{buildroot}%{_libdir}/SDL_dll.a %{buildroot}%{_libdir}/SDL120.dll
emximp -o %{buildroot}%{_libdir}/SDL120_dll.a %{buildroot}%{_libdir}/SDL120.dll
rm -rf %{buildroot}%{_libdir}/SDLmain.a

# create forwarder
echo "LIBRARY SDL12" >%{buildroot}%{_libdir}/sdl12.def
echo "DESCRIPTION '@#libsdl org:1.2.15#@##1## 2016-03-15               dtp::::::@@Simple DirectMedia Layer (alternative port) forwarder'" >>%{buildroot}%{_libdir}/sdl12.def
echo "DATA MULTIPLE NONSHARED" >>%{buildroot}%{_libdir}/sdl12.def
echo "EXPORTS" >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_InitSubSystem                           @1 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_Init                                    @2 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_QuitSubSystem                           @3 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WasInit                                 @4 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_Quit                                    @5 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_Linked_Version                          @6 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetError                                @7 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetError                                @8 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ClearError                              @9 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_Error                                   @10 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_revcpy                                  @11 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_strtoul                                 @12 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_strtoull                                @13 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_strncasecmp                             @14 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ConvertAudio                            @15 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_BuildAudioCVT                           @16 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_MixAudio                                @17 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_LoadWAV_RW                              @18 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_FreeWAV                                 @19 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_OpenAudio                               @20 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_AudioQuit                               @21 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_AudioInit                               @22 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CloseAudio                              @23 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_AudioDriverName                         @24 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetAudioStatus                          @25 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_PauseAudio                              @26 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_LockAudio                               @27 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_UnlockAudio                             @28 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_HasRDTSC                                @29 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_HasMMX                                  @30 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_HasMMXExt                               @31 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_Has3DNow                                @32 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_Has3DNowExt                             @33 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_HasSSE                                  @34 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_HasSSE2                                 @35 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_HasAltiVec                              @36 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetAppState                             @37 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_PeepEvents                              @38 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_PumpEvents                              @39 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_PollEvent                               @40 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WaitEvent                               @41 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_PushEvent                               @42 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetEventFilter                          @43 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetEventFilter                          @44 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_EventState                              @45 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_EnableUNICODE                           @46 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetKeyState                             @47 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetModState                             @48 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetModState                             @49 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetKeyName                              @50 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_EnableKeyRepeat                         @51 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetKeyRepeat                            @52 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetMouseState                           @53 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetRelativeMouseState                   @54 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_RWFromFile                              @55 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_RWFromFP                                @56 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_RWFromMem                               @57 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_RWFromConstMem                          @58 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_AllocRW                                 @59 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_FreeRW                                  @60 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ReadLE16                                @61 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ReadBE16                                @62 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ReadLE32                                @63 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ReadBE32                                @64 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ReadLE64                                @65 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ReadBE64                                @66 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WriteLE16                               @67 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WriteBE16                               @68 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WriteLE32                               @69 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WriteBE32                               @70 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WriteLE64                               @71 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WriteBE64                               @72 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_NumJoysticks                            @73 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickName                            @74 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickOpen                            @75 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickOpened                          @76 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickIndex                           @77 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickNumAxes                         @78 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickNumHats                         @79 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickNumBalls                        @80 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickNumButtons                      @81 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickGetAxis                         @82 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickGetHat                          @83 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickGetBall                         @84 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickGetButton                       @85 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickClose                           @86 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickUpdate                          @87 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_JoystickEventState                      @88 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_LoadObject                              @89 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_LoadFunction                            @90 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_UnloadObject                            @91 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CreateThread                            @92 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WaitThread                              @93 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetThreadID                             @94 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_KillThread                              @95 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CreateMutex                             @96 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_DestroyMutex                            @97 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_mutexP                                  @98 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_mutexV                                  @99 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CreateSemaphore                         @100 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_DestroySemaphore                        @101 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SemWaitTimeout                          @102 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SemTryWait                              @103 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SemWait                                 @104 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SemValue                                @105 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SemPost                                 @106 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ThreadID                                @107 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CreateCond                              @108 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_DestroyCond                             @109 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CondSignal                              @110 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CondBroadcast                           @111 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CondWaitTimeout                         @112 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CondWait                                @113 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_AddTimer                                @114 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_RemoveTimer                             @115 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetTimer                                @116 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetTicks                                @117 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_Delay                                   @118 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_LoadBMP_RW                              @119 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SaveBMP_RW                              @120 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CreateCursor                            @121 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetCursor                               @122 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetCursor                               @123 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_FreeCursor                              @124 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ShowCursor                              @125 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WarpMouse                               @126 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetGamma                                @127 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetGammaRamp                            @128 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetGammaRamp                            @129 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_MapRGB                                  @130 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_MapRGBA                                 @131 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetRGBA                                 @132 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetRGB                                  @133 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SoftStretch                             @134 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CreateRGBSurface                        @135 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CreateRGBSurfaceFrom                    @136 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetColorKey                             @137 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetAlpha                                @138 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetClipRect                             @139 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetClipRect                             @140 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_LowerBlit                               @141 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_UpperBlit                               @142 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_FillRect                                @143 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_LockSurface                             @144 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_UnlockSurface                           @145 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ConvertSurface                          @146 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_FreeSurface                             @147 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_VideoInit                               @148 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_VideoDriverName                         @149 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetVideoSurface                         @150 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetVideoInfo                            @151 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_ListModes                               @152 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_VideoModeOK                             @153 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetVideoMode                            @154 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_DisplayFormat                           @155 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_DisplayFormatAlpha                      @156 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_UpdateRect                              @157 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_UpdateRects                             @158 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_Flip                                    @159 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetPalette                              @160 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_SetColors                               @161 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_VideoQuit                               @162 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GL_LoadLibrary                          @163 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GL_GetProcAddress                       @164 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GL_SetAttribute                         @165 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GL_GetAttribute                         @166 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GL_SwapBuffers                          @167 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GL_UpdateRects                          @168 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GL_Lock                                 @169 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GL_Unlock                               @170 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WM_SetCaption                           @171 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WM_GetCaption                           @172 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WM_SetIcon                              @173 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WM_GrabInput                            @174 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WM_IconifyWindow                        @175 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_WM_ToggleFullScreen                     @176 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_GetWMInfo                               @177 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CreateYUVOverlay                        @178 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_LockYUVOverlay                          @179 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_UnlockYUVOverlay                        @180 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_DisplayYUVOverlay                       @181 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_FreeYUVOverlay                          @182 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDNumDrives                             @183 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDName                                  @184 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDOpen                                  @185 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDStatus                                @186 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDPlayTracks                            @187 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDPlay                                  @188 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDPause                                 @189 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDResume                                @190 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDStop                                  @191 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDEject                                 @192 >>%{buildroot}%{_libdir}/sdl12.def
echo     SDL_CDClose                                 @193 >>%{buildroot}%{_libdir}/sdl12.def
gcc -Zomf -Zdll -o %{buildroot}%{_libdir}/SDL12.dll %{buildroot}%{_libdir}/sdl12.def \
	-c %{_builddir}/%{?buildsubdir}/src/stdlib/os2/wrap.c -L%{buildroot}%{_libdir} -lSDL_dll
rm -rf %{buildroot}%{_libdir}/dummy.* %{buildroot}%{_libdir}/sdl12.def

%clean
rm -rf $RPM_BUILD_ROOT

%files
%{__defattr}
%doc README-SDL.txt COPYING CREDITS BUGS README.OS2 README-Digi.OS2 sdl.ini
%{_libdir}/SDL12*.dll

%files devel
%{__defattr}
%doc README README-SDL.txt COPYING CREDITS BUGS WhatsNew docs.html
%doc docs/index.html docs/html
%{_bindir}/*-config
%{_libdir}/SDL*.a
%{_libdir}/SDL*.lib
%exclude %{_libdir}/lib*.la
%dir %{_includedir}/SDL
%{_includedir}/SDL/*.h
%{_libdir}/pkgconfig/sdl.pc
%{_datadir}/aclocal/*
%{_mandir}/man3/*

%changelog
* Sat Mar 12 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-1
- Initial OS/2 packaging
