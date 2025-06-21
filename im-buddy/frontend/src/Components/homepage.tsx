import React, { useState } from 'react';
import { Upload, FileText, Download, AlertCircle, CheckCircle } from 'lucide-react';
import { useUploadDocument } from '../Hooks/useUploadDocument';

const ImmigrationFormAnalyzer = () => {
    const { uploadDocument, uploadState } = useUploadDocument()
    const [file, setFile] = useState<File | null>(null);
    const [extractedText, setExtractedText] = useState<string>('');
    const [analysisResult, setAnalysisResult] = useState<any>(null);
    const [loading, setLoading] = useState<boolean>(false);
    const [currentStep, setCurrentStep] = useState<number>(1);
    const [error, setError] = useState<string>('');

    // Simulated OCR/Text extraction function
    const extractTextFromFile = async (file: File) => {
        // In real implementation, you'd use actual OCR libraries
        // For demo purposes, we'll simulate this
        await new Promise(resolve => setTimeout(resolve, 2000));

        // Simulated extracted text from an immigration form
        return `UNITED STATES CITIZENSHIP AND IMMIGRATION SERVICES
FORM I-485 - APPLICATION TO ADJUST STATUS TO PERMANENT RESIDENT

PART 1: INFORMATION ABOUT YOU

1. Family Name (Last Name): _______________
2. Given Name (First Name): _______________  
3. Middle Name: _______________
4. Other Names Used: _______________
5. Date of Birth (mm/dd/yyyy): _______________
6. Country of Birth: _______________
7. Country of Citizenship or Nationality: _______________
8. U.S. Social Security Number (if any): _______________
9. USCIS Online Account Number (if any): _______________

PART 2: APPLICATION TYPE OR FILING CATEGORY

1. I am applying for adjustment of status because:
   a. [ ] An immigrant petition giving me an immediately available immigrant visa number that has been approved
   b. [ ] My spouse or parent applied for adjustment of status or was granted lawful permanent residence
   c. [ ] I entered as a K-1 fiancé(e) of a U.S. citizen whom I married within 90 days
   
2. Priority Date (if any): _______________

PART 3: PROCESSING INFORMATION

1. Current Immigration Status: _______________
2. Date of Last Arrival into the United States: _______________
3. Place of Last Arrival into the United States: _______________
4. Arrival/Departure Record (I-94) Number: _______________`;
    };

    // Simulated Llama 4 analysis function
    const analyzeWithLlama4 = async (text: string) => {
        await new Promise(resolve => setTimeout(resolve, 3000));

        return {
            fields: [
                {
                    field_name: "family_name",
                    description: "Last name or surname of the applicant",
                    data_type: "text",
                    required: true,
                    validation_rules: "Letters only, no special characters",
                    conditional_logic: "None",
                    options: []
                },
                {
                    field_name: "given_name",
                    description: "First name of the applicant",
                    data_type: "text",
                    required: true,
                    validation_rules: "Letters only, no special characters",
                    conditional_logic: "None",
                    options: []
                },
                {
                    field_name: "middle_name",
                    description: "Middle name of the applicant",
                    data_type: "text",
                    required: false,
                    validation_rules: "Letters only, no special characters if provided",
                    conditional_logic: "None",
                    options: []
                },
                {
                    field_name: "other_names",
                    description: "Any other names previously used by the applicant",
                    data_type: "text",
                    required: false,
                    validation_rules: "Letters only, multiple names separated by commas",
                    conditional_logic: "None",
                    options: []
                },
                {
                    field_name: "date_of_birth",
                    description: "Date of birth in MM/DD/YYYY format",
                    data_type: "date",
                    required: true,
                    validation_rules: "Must be valid date in MM/DD/YYYY format, applicant must be at least 18 years old",
                    conditional_logic: "None",
                    options: []
                },
                {
                    field_name: "country_of_birth",
                    description: "Country where the applicant was born",
                    data_type: "text",
                    required: true,
                    validation_rules: "Must be a valid country name",
                    conditional_logic: "None",
                    options: []
                },
                {
                    field_name: "country_of_citizenship",
                    description: "Country of current citizenship or nationality",
                    data_type: "text",
                    required: true,
                    validation_rules: "Must be a valid country name",
                    conditional_logic: "None",
                    options: []
                },
                {
                    field_name: "ssn",
                    description: "U.S. Social Security Number if available",
                    data_type: "text",
                    required: false,
                    validation_rules: "Must be 9 digits in format XXX-XX-XXXX if provided",
                    conditional_logic: "Only required if applicant has been assigned an SSN",
                    options: []
                },
                {
                    field_name: "application_type",
                    description: "Reason for applying for adjustment of status",
                    data_type: "select",
                    required: true,
                    validation_rules: "Must select one option",
                    conditional_logic: "Different supporting documents required based on selection",
                    options: [
                        "Immigrant petition with available visa number",
                        "Spouse/parent adjustment application",
                        "K-1 fiancé(e) marriage within 90 days"
                    ]
                },
                {
                    field_name: "priority_date",
                    description: "Priority date from approved immigrant petition",
                    data_type: "date",
                    required: false,
                    validation_rules: "Must be valid date in MM/DD/YYYY format if provided",
                    conditional_logic: "Required only if application type is based on immigrant petition",
                    options: []
                }
            ],
            form_metadata: {
                form_title: "Application to Adjust Status to Permanent Resident",
                form_number: "I-485",
                estimated_completion_time: "60-90 minutes"
            }
        };
    };

    const handleFileUpload = (event: React.ChangeEvent<HTMLInputElement>) => {
        const uploadedFile = event.target.files?.[0];
        if (uploadedFile) {
            setFile(uploadedFile as File);
            setError('');
            setCurrentStep(1);
            setExtractedText('');
            setAnalysisResult(null);
        }
    };

    const handleExtractText = async () => {
        if (!file) return;

        setLoading(true);
        setError('');

        try {
            const text = await extractTextFromFile(file);
            setExtractedText(text);
            setCurrentStep(2);
        } catch (err) {
            setError('Failed to extract text from file. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const handleAnalyzeForm = async () => {
        if (!extractedText) return;

        setLoading(true);
        setError('');

        try {
            const result = await analyzeWithLlama4(extractedText);
            setAnalysisResult(result);
            setCurrentStep(3);
        } catch (err) {
            setError('Failed to analyze form. Please try again.');
        } finally {
            setLoading(false);
        }
    };

    const exportAnalysis = () => {
        if (!analysisResult) return;

        const dataStr = JSON.stringify(analysisResult, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);
        const link = document.createElement('a');
        link.href = url;
        link.download = 'form-analysis.json';
        link.click();
    };

    return (
        <div className="min-h-screen bg-gray-50 py-8">
            <div className="max-w-6xl mx-auto px-4">
                <div className="bg-white rounded-lg shadow-lg p-8">
                    <h1 className="text-3xl font-bold text-gray-900 mb-2">
                        Immigration Form Analyzer
                    </h1>
                    <p className="text-gray-600 mb-8">
                        Phase 1: Upload an immigration form to extract and analyze all required fields
                    </p>

                    {/* Progress Steps */}
                    <div className="flex items-center mb-8">
                        <div className={`flex items-center ${currentStep >= 1 ? 'text-blue-600' : 'text-gray-400'}`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 1 ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
                                1
                            </div>
                            <span className="ml-2 font-medium">Upload Document</span>
                        </div>
                        <div className="flex-1 h-1 mx-4 bg-gray-200">
                            <div className={`h-full ${currentStep >= 2 ? 'bg-blue-600' : 'bg-gray-200'} transition-all`}></div>
                        </div>
                        <div className={`flex items-center ${currentStep >= 2 ? 'text-blue-600' : 'text-gray-400'}`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 2 ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
                                2
                            </div>
                            <span className="ml-2 font-medium">Extract Text</span>
                        </div>
                        <div className="flex-1 h-1 mx-4 bg-gray-200">
                            <div className={`h-full ${currentStep >= 3 ? 'bg-blue-600' : 'bg-gray-200'} transition-all`}></div>
                        </div>
                        <div className={`flex items-center ${currentStep >= 3 ? 'text-blue-600' : 'text-gray-400'}`}>
                            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${currentStep >= 3 ? 'bg-blue-600 text-white' : 'bg-gray-200'}`}>
                                3
                            </div>
                            <span className="ml-2 font-medium">Analyze Fields</span>
                        </div>
                    </div>

                    {error && (
                        <div className="mb-6 p-4 bg-red-50 border border-red-200 rounded-lg flex items-center">
                            <AlertCircle className="w-5 h-5 text-red-500 mr-2" />
                            <span className="text-red-700">{error}</span>
                        </div>
                    )}

                    {/* Step 1: File Upload */}
                    <div className="mb-8">
                        <h2 className="text-xl font-semibold mb-4">Step 1: Upload Immigration Form</h2>
                        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center">
                            <Upload className="w-12 h-12 text-gray-400 mx-auto mb-4" />
                            <div className="mb-4">
                                <label htmlFor="file-upload" className="cursor-pointer">
                  <span className="bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors">
                    Choose File
                  </span>
                                    <input
                                        id="file-upload"
                                        type="file"
                                        accept=".pdf,.jpg,.jpeg,.png"
                                        onChange={handleFileUpload}
                                        className="hidden"
                                    />
                                </label>
                            </div>
                            <p className="text-gray-500">
                                Upload PDF or image files (JPG, PNG) of immigration forms
                            </p>
                            {file && (
                                <div className="mt-4 p-3 bg-gray-50 rounded flex items-center justify-center">
                                    <FileText className="w-5 h-5 text-gray-600 mr-2" />
                                    <span className="text-gray-700">{file.name}</span>
                                </div>
                            )}
                        </div>
                        {file && currentStep === 1 && (
                            <button
                                onClick={handleExtractText}
                                disabled={loading}
                                className="mt-4 bg-blue-600 text-white px-6 py-2 rounded-lg hover:bg-blue-700 transition-colors disabled:opacity-50"
                            >
                                {loading ? 'Extracting Text...' : 'Extract Text'}
                            </button>
                        )}
                    </div>

                    {/* Step 2: Extracted Text */}
                    {extractedText && (
                        <div className="mb-8">
                            <h2 className="text-xl font-semibold mb-4">Step 2: Extracted Text</h2>
                            <div className="bg-gray-50 border rounded-lg p-4 max-h-64 overflow-y-auto">
                                <pre className="text-sm text-gray-700 whitespace-pre-wrap">{extractedText}</pre>
                            </div>
                            {currentStep === 2 && (
                                <button
                                    onClick={handleAnalyzeForm}
                                    disabled={loading}
                                    className="mt-4 bg-green-600 text-white px-6 py-2 rounded-lg hover:bg-green-700 transition-colors disabled:opacity-50"
                                >
                                    {loading ? 'Analyzing with Llama 4...' : 'Analyze Form Fields'}
                                </button>
                            )}
                        </div>
                    )}

                    {/* Step 3: Analysis Results */}
                    {analysisResult && (
                        <div className="mb-8">
                            <div className="flex items-center justify-between mb-4">
                                <h2 className="text-xl font-semibold">Step 3: Field Analysis Results</h2>
                                <button
                                    onClick={exportAnalysis}
                                    className="flex items-center bg-gray-600 text-white px-4 py-2 rounded-lg hover:bg-gray-700 transition-colors"
                                >
                                    <Download className="w-4 h-4 mr-2" />
                                    Export JSON
                                </button>
                            </div>

                            {/* Form Metadata */}
                            <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                                <h3 className="font-semibold text-blue-900 mb-2">Form Information</h3>
                                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                                    <div>
                                        <span className="font-medium">Title:</span> {analysisResult.form_metadata.form_title}
                                    </div>
                                    <div>
                                        <span className="font-medium">Form Number:</span> {analysisResult.form_metadata.form_number}
                                    </div>
                                    <div>
                                        <span className="font-medium">Est. Time:</span> {analysisResult.form_metadata.estimated_completion_time}
                                    </div>
                                </div>
                            </div>

                            {/* Fields Analysis */}
                            <div className="space-y-4">
                                <h3 className="font-semibold text-gray-900">Extracted Fields ({analysisResult.fields.length})</h3>
                                {analysisResult.fields.map((field: any, index: number) => (
                                    <div key={index} className="border border-gray-200 rounded-lg p-4">
                                        <div className="flex items-center justify-between mb-2">
                                            <h4 className="font-medium text-gray-900">{field.field_name}</h4>
                                            <div className="flex items-center space-x-2">
                        <span className={`px-2 py-1 rounded text-xs font-medium ${
                            field.required
                                ? 'bg-red-100 text-red-800'
                                : 'bg-gray-100 text-gray-600'
                        }`}>
                          {field.required ? 'Required' : 'Optional'}
                        </span>
                                                <span className="px-2 py-1 bg-blue-100 text-blue-800 rounded text-xs font-medium">
                          {field.data_type}
                        </span>
                                            </div>
                                        </div>
                                        <p className="text-gray-600 mb-2">{field.description}</p>
                                        {field.validation_rules && (
                                            <p className="text-sm text-gray-500 mb-1">
                                                <span className="font-medium">Validation:</span> {field.validation_rules}
                                            </p>
                                        )}
                                        {field.conditional_logic && field.conditional_logic !== "None" && (
                                            <p className="text-sm text-gray-500 mb-1">
                                                <span className="font-medium">Conditions:</span> {field.conditional_logic}
                                            </p>
                                        )}
                                        {field.options.length > 0 && (
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
                                ))}
                            </div>

                            <div className="mt-6 p-4 bg-green-50 border border-green-200 rounded-lg flex items-center">
                                <CheckCircle className="w-5 h-5 text-green-500 mr-2" />
                                <span className="text-green-700">
                  Form analysis complete! Ready for Phase 2 (Translation)
                </span>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </div>
    );
};

export default ImmigrationFormAnalyzer;