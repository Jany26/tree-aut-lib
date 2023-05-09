CC = g++
CFLAGS = -std=c++14 -Wall -Wextra -Werror -g
LIBPATH = -L/usr/local/lib
LDFLAGS = -lbdd

all: blif dimacs

blif: blif_parser.cpp blif_parser.h
	@mkdir -p bin
	$(CC) $(CFLAGS) blif_parser.cpp -o bin/blif_parser $(LDFLAGS) $(LIBPATH)

dimacs: dimacs_parser.cpp
	@mkdir -p bin
	$(CC) $(CFLAGS) dimacs_parser.cpp -o bin/dimacs_parser $(LDFLAGS) $(LIBPATH)