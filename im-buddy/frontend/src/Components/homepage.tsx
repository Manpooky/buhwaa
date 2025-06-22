import React, { useState } from "react";
import {
  FileText,
  Download,
  AlertCircle,
  CheckCircle,
  XIcon,
} from "lucide-react";
import DropZone from "./Dropzone"; // Assuming DropZone is correctly implemented
import { useMutation } from "@tanstack/react-query";

const ImmigrationFormAnalyzer = () => {
  const [initialFile, setInitialFile] = useState<File | null>(null);
  const [translatedFile, setTranslatedFile] = useState<File | null>(null);
  const [translatedDocumentDownloadUrl, setTranslatedDocumentDownloadUrl] =
    useState<string | null>(null);
  const [completedDocumentAnalysis, setCompletedDocumentAnalysis] =
    useState<any>(null); // This will hold the parsed data from the final analysis
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [error, setError] = useState<string>("");
  const [successMessage, setSuccessMessage] = useState<string>("");

  // Mutation for the initial document upload and translation
  const initialUploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("source_language", "english");
      formData.append("target_language", "spanish");

      const response = await fetch("http://localhost:8000/process-pdf", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload and translate the document.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      return { url, fileName: `final_${file.name}` };
    },
    onSuccess: ({ url, fileName }) => {
      setTranslatedDocumentDownloadUrl(url);
      setSuccessMessage("Translation complete! You can now download the translated document.");
      setCurrentStep(2); // Move to step 2 after successful initial upload
      setError("");
    },
    onError: (err: any) => {
      setError(err.message || "An unexpected error occurred during translation.");
      setSuccessMessage("");
    },
  });

  // Mutation for uploading the *completed* (translated and filled) document for analysis
  const finalDocumentAnalysisMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      // Assuming these languages are for the analysis API to understand the input
      formData.append("source_language", "spanish");
      formData.append("target_language", "english");

      const response = await fetch("http://localhost:8000/process-pdf", { // Assuming this endpoint now also returns analysis
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        throw new Error("Failed to upload and analyze the completed document.");
      }

      const blob = await response.blob();
      const url = window.URL.createObjectURL(blob);
      return { url, fileName: `final_${file.name}` };
    },
    onSuccess: ({ url, fileName }) => {
      setTranslatedDocumentDownloadUrl(url);
      setSuccessMessage("Translation complete! You can now download the translated document.");
      setCurrentStep(3); // Move to step 2 after successful initial upload
      setError("");
    },
    onError: (err: any) => {
      setError(err.message || "An unexpected error occurred during translation.");
      setSuccessMessage("");
    },
  });

  // Handles file selection for either initial or translated document upload
  const handleFileSelect = (acceptedFiles: File[], type: "initial" | "translated") => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      if (type === "initial") {
        setInitialFile(file);
      } else {
        setTranslatedFile(file);
      }
      setError("");
      setSuccessMessage("");
    }
  };

  // Handles the actual upload action
  const handleUpload = async (type: "initial" | "translated") => {
    setError("");
    setSuccessMessage("");

    try {
      if (type === "initial" && initialFile) {
        initialUploadMutation.mutate(initialFile);
      } else if (type === "translated" && translatedFile) {
        finalDocumentAnalysisMutation.mutate(translatedFile);
      } else {
        setError("Please select a file to upload.");
      }
    } catch (err: any) {
      // Mutations handle their own errors, but this catch block provides a fallback
      setError(err.message || "An error occurred during upload.");
    }
  };

  // Removes the selected file and resets relevant states
  const handleRemoveFile = (type: "initial" | "translated") => {
    if (type === "initial") {
      setInitialFile(null);
      setTranslatedDocumentDownloadUrl(null);
      setCompletedDocumentAnalysis(null);
      setCurrentStep(1); // Reset to step 1
    } else {
      setTranslatedFile(null);
      // If we remove the translated file, we might want to reset the analysis too
      setCompletedDocumentAnalysis(null);
    }
    setError("");
    setSuccessMessage("");
  };

  // Exports the analyzed document as JSON
  const exportAnalysis = () => {
    if (!completedDocumentAnalysis) return;

    const dataStr = JSON.stringify(completedDocumentAnalysis, null, 2);
    const dataBlob = new Blob([dataStr], { type: "application/json" });
    const url = URL.createObjectURL(dataBlob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "document-analysis.json";
    document.body.appendChild(link); // Required for Firefox
    link.click();
    document.body.removeChild(link); // Clean up
    URL.revokeObjectURL(url); // Release the object URL
  };

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Immigration Document Analyzer
          </h1>
          <p className="text-gray-600 mb-8">
            Effortlessly translate, complete, and analyze your immigration documents.
          </p>

          {/* Progress Steps */}
          <div className="flex items-center mb-8">
            <div
              className={`flex items-center ${currentStep >= 1 ? "text-blue-600" : "text-gray-400"
                }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 1 ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-600"
                  }`}
              >
                1
              </div>
              <span className="ml-2 font-medium">Upload Document</span>
            </div>
            <div className="flex-1 h-1 mx-4 bg-gray-200">
              <div
                className={`h-full ${currentStep >= 2 ? "bg-blue-600" : "bg-gray-200"
                  } transition-all duration-500 ease-in-out`}
              ></div>
            </div>
            <div
              className={`flex items-center ${currentStep >= 2 ? "text-blue-600" : "text-gray-400"
                }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 2 ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-600"
                  }`}
              >
                2
              </div>
              <span className="ml-2 font-medium text-wrap">
                Download & Complete in Your Language
              </span>
            </div>
            <div className="flex-1 h-1 mx-4 bg-gray-200">
              <div
                className={`h-full ${currentStep >= 3 ? "bg-blue-600" : "bg-gray-200"
                  } transition-all duration-500 ease-in-out`}
              ></div>
            </div>
            <div
              className={`flex items-center ${currentStep >= 3 ? "text-blue-600" : "text-gray-400"
                }`}
            >
              <div
                className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 3 ? "bg-blue-600 text-white" : "bg-gray-200 text-gray-600"
                  }`}
              >
                3
              </div>
              <span className="ml-2 font-medium">Get Analyzed Document</span>
            </div>
          </div>

          {/* Error and Success Messages */}
          {error && (
            <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center animate-fade-in">
              <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
              <span className="text-red-700">{error}</span>
            </div>
          )}

          {successMessage && (
            <div className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center animate-fade-in">
              <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
              <span className="text-green-700">{successMessage}</span>
            </div>
          )}

          {/* Step 1: Initial File Upload */}
          {currentStep === 1 && (
            <FileUpload
              title="Step 1: Upload Your Original Immigration Document (PDF)"
              description="This document will be translated into Spanish for you to fill out."
              file={initialFile}
              onFileSelect={(files) => handleFileSelect(files, "initial")}
              onRemoveFile={() => handleRemoveFile("initial")}
              onUpload={() => handleUpload("initial")}
              loading={initialUploadMutation.isPending}
            />
          )}

          {/* Step 2: Download Translated Document and Upload Completed */}
          {currentStep >= 2 && (
            <div className="mb-8 p-6 bg-white rounded-lg shadow-sm border border-gray-200">
              <h2 className="text-xl font-semibold text-gray-800 mb-4">
                Step 2: Download & Complete in Your Language
              </h2>
              <p className="text-gray-600 mb-4">
                The translated version of your document is ready. Please download it, fill it out, and then re-upload the completed document.
              </p>
              {translatedDocumentDownloadUrl && (
                <a
                  href={translatedDocumentDownloadUrl}
                  download={
                    initialFile
                      ? `translated_${initialFile.name}`
                      : "translated_document.pdf"
                  }
                  className="inline-flex items-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200"
                >
                  <Download className="w-5 h-5 mr-2" />
                  Download Translated Document
                </a>
              )}

              <hr className="my-6 border-gray-200" />

              <FileUpload
                title="Re-upload Your Completed Document (Translated)"
                description="Upload the document you've filled out in your preferred language for analysis."
                file={translatedFile}
                onFileSelect={(files) => handleFileSelect(files, "translated")}
                onRemoveFile={() => handleRemoveFile("translated")}
                onUpload={() => handleUpload("translated")}
                loading={finalDocumentAnalysisMutation.isPending}
              />
            </div>
          )}

          {/* Step 3: Final Analyzed Document Display */}
          {currentStep === 3 && completedDocumentAnalysis && (
            <div className="mb-8 p-6 bg-white rounded-lg shadow-sm border border-gray-200 animate-fade-in">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-semibold text-gray-800">
                  Step 3: Receive Your Analyzed Document
                </h2>
                <button
                  onClick={exportAnalysis}
                  className="flex items-center bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors duration-200"
                >
                  <Download className="w-4 h-4 mr-2" />
                  Export Analysis (JSON)
                </button>
              </div>

              {/* Document Metadata */}
              <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                <h3 className="font-semibold text-blue-900 mb-2">
                  Document Information
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                  <div>
                    <span className="font-medium">Title:</span>{" "}
                    {completedDocumentAnalysis?.form_metadata?.form_title || "N/A"}
                  </div>
                  <div>
                    <span className="font-medium">Form Number:</span>{" "}
                    {completedDocumentAnalysis?.form_metadata?.form_number || "N/A"}
                  </div>
                  <div>
                    <span className="font-medium">Est. Time:</span>{" "}
                    {completedDocumentAnalysis?.form_metadata?.estimated_completion_time || "N/A"}
                  </div>
                </div>
              </div>

              {/* Fields Analysis */}
              <div className="space-y-4">
                <h3 className="font-semibold text-gray-900">
                  Extracted Fields ({completedDocumentAnalysis?.fields?.length || 0})
                </h3>
                {completedDocumentAnalysis?.fields?.length > 0 ? (
                  completedDocumentAnalysis.fields.map((field: any, index: number) => (
                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h4 className="font-medium text-gray-900">
                          {field.field_name}
                        </h4>
                        <div className="flex items-center space-x-2">
                          <span
                            className={`px-2 py-1 rounded text-xs font-medium ${field.required
                                ? "bg-red-100 text-red-800"
                                : "bg-gray-100 text-gray-600"
                              }`}
                          >
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
                      {field.options && field.options.length > 0 && (
                        <div className="text-sm text-gray-500">
                          <span className="font-medium">Options:</span>
                          <ul className="list-disc list-inside mt-1">
                            {field.options.map((option: any, optIndex: number) => (
                              <li key={optIndex}>{option}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))
                ) : (
                  <p className="text-gray-600">No fields extracted for this document.</p>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ImmigrationFormAnalyzer;

interface FileUploadProps {
  title: string;
  description: string;
  file: File | null;
  onFileSelect: (files: File[]) => void;
  onRemoveFile: () => void;
  onUpload: () => void;
  loading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({
  title,
  description,
  file,
  onFileSelect,
  onRemoveFile,
  onUpload,
  loading,
}) => {
  return (
    <div className="mb-8 p-6 bg-white rounded-lg shadow-sm border border-gray-200">
      <h2 className="text-xl font-semibold text-gray-800 mb-2">{title}</h2>
      <p className="text-gray-600 mb-4">{description}</p>
      <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center bg-gray-50">
        <DropZone onFilesDrop={onFileSelect} />

        {file && (
          <div className="mt-4 p-3 bg-gray-100 rounded-md flex items-center justify-between shadow-sm">
            <div className="flex items-center">
              <FileText className="w-5 h-5 text-gray-600 mr-2" />
              <span className="text-gray-700 font-medium truncate">
                {file.name}
              </span>
            </div>
            <XIcon
              className="w-5 h-5 text-gray-500 cursor-pointer hover:text-red-500 transition-colors"
              onClick={onRemoveFile}
              aria-label={`Remove ${file.name}`}
            />
          </div>
        )}
      </div>
      <div className="flex w-full justify-end p-2">
        <button
          onClick={onUpload}
          disabled={!file || loading}
          className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors duration-200 disabled:opacity-50 disabled:cursor-not-allowed shadow-md"
        >
          {loading ? "Processing..." : "Upload Document"}
        </button>
      </div>
    </div>
  );
};