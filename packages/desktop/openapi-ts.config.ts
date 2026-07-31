import { defineConfig } from "@hey-api/openapi-ts"

export default defineConfig({
  input: "http://localhost:8000/openapi.json",

  output: {
    path: "src/api",
    postProcess: ["prettier"],
    // why: prettier runs on the generated files so they don't fail format:check
    // it's safe here because src/api/ is in the eslint ignores, not prettier's
  },

  plugins: [
    "@hey-api/typescript", // generates types.gen.ts
    "@hey-api/sdk",        // generates sdk.gen.ts (the service functions)
    "@hey-api/client-fetch", // why: moved from top-level `client` to plugins in v0.99
  ],
})
