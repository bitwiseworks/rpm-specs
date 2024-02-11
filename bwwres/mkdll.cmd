@echo off
if "%1"=="/?" goto error

link386 /A:4 /BASE:0x12000000 /NOD /NOL mkres.obj, bwwres.dll, nul, , mkres;

rc bwwres.rc bwwres.dll

goto end
:error
echo Usage: MKDLL
:end
