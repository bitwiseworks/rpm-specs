/* bww-fix-docdir */
parse source . 'COMMAND ' fullprg
prg      = strip(filespec('N',fullprg))
debug    = (value("DEBUG",,"OS2ENVIRONMENT")<>"")
if debug then say prg': "'fullprg'"'
DocFldr  = value("UNIXROOT",,"OS2ENVIRONMENT")"\usr\share\doc"
LongName = "Documentation"
LenLN    = d2x(length(Longname))
if debug then say prg': "'Docfldr'"'
ok = SysSetObjectData(DocFldr, "ALWAYSSORT=YES;DEFAULTSORT=-1;SHOWALLINTREEVIEW=YES;DEFAULTVIEW=TREE;NODELETE=YES;")
if ok = 1 & debug then say prg": Adjusted view successfully."
ok = SysPutEA(DocFldr,'.LONGNAME', x2c("FDFF")||x2c(LenLN||"00")||LongName)
if ok = 0 & debug then say prg": Set .LONGNAME successfully."
exit 0
