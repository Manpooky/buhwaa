import React, { useState, useCallback } from "react";
import {
  FileText,
  Download,
  AlertCircle,
  CheckCircle,
  XIcon,
  UploadCloud,
  Loader2,
} from "lucide-react";
import { useDropzone } from "react-dropzone";
import { useMutation } from "@tanstack/react-query";
import { motion, AnimatePresence, Variants } from "framer-motion";
import clsx from "clsx";

// CORRECTED HELPER FOR ANIMATIONS
const stepAnimation: Variants = {
  initial: {
    opacity: 0,
    y: 20,
  },
  animate: {
    opacity: 1,
    y: 0,
    transition: {
      duration: 0.4,
      ease: "easeInOut",
    },
  },
  exit: {
    opacity: 0,
    y: -20,
    transition: {
      duration: 0.3,
      ease: "easeInOut",
    },
  },
};

const ImmigrationFormAnalyzer = () => {
  const [initialFile, setInitialFile] = useState<File | null>(null);
  const [translatedFile, setTranslatedFile] = useState<File | null>(null);
  const [translatedDocumentDownloadUrl, setTranslatedDocumentDownloadUrl] =
    useState<string | null>(null);
  // NEW: State to hold the URL for the final generated PDF
  const [finalDocumentDownloadUrl, setFinalDocumentDownloadUrl] = useState<
    string | null
  >(null);
  const [currentStep, setCurrentStep] = useState<number>(1);
  const [error, setError] = useState<string>("");
  const [successMessage, setSuccessMessage] = useState<string>("");

  const initialUploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("source_language", "English");
      formData.append("target_language", "Spanish");

      // Your backend endpoint that returns a PDF file
      const response = await fetch("http://localhost:8000/process-pdf", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        // Try to parse a JSON error message from the backend, otherwise throw a generic error
        const errorData = await response
          .json()
          .catch(() => ({ detail: "Failed to generate the final PDF." }));
        throw new Error(errorData.detail);
      }

      // Process the response as a PDF blob
      const blob = await response.blob();
      if (blob.type !== "application/pdf") {
        console.error("Received content-type:", blob.type);
        throw new Error(
          "An error occurred. The server did not return a valid PDF file."
        );
      }
      const url = window.URL.createObjectURL(blob);
      return { url, fileName: `final_analysis_${file.name}` };
    },
    onSuccess: ({ url }) => {
      setTranslatedDocumentDownloadUrl(url); 
      setSuccessMessage("Your translated document is ready for download!");
      setCurrentStep(2);
      setError("");
    },
    onError: (err: any) => {
      setError(err.message || "An error occurred during the translation.");
      setSuccessMessage("");
    },
  });

  // CHANGED: This mutation now expects a PDF in response
  const finalUploadMutation = useMutation({
    mutationFn: async (file: File) => {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("source_language", "English");
      formData.append("target_language", "Spanish");

      // Your backend endpoint that returns a PDF file
      const response = await fetch("http://localhost:8000/process-pdf", {
        method: "POST",
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response
          .json()
          .catch(() => ({ detail: "Failed to generate the final PDF." }));
        throw new Error(errorData.detail);
      }

      // Process the response as a PDF blob
      const blob = await response.blob();
      if (blob.type !== "application/pdf") {
        console.error("Received content-type:", blob.type);
        throw new Error(
          "An error occurred. The server did not return a valid PDF file."
        );
      }
      const url = window.URL.createObjectURL(blob);
      return { url, fileName: `final_analysis_${file.name}` };
    },
    onSuccess: ({ url }) => {
      setFinalDocumentDownloadUrl(url); 
      setSuccessMessage("Your final document is ready for download!");
      setCurrentStep(3);
      setError("");
    },
    onError: (err: any) => {
      setError(err.message || "An error occurred during the final analysis.");
      setSuccessMessage("");
    },
  });

  const handleFileSelect = (
    acceptedFiles: File[],
    type: "initial" | "translated"
  ) => {
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      if (type === "initial") setInitialFile(file);
      else setTranslatedFile(file);
      setError("");
      setSuccessMessage("");
    }
  };

  const handleUpload = async (type: "initial" | "translated") => {
    setError("");
    setSuccessMessage("");
    if (type === "initial" && initialFile) {
      initialUploadMutation.mutate(initialFile);
    } else if (type === "translated" && translatedFile) {
      finalUploadMutation.mutate(translatedFile);
    }
  };

  const handleRemoveFile = (type: "initial" | "translated") => {
    if (type === "initial") {
      setInitialFile(null);
      setTranslatedDocumentDownloadUrl(null);
      setFinalDocumentDownloadUrl(null); 
      setCurrentStep(1);
    } else {
      setTranslatedFile(null);
      setFinalDocumentDownloadUrl(null); 
      // If we were on step 3, go back to step 2 to allow a new upload
      if (currentStep === 3) {
        setCurrentStep(2);
      }
    }
    setError("");
    setSuccessMessage("");
  };

  const steps = [
    { number: 1, title: "Upload Document" },
    { number: 2, title: "Download & Complete" },
    { number: 3, title: "Get Final PDF" }, // Changed title
  ];

  return (
    <div className="min-h-screen bg-gray-100 font-sans p-4 sm:p-8">
      <div className="max-w-5xl mx-auto">
        <div className="bg-white rounded-2xl shadow-xl p-6 sm:p-10">
          <header className="text-center mb-10">
            <h1 className="text-4xl font-bold text-gray-900 mb-2">
              Immigration Document Assistant
            </h1>
            <p className="text-lg text-gray-600">
              Effortlessly translate and complete your immigration
              documents.
            </p>
          </header>

          {/* Animated Progress Steps */}
          <div className="flex items-center mb-12">
            {steps.map((step, index) => (
              <React.Fragment key={step.number}>
                <div className="flex flex-col items-center text-center">
                  <motion.div
                    className={clsx(
                      "w-10 h-10 rounded-full flex items-center justify-center font-bold text-lg transition-all duration-300",
                      currentStep > step.number
                        ? "bg-green-500 text-white"
                        : "",
                      currentStep === step.number
                        ? "bg-blue-600 text-white scale-110"
                        : "",
                      currentStep < step.number
                        ? "bg-gray-200 text-gray-500"
                        : ""
                    )}
                    animate={{ scale: currentStep === step.number ? 1.1 : 1 }}
                  >
                    <AnimatePresence>
                      {currentStep > step.number ? (
                        <motion.div
                          initial={{ scale: 0 }}
                          animate={{ scale: 1 }}
                        >
                          <CheckCircle size={24} />
                        </motion.div>
                      ) : (
                        <span>{step.number}</span>
                      )}
                    </AnimatePresence>
                  </motion.div>
                  <p
                    className={clsx(
                      "mt-2 text-sm font-medium w-24",
                      currentStep >= step.number
                        ? "text-blue-600"
                        : "text-gray-500"
                    )}
                  >
                    {step.title}
                  </p>
                </div>
                {index < steps.length - 1 && (
                  <div className="flex-1 h-1 mx-4 bg-gray-200 rounded-full">
                    <motion.div
                      className="h-full bg-blue-600 rounded-full"
                      initial={{ width: 0 }}
                      animate={{
                        width: currentStep > step.number ? "100%" : "0%",
                      }}
                      transition={{ duration: 0.5, ease: "circOut" }}
                    />
                  </div>
                )}
              </React.Fragment>
            ))}
          </div>

          {/* Messages */}
          <AnimatePresence>
            {error && (
              <motion.div
                className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center"
                {...stepAnimation}
              >
                <AlertCircle className="w-5 h-5 text-red-500 mr-3 flex-shrink-0" />
                <span className="text-red-700">{error}</span>
              </motion.div>
            )}
            {successMessage && (
              <motion.div
                className="mb-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center"
                {...stepAnimation}
              >
                <CheckCircle className="w-5 h-5 text-green-500 mr-3 flex-shrink-0" />
                <span className="text-green-700">{successMessage}</span>
              </motion.div>
            )}
          </AnimatePresence>

          {/* Step Content */}
          <main>
            <AnimatePresence mode="wait">
              {currentStep === 1 && (
                <motion.div key="step1" {...stepAnimation}>
                  <FileUpload
                    title="Step 1: Upload Your Original Immigration Document"
                    description="This document will be translated into Spanish for you to fill out."
                    file={initialFile}
                    onFileSelect={(files) => handleFileSelect(files, "initial")}
                    onRemoveFile={() => handleRemoveFile("initial")}
                    onUpload={() => handleUpload("initial")}
                    loading={initialUploadMutation.isPending}
                  />
                </motion.div>
              )}

              {currentStep === 2 && (
                <motion.div key="step2" {...stepAnimation}>
                  <div className="p-6 bg-gray-50 rounded-lg border border-gray-200">
                    <h2 className="text-xl font-semibold text-gray-800 mb-3">
                      Download & Re-upload
                    </h2>
                    <p className="text-gray-600 mb-6">
                      Download the translated document, fill it out completely,
                      and then upload the completed version for final translation.
                    </p>
                    {translatedDocumentDownloadUrl && (
                      <a
                        href={translatedDocumentDownloadUrl}
                        download={`translated_${
                          initialFile?.name || "document.pdf"
                        }`}
                        className="inline-flex items-center justify-center px-6 py-3 border border-transparent text-base font-medium rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-all duration-200 transform hover:scale-105"
                      >
                        <Download className="w-5 h-5 mr-2" />
                        Download Translated Document
                      </a>
                    )}
                    <hr className="my-8 border-gray-300" />
                    <FileUpload
                      title="Upload Your Completed Document"
                      description="Upload the translated PDF you have filled out."
                      file={translatedFile}
                      onFileSelect={(files) =>
                        handleFileSelect(files, "translated")
                      }
                      onRemoveFile={() => handleRemoveFile("translated")}
                      onUpload={() => handleUpload("translated")}
                      loading={finalUploadMutation.isPending}
                    />
                  </div>
                </motion.div>
              )}

              {/* NEW: Final step UI for downloading the PDF */}
              {currentStep === 3 && finalDocumentDownloadUrl && (
                <motion.div key="step3" {...stepAnimation}>
                  <div className="p-8 bg-gray-50 rounded-lg border border-gray-200 text-center">
                    <div className="w-16 h-16 bg-green-100 rounded-full mx-auto flex items-center justify-center mb-5">
                        <CheckCircle className="w-10 h-10 text-green-600" />
                    </div>
                    <h2 className="text-2xl font-semibold text-gray-800 mb-3">
                      Your Document is Ready
                    </h2>
                    <p className="text-gray-600 mb-8 max-w-md mx-auto">
                      The final PDF document has been generated. Click the
                      button below to download it.
                    </p>
                    <a
                      href={finalDocumentDownloadUrl}
                      download={
                        translatedFile
                          ? `final_${translatedFile.name}`
                          : "final_document.pdf"
                      }
                      className="inline-flex items-center justify-center px-8 py-4 border border-transparent text-lg font-medium rounded-md shadow-sm text-white bg-green-600 hover:bg-green-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500 transition-all duration-200 transform hover:scale-105"
                    >
                      <Download className="w-6 h-6 mr-3" />
                      Download Final PDF
                    </a>
                  </div>
                </motion.div>
              )}
            </AnimatePresence>
          </main>
        </div>
      </div>
    </div>
  );
};

// --- FileUpload Sub-component (Unchanged) --- //
interface FileUploadProps {
    title: string;
    description: string;
    file: File | null;
    onFileSelect: (files: File[]) => void;
    onRemoveFile: () => void;
    onUpload: () => void;
    loading: boolean;
}

const FileUpload: React.FC<FileUploadProps> = ({ title, description, file, onFileSelect, onRemoveFile, onUpload, loading }) => {
    const onDrop = useCallback((acceptedFiles: File[]) => {
        onFileSelect(acceptedFiles);
    }, [onFileSelect]);

    const { getRootProps, getInputProps, isDragActive } = useDropzone({
        onDrop,
        accept: { 'application/pdf': ['.pdf'] },
        multiple: false,
    });

    return (
        <div className="p-6 bg-white rounded-lg">
            <h3 className="text-xl font-semibold text-gray-800 mb-1">{title}</h3>
            <p className="text-gray-600 mb-4">{description}</p>
            
            <div
                {...getRootProps()}
                className={clsx(
                    "border-2 border-dashed rounded-xl p-8 text-center cursor-pointer transition-all duration-300",
                    isDragActive ? "border-blue-500 bg-blue-50" : "border-gray-300 bg-gray-50 hover:border-gray-400"
                )}
            >
                <input {...getInputProps()} />
                <div className="flex flex-col items-center justify-center text-gray-500">
                    <UploadCloud className={clsx("w-12 h-12 mb-4 transition-transform", isDragActive ? "scale-110 text-blue-600" : "")} />
                    {isDragActive ? (
                        <p className="text-lg font-semibold text-blue-600">Drop the file here...</p>
                    ) : (
                        <p className="text-lg">Drag & drop a PDF here, or <span className="font-semibold text-blue-600">click to select</span></p>
                    )}
                    <p className="text-sm mt-1">Maximum file size: 10MB</p>
                </div>
            </div>

            <AnimatePresence>
                {file && (
                    <motion.div
                        className="mt-4 p-3 bg-gray-100 rounded-lg flex items-center justify-between shadow-sm"
                        initial={{ opacity: 0, y: 10 }}
                        animate={{ opacity: 1, y: 0 }}
                        exit={{ opacity: 0, y: -10 }}
                    >
                        <div className="flex items-center overflow-hidden">
                            <FileText className="w-5 h-5 text-blue-600 mr-3 flex-shrink-0" />
                            <span className="text-gray-800 font-medium truncate">{file.name}</span>
                        </div>
                        <button onClick={onRemoveFile} className="p-1 rounded-full hover:bg-red-100">
                            <XIcon className="w-5 h-5 text-gray-500 hover:text-red-600 transition-colors" />
                        </button>
                    </motion.div>
                )}
            </AnimatePresence>
            
            <div className="flex justify-end mt-6">
                <motion.button
                    onClick={onUpload}
                    disabled={!file || loading}
                    className="inline-flex items-center justify-center w-48 h-12 bg-blue-600 text-white px-6 py-2 rounded-lg font-semibold shadow-md transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                    whileHover={{ scale: !loading && file ? 1.05 : 1 }}
                    whileTap={{ scale: !loading && file ? 0.95 : 1 }}
                >
                    {loading ? (
                        <Loader2 className="w-6 h-6 animate-spin" />
                    ) : (
                        "Upload Document"
                    )}
                </motion.button>
            </div>
        </div>
    );
};

export default ImmigrationFormAnalyzer;