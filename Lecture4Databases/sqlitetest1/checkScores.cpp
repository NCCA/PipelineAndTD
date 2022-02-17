#include <iostream>
#include <cstdlib>
#include <sqlite3.h>

static int callback(void *NotUsed, int argc, char **argv, char **azColName)
{
  int i;
  for(i=0; i<argc; i++)
  {
    printf("%s = %s\n", azColName[i], argv[i] ? argv[i] : "NULL");
  }
  printf("\n");
  return 0;
}

int main(int argc, char **argv)
{
  sqlite3 *db;
  char *zErrMsg = 0;
  int rc;

  
  rc = sqlite3_open("scores.db", &db);
  if( rc )
  {
    std::cerr<< "Can't open database: " << sqlite3_errmsg(db) <<'\n';
    sqlite3_close(db);
    exit(EXIT_FAILURE);
  }
  auto query="Select * from Scores;";
  rc = sqlite3_exec(db, query, callback, 0, &zErrMsg);
  
  sqlite3_close(db);
  return 0;
}