CC=gcc
CFLAGS=-c -fPIC
LDFLAGS=-shared

APP_CLASSIFIER_DATA_DIR=app/classifier/data
APP_TOOLS_DATA=app/tools/data
APP_TOOLS_DATA_MATRIXANALYSER=app/tools/data/matrixanalyser
APP_TOOLS_DATA_MATRIXANALYSER_FIGURES_DIR=app/tools/data/matrixanalyser/figures
LIB_DIR=lib
OBJ_DIR=obj
SRC_DIR=src

DATA_DIRS=$(APP_CLASSIFIER_DATA_DIR) \
		  $(APP_TOOLS_DATA) \
		  $(APP_TOOLS_DATA_MATRIXANALYSER) \
		  $(APP_TOOLS_DATA_MATRIXANALYSER_FIGURES_DIR)

SILENCE_ERROR_MESSAGES=2>/dev/null || true

.PHONY: all clean directories

all: directories $(LIB_DIR)/touchpadlib.so

directories: $(DATA_DIRS)

$(DATA_DIRS):
	-@mkdir $@ 2>/dev/null || true

$(LIB_DIR)/touchpadlib.so: $(OBJ_DIR)/touchpadlib.o
	-@mkdir $(LIB_DIR) 2>/dev/null || true
	$(CC) $(LDFLAGS) -Wl,-soname,touchpadlib.so -o $(LIB_DIR)/touchpadlib.so $(OBJ_DIR)/touchpadlib.o

$(OBJ_DIR)/touchpadlib.o: $(SRC_DIR)/touchpadlib.c $(SRC_DIR)/touchpadlib.h
	-@mkdir $(OBJ_DIR) 2>/dev/null || true
	$(CC) $(CFLAGS) -o $(OBJ_DIR)/touchpadlib.o $(SRC_DIR)/touchpadlib.c

clean:
	-@rm -f $(OBJ_DIR)/*.o $(LIB_DIR)/touchpadlib.so $(SILENCE_ERROR_MESSAGES)
	-@rmdir $(LIB_DIR) $(SILENCE_ERROR_MESSAGES)
	-@rmdir $(OBJ_DIR) $(SILENCE_ERROR_MESSAGES)
	-@rm -f $(DATA_DIRS) $(SILENCE_ERROR_MESSAGES)
