#include <process.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define INCL_DOS
#define INCL_DOSERRORS
#include <os2.h>

#define DEBUG 0

int execute( char* script, int argc, char* argv[])
{
  char* python = "/@unixroot/usr/bin/" PYTHON_EXE;
  char* python2 = PYTHON_EXE;
  char** argv2;
  int i;
  int rc;
  
  if (DEBUG)
    printf( "execute: %s\n", script);
  
  argv2 = calloc( argc+1+1, sizeof(char*));
  if (argv2 == NULL) {
    perror( "argv2");
    return(-1);
  }
   
  argv2[0] = python;
  argv2[1] = script;
  for( i = 1; i<=argc; i++) {
    argv2[i+1] = argv[i];
    if (DEBUG)
      printf("%d:%x\n", i, argv[i]);
  }
  if (DEBUG)
	for( i = 0; i<argc+1+1; i++)
		printf("%d:%x %s\n", i, argv2[i], argv2[i]);

  /* try default python */
  rc = execv( python, argv2);

  /* failed, try searching python.exe in PATH */
  argv2[0] = python2;
  rc = execvp( python2, argv2);

  /* failed again */
  printf("execv failed, rc=%d\n", rc);
  perror("execv");
  // failed
  return -1;
}

int main( int argc, char* argv[])
{
    CHAR	Buff[2*_MAX_PATH];
    PPIB	pib;
    char 	drive[_MAX_DRIVE], dir[_MAX_DIR], fname[_MAX_FNAME];
    char*	bin;
    APIRET rc;

  if (DEBUG)
    puts(getenv("HOME"));

    // get executable fullpath
    rc = DosGetInfoBlocks( NULL, &pib);
    rc = DosQueryModuleName( pib->pib_hmte, sizeof(Buff), Buff);
    // extract path info
    _splitpath( Buff, drive, dir, fname, NULL);

    // try without extension
    strcpy( Buff, drive);
    strcat( Buff, dir);
    strcat( Buff, fname);
    if (DEBUG)
      printf( "try %s\n", Buff);
    if (access( Buff, 0) == 0)
      return execute( Buff, argc, argv);
    
    // try without extension
    strcat( Buff, ".py");
    if (DEBUG)
      printf( "try %s\n", Buff);
    if (access( Buff, 0) == 0)
      return execute( Buff, argc, argv);

    if (DEBUG)
      printf("script not found\n");
    exit(-1);
}

