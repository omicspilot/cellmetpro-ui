.PHONY: dev check typecheck build clean

# First-time setup: install dependencies (run from repo root for workspace linking)
dev:
	pnpm install

# Run the full quality pass: lint + format check + type check
check:
	pnpm lint
	pnpm format:check
	pnpm typecheck
	pnpm typecheck:node

# Type-check only (faster, skips lint/format)
typecheck:
	pnpm typecheck
	pnpm typecheck:node

# Production build
build:
	pnpm build

# Remove build output
clean:
	rm -rf dist out
