import { create } from "zustand"

interface ActiveJob {
  jobId: string | null
  projectId: string | null

  setActiveJob: (jobId: string, projectId: string) => void
  clearActiveJob: () => void
}

const useActiveJob = create<ActiveJob>()((set) => ({
  jobId: null,
  projectId: null,

  setActiveJob: (jobId, projectId) => set({ jobId, projectId }),
  clearActiveJob: () => set({ jobId: null, projectId: null }),
}))

export { useActiveJob }
