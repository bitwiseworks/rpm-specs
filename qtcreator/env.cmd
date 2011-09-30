/* REXX */

/*
 * Template script to set up Qt Creator official RPM build enviroment.
 *
 * Please check the paths and correct accordingly.
 */

'@echo off'

/* Compiler */
'call D:\Dev\gcc444\gcc444.cmd'
/* rpmbuild doesn't like SSP.DLL from the compiler */
'set BEGINLIBPATH=%UNIXROOT%\usr\lib;%BEGINLIBPATH%'

/* Number of make jobs, normally # of CPUs + 1 */
'set MAKE_JOBS=3'

parse arg args
if (strip(args) \== '') then
    'cmd /c' args
exit rc
