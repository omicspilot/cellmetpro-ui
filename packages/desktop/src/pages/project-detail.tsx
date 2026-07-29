import { useParams } from "react-router-dom"

export default function ProjectDetailPage() {
  const params = useParams()

  return (
    <div>
      <h1>project id:</h1>
      <span>{params.projectId}</span>
    </div>
  )
}
