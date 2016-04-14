%define svn_url http://svn.netlabs.org/repos/ports/libsdl/trunk
%define svn_rev 1537

Name:    SDL
Version: 1.2.15
Release: 3%{?dist}
Summary:    A cross-platform multimedia library
Group:      System Environment/Libraries
URL:        http://www.libsdl.org/
# The license of the file src/video/fbcon/riva_mmio.h is bad, but the contents
# of the file has been relicensed to MIT in 2008 by Nvidia for the 
# xf86_video-nv driver, therefore it can be considered ok.
License:    LGPLv2+
# Source: http://www.libsdl.org/release/%%{name}-%%{version}.tar.gz
# To create the repackaged archive use ./repackage.sh %%{version}
Source0: %{name}-%{version}%{?svn_rev:-r%{svn_rev}}.zip
Patch0:  SDL-os2-2.patch
# Rejected by upstream as sdl1155, rh480065
#Patch0:     SDL-1.2.10-GrabNotViewable.patch
# Proposed to upstream as sdl1680, rh891973
#Patch1:     SDL-1.2.15-x11-Bypass-SetGammaRamp-when-changing-gamma.patch
# Proposded to upstream as sdl1769
#Patch2:     SDL-1.2.15-const_XData32.patch
# sdl-config(1) manual from Debian, rh948864
#Patch3:     SDL-1.2.15-add_sdl_config_man.patch
# Upstream fix for sdl1486, rh990677
#Patch4:     SDL-1.2.15-ignore_insane_joystick_axis.patch
# Do not use backing store by default, sdl2383, rh1073057, rejected by
# upstream
#Patch5:     SDL-1.2.15-no-default-backing-store.patch
# Fix processing keyboard events if SDL_EnableUNICODE() is enabled, sdl2325,
# rh1126136, in upstream after 1.2.15
#Patch6:     SDL-1.2.15-SDL_EnableUNICODE_drops_keyboard_events.patch

#BuildRequires:  alsa-lib-devel
#%if %{with arts}
#BuildRequires:  arts-devel
#%endif
#BuildRequires:  audiofile-devel
BuildRequires:  coreutils
#%if %{with esound}
#BuildRequires:  esound-devel
#%endif
BuildRequires:  gcc
BuildRequires:  libc-devel
#BuildRequires:  mesa-libGL-devel
#BuildRequires:  mesa-libGLU-devel
#BuildRequires:  libXext-devel
#BuildRequires:  libX11-devel
#BuildRequires:  libXrandr-devel
#BuildRequires:  libXrender-devel
BuildRequires:  make
#%if %{with nas}
#BuildRequires:  nas-devel
#%endif
#%ifarch %{ix86}
BuildRequires:  nasm
#%endif
#BuildRequires:  pulseaudio-libs-devel
#%if %{with esound}
#BuildRequires:  sed
#%endif
# Autotools
BuildRequires:  automake
BuildRequires:  autoconf
BuildRequires:  libtool

%description
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device.

%package devel
Summary:    Files needed to develop Simple DirectMedia Layer applications
Group:      Development/Libraries
Requires:   %{name} = %{version}-%{release}
#Requires:   alsa-lib-devel
#Requires:   mesa-libGL-devel
#Requires:   mesa-libGLU-devel
#Requires:   libX11-devel
#Requires:   libXext-devel
#Requires:   libXrandr-devel
#Requires:   libXrender-devel

%description devel
Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
to provide fast access to the graphics frame buffer and audio device. This
package provides the libraries, include files, and other resources needed for
developing SDL applications.

#%package static
#Summary:    Files needed to develop static Simple DirectMedia Layer applications
#Group:      Development/Libraries
#Requires:   SDL-devel = %{version}-%{release}

#%description static
#Simple DirectMedia Layer (SDL) is a cross-platform multimedia library designed
#to provide fast access to the graphics frame buffer and audio device. This
#package provides the static libraries needed for developing static SDL
#applications.

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

%configure \
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
cat << EOF >%{buildroot}%{_libdir}/SDL12.def
LIBRARY SDL12
DESCRIPTION '@#libsdl org:1.2.15#@##1## 2016-03-16               dtp::::::@@Simple DirectMedia Layer (alternative port) forwarder'
DATA MULTIPLE NONSHARED
IMPORTS
    SDL_InitSubSystem=SDL120.SDL_InitSubSystem
    SDL_Init=SDL120.SDL_Init
    SDL_QuitSubSystem=SDL120.SDL_QuitSubSystem
    SDL_WasInit=SDL120.SDL_WasInit
    SDL_Quit=SDL120.SDL_Quit
    SDL_Linked_Version=SDL120.SDL_Linked_Version
    SDL_SetError=SDL120.SDL_SetError
    SDL_GetError=SDL120.SDL_GetError
    SDL_ClearError=SDL120.SDL_ClearError
    SDL_Error=SDL120.SDL_Error
;    SDL_revcpy=SDL120.SDL_revcpy
;    SDL_strtoul=SDL120.SDL_strtoul
;    SDL_strtoull=SDL120.SDL_strtoull
;    SDL_strncasecmp=SDL120.SDL_strncasecmp
    SDL_ConvertAudio=SDL120.SDL_ConvertAudio
    SDL_BuildAudioCVT=SDL120.SDL_BuildAudioCVT
    SDL_MixAudio=SDL120.SDL_MixAudio
    SDL_LoadWAV_RW=SDL120.SDL_LoadWAV_RW
    SDL_FreeWAV=SDL120.SDL_FreeWAV
    SDL_OpenAudio=SDL120.SDL_OpenAudio
    SDL_AudioQuit=SDL120.SDL_AudioQuit
    SDL_AudioInit=SDL120.SDL_AudioInit
    SDL_CloseAudio=SDL120.SDL_CloseAudio
    SDL_AudioDriverName=SDL120.SDL_AudioDriverName
    SDL_GetAudioStatus=SDL120.SDL_GetAudioStatus
    SDL_PauseAudio=SDL120.SDL_PauseAudio
    SDL_LockAudio=SDL120.SDL_LockAudio
    SDL_UnlockAudio=SDL120.SDL_UnlockAudio
    SDL_HasRDTSC=SDL120.SDL_HasRDTSC
    SDL_HasMMX=SDL120.SDL_HasMMX
    SDL_HasMMXExt=SDL120.SDL_HasMMXExt
    SDL_Has3DNow=SDL120.SDL_Has3DNow
    SDL_Has3DNowExt=SDL120.SDL_Has3DNowExt
    SDL_HasSSE=SDL120.SDL_HasSSE
    SDL_HasSSE2=SDL120.SDL_HasSSE2
    SDL_HasAltiVec=SDL120.SDL_HasAltiVec
    SDL_GetAppState=SDL120.SDL_GetAppState
    SDL_PeepEvents=SDL120.SDL_PeepEvents
    SDL_PumpEvents=SDL120.SDL_PumpEvents
    SDL_PollEvent=SDL120.SDL_PollEvent
    SDL_WaitEvent=SDL120.SDL_WaitEvent
    SDL_PushEvent=SDL120.SDL_PushEvent
    SDL_SetEventFilter=SDL120.SDL_SetEventFilter
    SDL_GetEventFilter=SDL120.SDL_GetEventFilter
    SDL_EventState=SDL120.SDL_EventState
    SDL_EnableUNICODE=SDL120.SDL_EnableUNICODE
    SDL_GetKeyState=SDL120.SDL_GetKeyState
    SDL_GetModState=SDL120.SDL_GetModState
    SDL_SetModState=SDL120.SDL_SetModState
    SDL_GetKeyName=SDL120.SDL_GetKeyName
    SDL_EnableKeyRepeat=SDL120.SDL_EnableKeyRepeat
    SDL_GetKeyRepeat=SDL120.SDL_GetKeyRepeat
    SDL_GetMouseState=SDL120.SDL_GetMouseState
    SDL_GetRelativeMouseState=SDL120.SDL_GetRelativeMouseState
    SDL_RWFromFile=SDL120.SDL_RWFromFile
    SDL_RWFromFP=SDL120.SDL_RWFromFP
    SDL_RWFromMem=SDL120.SDL_RWFromMem
    SDL_RWFromConstMem=SDL120.SDL_RWFromConstMem
    SDL_AllocRW=SDL120.SDL_AllocRW
    SDL_FreeRW=SDL120.SDL_FreeRW
    SDL_ReadLE16=SDL120.SDL_ReadLE16
    SDL_ReadBE16=SDL120.SDL_ReadBE16
    SDL_ReadLE32=SDL120.SDL_ReadLE32
    SDL_ReadBE32=SDL120.SDL_ReadBE32
    SDL_ReadLE64=SDL120.SDL_ReadLE64
    SDL_ReadBE64=SDL120.SDL_ReadBE64
    SDL_WriteLE16=SDL120.SDL_WriteLE16
    SDL_WriteBE16=SDL120.SDL_WriteBE16
    SDL_WriteLE32=SDL120.SDL_WriteLE32
    SDL_WriteBE32=SDL120.SDL_WriteBE32
    SDL_WriteLE64=SDL120.SDL_WriteLE64
    SDL_WriteBE64=SDL120.SDL_WriteBE64
    SDL_NumJoysticks=SDL120.SDL_NumJoysticks
    SDL_JoystickName=SDL120.SDL_JoystickName
    SDL_JoystickOpen=SDL120.SDL_JoystickOpen
    SDL_JoystickOpened=SDL120.SDL_JoystickOpened
    SDL_JoystickIndex=SDL120.SDL_JoystickIndex
    SDL_JoystickNumAxes=SDL120.SDL_JoystickNumAxes
    SDL_JoystickNumHats=SDL120.SDL_JoystickNumHats
    SDL_JoystickNumBalls=SDL120.SDL_JoystickNumBalls
    SDL_JoystickNumButtons=SDL120.SDL_JoystickNumButtons
    SDL_JoystickGetAxis=SDL120.SDL_JoystickGetAxis
    SDL_JoystickGetHat=SDL120.SDL_JoystickGetHat
    SDL_JoystickGetBall=SDL120.SDL_JoystickGetBall
    SDL_JoystickGetButton=SDL120.SDL_JoystickGetButton
    SDL_JoystickClose=SDL120.SDL_JoystickClose
    SDL_JoystickUpdate=SDL120.SDL_JoystickUpdate
    SDL_JoystickEventState=SDL120.SDL_JoystickEventState
    SDL_LoadObject=SDL120.SDL_LoadObject
    SDL_LoadFunction=SDL120.SDL_LoadFunction
    SDL_UnloadObject=SDL120.SDL_UnloadObject
    SDL_CreateThread=SDL120.SDL_CreateThread
    SDL_WaitThread=SDL120.SDL_WaitThread
    SDL_GetThreadID=SDL120.SDL_GetThreadID
    SDL_KillThread=SDL120.SDL_KillThread
    SDL_CreateMutex=SDL120.SDL_CreateMutex
    SDL_DestroyMutex=SDL120.SDL_DestroyMutex
    SDL_mutexP=SDL120.SDL_mutexP
    SDL_mutexV=SDL120.SDL_mutexV
    SDL_CreateSemaphore=SDL120.SDL_CreateSemaphore
    SDL_DestroySemaphore=SDL120.SDL_DestroySemaphore
    SDL_SemWaitTimeout=SDL120.SDL_SemWaitTimeout
    SDL_SemTryWait=SDL120.SDL_SemTryWait
    SDL_SemWait=SDL120.SDL_SemWait
    SDL_SemValue=SDL120.SDL_SemValue
    SDL_SemPost=SDL120.SDL_SemPost
    SDL_ThreadID=SDL120.SDL_ThreadID
    SDL_CreateCond=SDL120.SDL_CreateCond
    SDL_DestroyCond=SDL120.SDL_DestroyCond
    SDL_CondSignal=SDL120.SDL_CondSignal
    SDL_CondBroadcast=SDL120.SDL_CondBroadcast
    SDL_CondWaitTimeout=SDL120.SDL_CondWaitTimeout
    SDL_CondWait=SDL120.SDL_CondWait
    SDL_AddTimer=SDL120.SDL_AddTimer
    SDL_RemoveTimer=SDL120.SDL_RemoveTimer
    SDL_SetTimer=SDL120.SDL_SetTimer
    SDL_GetTicks=SDL120.SDL_GetTicks
    SDL_Delay=SDL120.SDL_Delay
    SDL_LoadBMP_RW=SDL120.SDL_LoadBMP_RW
    SDL_SaveBMP_RW=SDL120.SDL_SaveBMP_RW
    SDL_CreateCursor=SDL120.SDL_CreateCursor
    SDL_SetCursor=SDL120.SDL_SetCursor
    SDL_GetCursor=SDL120.SDL_GetCursor
    SDL_FreeCursor=SDL120.SDL_FreeCursor
    SDL_ShowCursor=SDL120.SDL_ShowCursor
    SDL_WarpMouse=SDL120.SDL_WarpMouse
    SDL_SetGamma=SDL120.SDL_SetGamma
    SDL_SetGammaRamp=SDL120.SDL_SetGammaRamp
    SDL_GetGammaRamp=SDL120.SDL_GetGammaRamp
    SDL_MapRGB=SDL120.SDL_MapRGB
    SDL_MapRGBA=SDL120.SDL_MapRGBA
    SDL_GetRGBA=SDL120.SDL_GetRGBA
    SDL_GetRGB=SDL120.SDL_GetRGB
    SDL_SoftStretch=SDL120.SDL_SoftStretch
    SDL_CreateRGBSurface=SDL120.SDL_CreateRGBSurface
    SDL_CreateRGBSurfaceFrom=SDL120.SDL_CreateRGBSurfaceFrom
    SDL_SetColorKey=SDL120.SDL_SetColorKey
    SDL_SetAlpha=SDL120.SDL_SetAlpha
    SDL_SetClipRect=SDL120.SDL_SetClipRect
    SDL_GetClipRect=SDL120.SDL_GetClipRect
    SDL_LowerBlit=SDL120.SDL_LowerBlit
    SDL_UpperBlit=SDL120.SDL_UpperBlit
    SDL_FillRect=SDL120.SDL_FillRect
    SDL_LockSurface=SDL120.SDL_LockSurface
    SDL_UnlockSurface=SDL120.SDL_UnlockSurface
    SDL_ConvertSurface=SDL120.SDL_ConvertSurface
    SDL_FreeSurface=SDL120.SDL_FreeSurface
    SDL_VideoInit=SDL120.SDL_VideoInit
    SDL_VideoDriverName=SDL120.SDL_VideoDriverName
    SDL_GetVideoSurface=SDL120.SDL_GetVideoSurface
    SDL_GetVideoInfo=SDL120.SDL_GetVideoInfo
    SDL_ListModes=SDL120.SDL_ListModes
    SDL_VideoModeOK=SDL120.SDL_VideoModeOK
    SDL_SetVideoMode=SDL120.SDL_SetVideoMode
    SDL_DisplayFormat=SDL120.SDL_DisplayFormat
    SDL_DisplayFormatAlpha=SDL120.SDL_DisplayFormatAlpha
    SDL_UpdateRect=SDL120.SDL_UpdateRect
    SDL_UpdateRects=SDL120.SDL_UpdateRects
    SDL_Flip=SDL120.SDL_Flip
    SDL_SetPalette=SDL120.SDL_SetPalette
    SDL_SetColors=SDL120.SDL_SetColors
    SDL_VideoQuit=SDL120.SDL_VideoQuit
    SDL_GL_LoadLibrary=SDL120.SDL_GL_LoadLibrary
    SDL_GL_GetProcAddress=SDL120.SDL_GL_GetProcAddress
    SDL_GL_SetAttribute=SDL120.SDL_GL_SetAttribute
    SDL_GL_GetAttribute=SDL120.SDL_GL_GetAttribute
    SDL_GL_SwapBuffers=SDL120.SDL_GL_SwapBuffers
    SDL_GL_UpdateRects=SDL120.SDL_GL_UpdateRects
    SDL_GL_Lock=SDL120.SDL_GL_Lock
    SDL_GL_Unlock=SDL120.SDL_GL_Unlock
    SDL_WM_SetCaption=SDL120.SDL_WM_SetCaption
    SDL_WM_GetCaption=SDL120.SDL_WM_GetCaption
    SDL_WM_SetIcon=SDL120.SDL_WM_SetIcon
    SDL_WM_GrabInput=SDL120.SDL_WM_GrabInput
    SDL_WM_IconifyWindow=SDL120.SDL_WM_IconifyWindow
    SDL_WM_ToggleFullScreen=SDL120.SDL_WM_ToggleFullScreen
    SDL_GetWMInfo=SDL120.SDL_GetWMInfo
    SDL_CreateYUVOverlay=SDL120.SDL_CreateYUVOverlay
    SDL_LockYUVOverlay=SDL120.SDL_LockYUVOverlay
    SDL_UnlockYUVOverlay=SDL120.SDL_UnlockYUVOverlay
    SDL_DisplayYUVOverlay=SDL120.SDL_DisplayYUVOverlay
    SDL_FreeYUVOverlay=SDL120.SDL_FreeYUVOverlay
    SDL_CDNumDrives=SDL120.SDL_CDNumDrives
    SDL_CDName=SDL120.SDL_CDName
    SDL_CDOpen=SDL120.SDL_CDOpen
    SDL_CDStatus=SDL120.SDL_CDStatus
    SDL_CDPlayTracks=SDL120.SDL_CDPlayTracks
    SDL_CDPlay=SDL120.SDL_CDPlay
    SDL_CDPause=SDL120.SDL_CDPause
    SDL_CDResume=SDL120.SDL_CDResume
    SDL_CDStop=SDL120.SDL_CDStop
    SDL_CDEject=SDL120.SDL_CDEject
    SDL_CDClose=SDL120.SDL_CDClose
EXPORTS
    SDL_InitSubSystem                           @1
    SDL_Init                                    @2
    SDL_QuitSubSystem                           @3
    SDL_WasInit                                 @4
    SDL_Quit                                    @5
    SDL_Linked_Version                          @6
    SDL_SetError                                @7
    SDL_GetError                                @8
    SDL_ClearError                              @9
    SDL_Error                                   @10
    SDL_revcpy                                  @11
    SDL_strtoul                                 @12
    SDL_strtoull                                @13
    SDL_strncasecmp                             @14
    SDL_ConvertAudio                            @15
    SDL_BuildAudioCVT                           @16
    SDL_MixAudio                                @17
    SDL_LoadWAV_RW                              @18
    SDL_FreeWAV                                 @19
    SDL_OpenAudio                               @20
    SDL_AudioQuit                               @21
    SDL_AudioInit                               @22
    SDL_CloseAudio                              @23
    SDL_AudioDriverName                         @24
    SDL_GetAudioStatus                          @25
    SDL_PauseAudio                              @26
    SDL_LockAudio                               @27
    SDL_UnlockAudio                             @28
    SDL_HasRDTSC                                @29
    SDL_HasMMX                                  @30
    SDL_HasMMXExt                               @31
    SDL_Has3DNow                                @32
    SDL_Has3DNowExt                             @33
    SDL_HasSSE                                  @34
    SDL_HasSSE2                                 @35
    SDL_HasAltiVec                              @36
    SDL_GetAppState                             @37
    SDL_PeepEvents                              @38
    SDL_PumpEvents                              @39
    SDL_PollEvent                               @40
    SDL_WaitEvent                               @41
    SDL_PushEvent                               @42
    SDL_SetEventFilter                          @43
    SDL_GetEventFilter                          @44
    SDL_EventState                              @45
    SDL_EnableUNICODE                           @46
    SDL_GetKeyState                             @47
    SDL_GetModState                             @48
    SDL_SetModState                             @49
    SDL_GetKeyName                              @50
    SDL_EnableKeyRepeat                         @51
    SDL_GetKeyRepeat                            @52
    SDL_GetMouseState                           @53
    SDL_GetRelativeMouseState                   @54
    SDL_RWFromFile                              @55
    SDL_RWFromFP                                @56
    SDL_RWFromMem                               @57
    SDL_RWFromConstMem                          @58
    SDL_AllocRW                                 @59
    SDL_FreeRW                                  @60
    SDL_ReadLE16                                @61
    SDL_ReadBE16                                @62
    SDL_ReadLE32                                @63
    SDL_ReadBE32                                @64
    SDL_ReadLE64                                @65
    SDL_ReadBE64                                @66
    SDL_WriteLE16                               @67
    SDL_WriteBE16                               @68
    SDL_WriteLE32                               @69
    SDL_WriteBE32                               @70
    SDL_WriteLE64                               @71
    SDL_WriteBE64                               @72
    SDL_NumJoysticks                            @73
    SDL_JoystickName                            @74
    SDL_JoystickOpen                            @75
    SDL_JoystickOpened                          @76
    SDL_JoystickIndex                           @77
    SDL_JoystickNumAxes                         @78
    SDL_JoystickNumHats                         @79
    SDL_JoystickNumBalls                        @80
    SDL_JoystickNumButtons                      @81
    SDL_JoystickGetAxis                         @82
    SDL_JoystickGetHat                          @83
    SDL_JoystickGetBall                         @84
    SDL_JoystickGetButton                       @85
    SDL_JoystickClose                           @86
    SDL_JoystickUpdate                          @87
    SDL_JoystickEventState                      @88
    SDL_LoadObject                              @89
    SDL_LoadFunction                            @90
    SDL_UnloadObject                            @91
    SDL_CreateThread                            @92
    SDL_WaitThread                              @93
    SDL_GetThreadID                             @94
    SDL_KillThread                              @95
    SDL_CreateMutex                             @96
    SDL_DestroyMutex                            @97
    SDL_mutexP                                  @98
    SDL_mutexV                                  @99
    SDL_CreateSemaphore                         @100
    SDL_DestroySemaphore                        @101
    SDL_SemWaitTimeout                          @102
    SDL_SemTryWait                              @103
    SDL_SemWait                                 @104
    SDL_SemValue                                @105
    SDL_SemPost                                 @106
    SDL_ThreadID                                @107
    SDL_CreateCond                              @108
    SDL_DestroyCond                             @109
    SDL_CondSignal                              @110
    SDL_CondBroadcast                           @111
    SDL_CondWaitTimeout                         @112
    SDL_CondWait                                @113
    SDL_AddTimer                                @114
    SDL_RemoveTimer                             @115
    SDL_SetTimer                                @116
    SDL_GetTicks                                @117
    SDL_Delay                                   @118
    SDL_LoadBMP_RW                              @119
    SDL_SaveBMP_RW                              @120
    SDL_CreateCursor                            @121
    SDL_SetCursor                               @122
    SDL_GetCursor                               @123
    SDL_FreeCursor                              @124
    SDL_ShowCursor                              @125
    SDL_WarpMouse                               @126
    SDL_SetGamma                                @127
    SDL_SetGammaRamp                            @128
    SDL_GetGammaRamp                            @129
    SDL_MapRGB                                  @130
    SDL_MapRGBA                                 @131
    SDL_GetRGBA                                 @132
    SDL_GetRGB                                  @133
    SDL_SoftStretch                             @134
    SDL_CreateRGBSurface                        @135
    SDL_CreateRGBSurfaceFrom                    @136
    SDL_SetColorKey                             @137
    SDL_SetAlpha                                @138
    SDL_SetClipRect                             @139
    SDL_GetClipRect                             @140
    SDL_LowerBlit                               @141
    SDL_UpperBlit                               @142
    SDL_FillRect                                @143
    SDL_LockSurface                             @144
    SDL_UnlockSurface                           @145
    SDL_ConvertSurface                          @146
    SDL_FreeSurface                             @147
    SDL_VideoInit                               @148
    SDL_VideoDriverName                         @149
    SDL_GetVideoSurface                         @150
    SDL_GetVideoInfo                            @151
    SDL_ListModes                               @152
    SDL_VideoModeOK                             @153
    SDL_SetVideoMode                            @154
    SDL_DisplayFormat                           @155
    SDL_DisplayFormatAlpha                      @156
    SDL_UpdateRect                              @157
    SDL_UpdateRects                             @158
    SDL_Flip                                    @159
    SDL_SetPalette                              @160
    SDL_SetColors                               @161
    SDL_VideoQuit                               @162
    SDL_GL_LoadLibrary                          @163
    SDL_GL_GetProcAddress                       @164
    SDL_GL_SetAttribute                         @165
    SDL_GL_GetAttribute                         @166
    SDL_GL_SwapBuffers                          @167
    SDL_GL_UpdateRects                          @168
    SDL_GL_Lock                                 @169
    SDL_GL_Unlock                               @170
    SDL_WM_SetCaption                           @171
    SDL_WM_GetCaption                           @172
    SDL_WM_SetIcon                              @173
    SDL_WM_GrabInput                            @174
    SDL_WM_IconifyWindow                        @175
    SDL_WM_ToggleFullScreen                     @176
    SDL_GetWMInfo                               @177
    SDL_CreateYUVOverlay                        @178
    SDL_LockYUVOverlay                          @179
    SDL_UnlockYUVOverlay                        @180
    SDL_DisplayYUVOverlay                       @181
    SDL_FreeYUVOverlay                          @182
    SDL_CDNumDrives                             @183
    SDL_CDName                                  @184
    SDL_CDOpen                                  @185
    SDL_CDStatus                                @186
    SDL_CDPlayTracks                            @187
    SDL_CDPlay                                  @188
    SDL_CDPause                                 @189
    SDL_CDResume                                @190
    SDL_CDStop                                  @191
    SDL_CDEject                                 @192
    SDL_CDClose                                 @193
EOF
gcc -Zomf -c %{_builddir}/%{?buildsubdir}/src/stdlib/os2/wrap.c -o %{buildroot}%{_libdir}/wrap.o
gcc -Zomf -Zdll -g -o %{buildroot}%{_libdir}/SDL12.dll %{buildroot}%{_libdir}/SDL12.def \
	%{buildroot}%{_libdir}/wrap.o -L%{buildroot}%{_libdir} -lSDL_dll
rm -rf %{buildroot}%{_libdir}/wrap.o %{buildroot}%{_libdir}/SDL12.def

%clean
rm -rf $RPM_BUILD_ROOT

%files
%doc README-SDL.txt COPYING CREDITS BUGS README.OS2 README-Digi.OS2 sdl.ini
%{_libdir}/SDL12*.dll

%files devel
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

#%files static
#%{_libdir}/lib*.a

%changelog
* Thu Apr 14 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-3
- Made the .spec in accordance with Fedora version, renamed to SDL in caps

* Tue Mar 15 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-2
- Adding the debug info for forwarder/wrapper

* Sat Mar 12 2016 Valery V.Sedletski <_valerius@mail.ru> - 1.2.15-1
- Initial OS/2 packaging
