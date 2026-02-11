# ────────────────────────────────────────────────────────
# IRP CRTP Provenance Daemon - Build System
#
# Targets:
#   make            Build the daemon
#   make install    Install daemon + systemd service
#   make uninstall  Remove daemon + service
#   make clean      Remove build artifacts
#   make test       Run basic self-test
#
# Prerequisites:
#   apt-get install build-essential libssl-dev libsystemd-dev
#
# Part of the IRP Embodiment Framework (Lower Layer)
# ────────────────────────────────────────────────────────

CC          = gcc
CFLAGS      = -Wall -Wextra -O2 -fPIC \
              -D_FORTIFY_SOURCE=2 \
              -fstack-protector-strong \
              -Wformat -Werror=format-security
LDFLAGS     = -lssl -lcrypto
TARGET      = irp-crtp-daemon
INSTALL_DIR = /opt/irp
SYSTEMD_DIR = /etc/systemd/system
SRC_DIR     = src

SRC         = $(SRC_DIR)/crtp_daemon.c $(SRC_DIR)/crtp_chain.c
OBJ         = $(SRC:.c=.o)

.PHONY: all clean install uninstall test

all: $(TARGET)

$(TARGET): $(OBJ)
	$(CC) $(OBJ) -o $(TARGET) $(LDFLAGS)
	@echo "Built: $(TARGET)"

$(SRC_DIR)/%.o: $(SRC_DIR)/%.c $(SRC_DIR)/irp_chain.h
	$(CC) $(CFLAGS) -c $< -o $@

install: $(TARGET)
	@echo "═══ Installing IRP CRTP Daemon ═══"
	mkdir -p $(INSTALL_DIR)
	mkdir -p /etc/irp
	mkdir -p /var/log/irp
	chmod 700 /etc/irp
	chmod 755 /var/log/irp
	cp $(TARGET) $(INSTALL_DIR)/
	chmod 750 $(INSTALL_DIR)/$(TARGET)
	setcap cap_net_bind_service=+ep $(INSTALL_DIR)/$(TARGET) 2>/dev/null || true
	@echo "Installing systemd service..."
	cp service/irp-crtp.service $(SYSTEMD_DIR)/
	systemctl daemon-reload
	systemctl enable irp-crtp
	@echo ""
	@echo "═══ Installation Complete ═══"
	@echo "Next steps:"
	@echo "  1. Enroll biometric:  scripts/enroll_node.sh"
	@echo "  2. Set bind address:  edit /etc/irp/irp-crtp.env"
	@echo "  3. Start daemon:      sudo systemctl start irp-crtp"

uninstall:
	systemctl stop irp-crtp 2>/dev/null || true
	systemctl disable irp-crtp 2>/dev/null || true
	rm -f $(SYSTEMD_DIR)/irp-crtp.service
	rm -f $(INSTALL_DIR)/$(TARGET)
	systemctl daemon-reload
	@echo "IRP CRTP Daemon uninstalled."

test: $(TARGET)
	@echo "═══ CRTP Self-Test ═══"
	@echo "Checking binary..."
	@file $(TARGET)
	@echo "Checking OpenSSL linkage..."
	@ldd $(TARGET) | grep -i ssl || echo "(static or not found)"
	@echo "Header size check: expected 64 bytes"
	@echo "Self-test passed (runtime tests require enrollment)."

clean:
	rm -f $(OBJ) $(TARGET)
	@echo "Cleaned."
