import { Upload } from "lucide-react"
import { useDropzone } from "react-dropzone"

export default function DropZone({ onFilesDrop }: { onFilesDrop: (files: File[]) => void }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: onFilesDrop,
    accept: {
      "text/*": [".pdf", ".png", ".jpg", ".jpeg"],
      "application/json": [".json"],
    },
    maxSize: 10 * 1024 * 1024, // 10MB per file
    multiple: true,
  })

  return (
    <div
      {...getRootProps()}
      className={`dropzone bg-accent/70 hover:bg-accent cursor-pointer p-20 group ${isDragActive ? "drag-active" : ""}`}>
      <input {...getInputProps()} />
        <div className="flex flex-col gap-2">
        <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4 group-hover:text-gray-500" />
        <p className="text-gray-500 group-hover:text-gray-600">
                Upload PDF or image files (JPG, PNG) of immigration forms
            </p>
        </div>
    </div>
  )
}

