import { create } from "zustand"

interface ConnectionStore {
  // state
  serverUrl: string
  status: "idle" | "checking" | "connected" | "error"
  errorMessage: string | null

  // actions
  setServerUrl: (url: string) => void
  setStatus: (status: ConnectionStore["status"], error?: string) => void
}

const useConnectionStore = create<ConnectionStore>()((set) => ({
  serverUrl: import.meta.env.VITE_API_URL ?? "http://localhost:8000",
  status: "idle",
  errorMessage: null,

  setServerUrl: (url) =>
    set({
      serverUrl: url,
      status: "idle",
      errorMessage: null,
    }),

  setStatus: (status, error) =>
    set({
      status,
      errorMessage: error ?? null,
    }),
}))

export { useConnectionStore }
