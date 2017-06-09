/* REXX */
if RxFuncQuery('SysBootDrive') = 0 | RxFuncAdd('SysBootDrive', 'RexxUtil', 'SysBootDrive') = 0 then
  say SysBootDrive()
else
  say 'C:'
