CC=gcc
CFLAGS=-c -fPIC
LDFLAGS=-shared
LIB_DIR=lib
OBJ_DIR=obj
SRC_DIR=src
APP_CLASSIFIER_DATA_DIR=./app/classifier/data

.PHONY: clean directories

all: directories $(LIB_DIR)/touchpadlib.so

directories: $(APP_CLASSIFIER_DATA_DIR)

$(APP_CLASSIFIER_DATA_DIR):
	-@mkdir $(APP_CLASSIFIER_DATA_DIR) 2>/dev/null || true

$(LIB_DIR)/touchpadlib.so: $(OBJ_DIR)/touchpadlib.o
	-@mkdir $(LIB_DIR) 2>/dev/null || true
	$(CC) $(LDFLAGS) -Wl,-soname,touchpadlib.so -o $(LIB_DIR)/touchpadlib.so $(OBJ_DIR)/touchpadlib.o

$(OBJ_DIR)/touchpadlib.o: $(SRC_DIR)/touchpadlib.c $(SRC_DIR)/touchpadlib.h
	-@mkdir $(OBJ_DIR) 2>/dev/null || true
	$(CC) $(CFLAGS) -o $(OBJ_DIR)/touchpadlib.o $(SRC_DIR)/touchpadlib.c

clean:
	-@rm -f $(OBJ_DIR)/*.o $(LIB_DIR)/touchpadlib.so 2>/dev/null || true
	-@rmdir $(LIB_DIR) 2>/dev/null || true
	-@rmdir $(OBJ_DIR) 2>/dev/null || true
