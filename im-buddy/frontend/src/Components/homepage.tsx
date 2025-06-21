import React, { useState } from "react"
import {
  FileText,
  Download,
  AlertCircle,
  CheckCircle,
  XIcon,
} from "lucide-react"
import DropZone from "./Dropzone"

const ImmigrationFormAnalyzer = () => {
  const [files, setFiles] = useState<File[] | null>(null)
  const [translatedDocument, setTranslatedDocument] = useState<string>("")
  const [completedDocument, setCompletedDocument] = useState<any>(null)
  const [loading, setLoading] = useState<boolean>(false)
  const [currentStep, setCurrentStep] = useState<number>(1)
  const [error, setError] = useState<string>("")

  // Simulated Llama 4 analysis function
  const analyzeWithLlama4 = async (file: File) => {
    await new Promise((resolve) => setTimeout(resolve, 3000))
  }

  const handleDocumentInput = (files: File[]) => {
    console.log("file name", files[0].name)
    if (files[0]) {
      setFiles(files)
      setError("")
      setCurrentStep(1)
      setTranslatedDocument("")
      setCompletedDocument(null)
    }
  }

  const handleDocumentUpload = async (files: File[]) => {
    if (!files.length) return

    setLoading(true)
    setError("")

    try {
      const result = await analyzeWithLlama4(files[0])
      setCompletedDocument(result)
      setCurrentStep(3)
    } catch (err) {
      setError("Failed to analyze form. Please try again.")
    } finally {
      setLoading(false)
    }
  }

  const handleRemoveFile = () => {
    setFiles(prev => prev?.slice(1) || null)
    setCurrentStep(1)
  }

  const exportAnalysis = () => {
    if (!completedDocument) return

    const dataStr = JSON.stringify(completedDocument, null, 2)
    const dataBlob = new Blob([dataStr], { type: "application/json" })
    const url = URL.createObjectURL(dataBlob)
    const link = document.createElement("a")
    link.href = url
    link.download = "form-analysis.json"
    link.click()
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Immigration Form Analyzer
          </h1>
          <p className="text-gray-600 mb-8">
            Phase 1: Upload your immigration form
          </p>

          {/* Progress Steps */}
          <div className="flex items-center mb-8">
            <div
              className={`flex items-center ${
                currentStep >= 1 ? "text-blue-600" : "text-gray-400"
              }`}>
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  currentStep >= 1 ? "bg-blue-600 text-white" : "bg-gray-200"
                }`}>
                1
              </div>
              <span className="ml-2 font-medium">Upload Document</span>
            </div>
            <div className="flex-1 h-1 mx-4 bg-gray-200">
              <div
                className={`h-full ${
                  currentStep >= 2 ? "bg-blue-600" : "bg-gray-200"
                } transition-all`}></div>
            </div>
            <div
              className={`flex items-center ${
                currentStep >= 2 ? "text-blue-600" : "text-gray-400"
              }`}>
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  currentStep >= 2 ? "bg-blue-600 text-white" : "bg-gray-200"
                }`}>
                2
              </div>
              <span className="ml-2 font-medium">
                Fill out the document in your language
              </span>
            </div>
            <div className="flex-1 h-1 mx-4 bg-gray-200">
              <div
                className={`h-full ${
                  currentStep >= 3 ? "bg-blue-600" : "bg-gray-200"
                } transition-all`}></div>
            </div>
            <div
              className={`flex items-center ${
                currentStep >= 3 ? "text-blue-600" : "text-gray-400"
              }`}>
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${
                  currentStep >= 3 ? "bg-blue-600 text-white" : "bg-gray-200"
                }`}>
                3
              </div>
              <span className="ml-2 font-medium">
                We return the document in the needed language
              </span>
            </div>
          </div>

          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
              <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
              <span className="text-red-700">{error}</span>
            </div>
          )}

          {/* Step 1: File Upload */}
          <FileUpload
            files={files}
            handleDocumentInput={handleDocumentInput}
            handleDocumentUpload={handleDocumentUpload}
            handleRemoveFile={handleRemoveFile}
            loading={loading}
          />

          {/* Step 2: Translated Document */}
          {translatedDocument && (
            <div className="mb-8">
              <h2 className="text-xl font-semibold mb-4">
                Step 2: Fill out form in your language
              </h2>
              <div className="bg-gray-50 border rounded-lg p-4 max-h-64 overflow-y-auto">
                <pre className="text-sm text-gray-700 whitespace-pre-wrap">
                  {translatedDocument}
                </pre>
              </div>
              {currentStep === 2 && (
                <FileUpload
                  files={files}
                  handleDocumentInput={handleDocumentInput}
                  handleDocumentUpload={handleDocumentUpload}
                  handleRemoveFile={handleRemoveFile}
                  loading={loading}
                />
              )}
            </div>
          )}

          {/* Step 3: Final Document */}
          {completedDocument && (
            <div className="mb-8">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold">
                  Step 3: Recieve Your Form in Desired Language
                </h2>
                <button
                  onClick={exportAnalysis}
                  className="flex items-center bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors">
                  <Download className="w-4 h-4 mr-2" />
                  Export JSON
                </button>
              </div>

              {/* Form Metadata */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <h3 className="font-semibold text-blue-900 mb-2">
                  Form Information
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Title:</span>{" "}
                    {completedDocument.form_metadata.form_title}
                  </div>
                  <div>
                    <span className="font-medium">Form Number:</span>{" "}
                    {completedDocument.form_metadata.form_number}
                  </div>
                  <div>
                    <span className="font-medium">Est. Time:</span>{" "}
                    {completedDocument.form_metadata.estimated_completion_time}
                  </div>
                </div>
              </div>

              {/* Fields Analysis */}
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">
                  Extracted Fields ({completedDocument.fields.length})
                </h3>
                {completedDocument.fields.map((field: any, index: number) => (
                  <div
                    key={index}
                    className="border border-gray-200 rounded-lg p-4">
                    <div className="flex items-center justify-between mb-2">
                      <h4 className="font-medium text-gray-900">
                        {field.field_name}
                      </h4>
                      <div className="flex items-center space-x-2">
                        <span
                          className={`px-2 py-1 rounded text-xs font-medium ${
                            field.required
                              ? "bg-red-100 text-red-800"
                              : "bg-gray-100 text-gray-600"
                          }`}>
                          {field.required ? "Required" : "Optional"}
                        </span>
                        <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                          {field.data_type}
                        </span>
                      </div>
                    </div>
                    <p className="text-gray-600 mb-2">{field.description}</p>
                    {field.validation_rules && (
                      <p className="text-sm text-gray-500 mb-1">
                        <span className="font-medium">Validation:</span>{" "}
                        {field.validation_rules}
                      </p>
                    )}
                    {field.conditional_logic &&
                      field.conditional_logic !== "None" && (
                        <p className="text-sm text-gray-500 mb-1">
                          <span className="font-medium">Conditions:</span>{" "}
                          {field.conditional_logic}
                        </p>
                      )}
                    {field.options.length > 0 && (
                      <div className="text-sm text-gray-500">
                        <span className="font-medium">Options:</span>
                        <ul className="list-disc list-inside mt-1">
                          {field.options.map(
                            (option: any, optIndex: number) => (
                              <li key={optIndex}>{option}</li>
                            )
                          )}
                        </ul>
                      </div>
                    )}
                  </div>
                ))}
              </div>

              <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center">
                <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
                <span className="text-green-700">
                  Form upload complete! Ready for Phase 2
                </span>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default ImmigrationFormAnalyzer

function FileUpload({
  files,
  handleDocumentInput,
  handleDocumentUpload,
  handleRemoveFile,
  loading,
}: {
  files: File[] | null
  handleDocumentInput: (files: File[]) => void
  handleDocumentUpload: (files: File[]) => void
  handleRemoveFile: () => void
  loading: boolean
}) {

  return (
    <div className="mb-8">
      <h2 className="text-xl font-semibold mb-4">
        Step 1: Upload Immigration Form
      </h2>
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
        <DropZone onFilesDrop={handleDocumentInput} />

        {files && files.length > 0 && (
          <div className="mt-4 p-3 bg-gray-50 rounded flex items-center justify-center">
            <XIcon className="w-5 h-5 text-gray-600 mr-2 cursor-pointer" onClick={() => handleRemoveFile()} />
            <FileText className="w-5 h-5 text-gray-600 mr-2" />
            <span className="text-gray-700">{files[0]?.name || ""}</span>
          </div>
        )}
      </div>
      {files && files.length > 0 && (
        <div className="flex w-full justify-end p-2">
          <button
            onClick={() => handleDocumentUpload(files)}
            disabled={loading}
            className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50 cursor-pointer">
            {loading ? "Uploading..." : "Upload"}
          </button>
        </div>
      )}
    </div>
  )
}
