.PHONY: dev check test serve clean \
        server-dev server-check server-test server-serve server-clean \
        desktop-dev desktop-check desktop-build desktop-clean

SERVER  := packages/server
DESKTOP := packages/desktop

# ── Repo-wide ──────────────────────────────────────────────────────────────────

# First-time setup: install all dependencies and git hooks
dev: server-dev desktop-dev

# Run the full quality pass for all packages
check: server-check desktop-check

# Run all test suites
test: server-test

# Clean all packages
clean: server-clean desktop-clean

# ── Server (packages/server) ───────────────────────────────────────────────────

server-dev:
	$(MAKE) -C $(SERVER) dev

server-check:
	$(MAKE) -C $(SERVER) check

server-test:
	$(MAKE) -C $(SERVER) test

server-serve:
	$(MAKE) -C $(SERVER) serve

server-clean:
	$(MAKE) -C $(SERVER) clean

# ── Desktop (packages/desktop) ─────────────────────────────────────────────────

desktop-dev:
	$(MAKE) -C $(DESKTOP) dev

desktop-check:
	$(MAKE) -C $(DESKTOP) check

desktop-build:
	$(MAKE) -C $(DESKTOP) build

desktop-clean:
	$(MAKE) -C $(DESKTOP) clean


desktop-generate:
	$(MAKE) -C $(DESKTOP) generate
