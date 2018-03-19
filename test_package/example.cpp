#ifdef WIN32
#include <windows.h>
#endif
#include <iostream>
#include <sql.h>
#include <sqlext.h>

int main(int, char* []) {
    std::cout << "ODBC version " << SQL_SPEC_STRING << std::endl;
}

SQLRETURN driver_connect() {
	SQLHDBC dbc;
    SQLCHAR *connect_string = (unsigned char *)"DSN=mydsn;";

    return SQLDriverConnect(dbc, NULL, connect_string, SQL_NTS,
                            NULL, 0, NULL, SQL_DRIVER_COMPLETE);
}
