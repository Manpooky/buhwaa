import React from "react"
import { useMutation } from "@tanstack/react-query"
import pako from "pako"

interface UploadProgress {
    totalFiles: number
    processedFiles: number
    currentFile: string
    currentChunk: number
    totalChunks: number
    compressionRatio: number
    uploadSpeed: number
}

interface FileMetadata {
    chunkIndex: number
    totalChunks: number
    fileName: string
    originalSize: number
    compressedSize: number
}

export function useUploadDocument() {
  const [uploadState, setUploadState] = React.useState({
    status: "idle",
    progress: {
      totalFiles: 0,
      processedFiles: 0,
      currentFile: "",
      currentChunk: 0,
      totalChunks: 0,
      compressionRatio: 0,
      uploadSpeed: 0,
    },
    jobId: null,
    error: null,
  })

  const uploadChunkMutation = useMutation({
    mutationFn: async ({
      chunk,
      metadata,
    }: {
      chunk: Uint8Array,
      metadata: FileMetadata
    }) => {
      const formData = new FormData()
      formData.append("chunk", new Blob([chunk]))
      formData.append("metadata", JSON.stringify(metadata))

      const response = await fetch("http://localhost:8000/api/upload-chunk", {
        method: "POST",
        body: formData,
      })
      if (!response.ok) throw new Error("Upload failed")
      return response.json()
    },
    onError: (error: any) => {
      setUploadState((prev) => ({
        ...prev,
        status: "error",
        error: error.message,
      }))
    },
  })

 

  async function uploadWithMetrics(file: File, onProgress: (progress: Partial<UploadProgress>) => void) {
    const chunkSize = 5 * 1024 * 1024 //5mb
    const totalChunks = Math.ceil(file.size / chunkSize)
    let totalOriginalSize = 0
    let totalCompressedSize = 0
    const startTime = Date.now()    

    for (let i = 0; i < totalChunks; i++) {
      const start = i * chunkSize
      const end = Math.min(start + chunkSize, file.size)
      const chunk = file.slice(start, end)

      //Read and compress chunk
      const chunkBuffer = await chunk.arrayBuffer()
      const chunkUint8 = new Uint8Array(chunkBuffer)
      const compressedChunk = pako.gzip(chunkUint8)

      totalOriginalSize += chunk.size
      totalCompressedSize += compressedChunk.length

      //Await mutation fn
      await uploadChunkMutation.mutateAsync({
        chunk: compressedChunk,
        metadata: {
          chunkIndex: i + 1,
          totalChunks,
          fileName: file.name,
          originalSize: chunk.size,
          compressedSize: compressedChunk.length,
        },
      })

      //Update progress
      const progress = {
        currentChunk: i + 1,
        totalChunks,
        fileName: file.name,
        compressionRatio: 1 - totalCompressedSize / totalOriginalSize,
        uploadSpeed:
          totalCompressedSize / ((Date.now() - startTime) / 1000) / 1024, //KB/s
      }

      onProgress?.(progress)
    }
  }

  async function uploadFiles(files: File[]) {
    const jobId = crypto.randomUUID()

    setUploadState((prev) => ({
      ...prev,
      status: "pending",
      progress: { ...prev.progress, totalFiles: files.length },
    }))

    try {
      for (let fileIndex = 0; fileIndex < files.length; fileIndex++) {
        const file = files[fileIndex]

        await uploadWithMetrics(file, (progress) => {
          setUploadState((prev) => ({
            ...prev,
            progress: {
              ...prev.progress,
              processedFiles: fileIndex,
              currentFile: file.name,
              ...progress,
            },
          }))
        })

        setUploadState((prev) => ({
          ...prev,
          progress: {
            ...prev.progress,
            processedFiles: fileIndex + 1,
          },
        }))
      }

    } catch (error: any) {
      setUploadState((prev) => ({
        ...prev,
        status: "error",
        error: error.message,
      }))
    }
  }

  return {
    uploadFiles,
    uploadState,
    isUploading: uploadChunkMutation.isPending,
    reset: () =>
      setUploadState({
        status: "idle",
        progress: {
          totalFiles: 0,
          processedFiles: 0,
          currentFile: "",
          currentChunk: 0,
          totalChunks: 0,
          compressionRatio: 0,
          uploadSpeed: 0,
        },
        jobId: null,
        error: null,
      }),
  }
}

