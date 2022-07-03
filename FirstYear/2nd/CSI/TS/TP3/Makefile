# Source files directory
SRC_DIR = src

# Build directory
BUILD_DIR = src

# Include directory
INCLUDES = include

# Daemon exec name
OUT_DAEMON = monitord

# Client exec name
OUT_CLIENT = mon

# Source files necessary to build the daemon
SRCS_DAEMON = $(SRC_DIR)/file.c $(SRC_DIR)/monitord.c

# Source files necessary to build the client
SRCS_CLIENT = $(SRC_DIR)/file.c $(SRC_DIR)/monitorc.c

# Object files to build the daemon
OBJS_DAEMON = $(SRCS_DAEMON:%=%.o)

# Object files to build the client
OBJS_CLIENT = $(SRCS_CLIENT:%=%.o)

# C compiler flags 
CCFLAGS = -O2 -Wall -I$(INCLUDES) -g

# Compiler
CCC = gcc

default: $(BUILD_DIR)/$(OUT_DAEMON) $(BUILD_DIR)/$(OUT_CLIENT)

daemon: $(BUILD_DIR)/$(OUT_DAEMON) 

client: $(BUILD_DIR)/$(OUT_CLIENT)

$(BUILD_DIR)/$(OUT_DAEMON): $(OBJS_DAEMON)
	$(CCC) $(OBJS_DAEMON) $(CCFLAGS) -o $@ -lssl -lcrypto

$(BUILD_DIR)/$(OUT_CLIENT): $(OBJS_CLIENT)
	$(CCC) $(OBJS_CLIENT) $(CCFLAGS) -o $@ -lssl -lcrypto

$(BUILD_DIR)/%.c.o: $(BUILD_DIR)/%.c
	$(CCC) $(CCFLAGS) -c $< -o $@ 

clean:
	rm $(BUILD_DIR)/*.o $(BUILD_DIR)/$(OUT_DAEMON) $(BUILD_DIR)/$(OUT_CLIENT)
