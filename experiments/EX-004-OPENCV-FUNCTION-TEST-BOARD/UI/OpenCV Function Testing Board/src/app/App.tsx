import { useEffect, useState } from 'react';
import { Play, Loader2, AlertCircle } from 'lucide-react';
import { ImageUploader } from './components/ImageUploader';
import { FunctionSelector } from './components/FunctionSelector';
import { ParameterInput } from './components/ParameterInput';
import { OutputPanel } from './components/OutputPanel';
import { UsagePanel } from './components/UsagePanel';
import { OpenCVFunction } from './data/opencv-functions';
import { OpenCVProcessor } from './utils/opencv-processor';

export default function App() {
  const [isOpenCVLoaded, setIsOpenCVLoaded] = useState(false);
  const [loadingError, setLoadingError] = useState<string | null>(null);
  const [inputCanvas, setInputCanvas] = useState<HTMLCanvasElement | null>(null);
  const [inputImage, setInputImage] = useState<string | null>(null);
  const [inputCanvas2, setInputCanvas2] = useState<HTMLCanvasElement | null>(null);
  const [inputImage2, setInputImage2] = useState<string | null>(null);
  const [selectedFunction, setSelectedFunction] = useState<OpenCVFunction | null>(null);
  const [parameters, setParameters] = useState<Record<string, any>>({});
  const [outputImage, setOutputImage] = useState<string | null>(null);
  const [processingInfo, setProcessingInfo] = useState('');
  const [processingTime, setProcessingTime] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  useEffect(() => {
    // OpenCV.js 로드
    OpenCVProcessor.loadOpenCV()
      .then(() => {
        setIsOpenCVLoaded(true);
      })
      .catch((error) => {
        setLoadingError(error.message);
      });
  }, []);

  const handleImageLoad = (canvas: HTMLCanvasElement) => {
    setInputCanvas(canvas);
    setInputImage(canvas.toDataURL());
    setOutputImage(null);
    setProcessingInfo('');
  };

  const handleImageLoad2 = (canvas: HTMLCanvasElement) => {
    setInputCanvas2(canvas);
    setInputImage2(canvas.toDataURL());
    setOutputImage(null);
    setProcessingInfo('');
  };

  const handleImageClear = () => {
    setInputCanvas(null);
    setInputImage(null);
    setOutputImage(null);
    setProcessingInfo('');
    setSelectedFunction(null);
    setParameters({});
  };

  const handleImageClear2 = () => {
    setInputCanvas2(null);
    setInputImage2(null);
    setOutputImage(null);
    setProcessingInfo('');
  };

  const handleFunctionSelect = (func: OpenCVFunction) => {
    setSelectedFunction(func);
    // 파라미터 초기값 설정
    const initialParams: Record<string, any> = {};
    func.parameters.forEach((param) => {
      initialParams[param.name] = param.defaultValue;
    });
    setParameters(initialParams);
    setOutputImage(null);
    setProcessingInfo('');
  };

  const handleParameterChange = (name: string, value: any) => {
    setParameters((prev) => ({ ...prev, [name]: value }));
  };

  const handleProcess = () => {
    if (!inputCanvas || !selectedFunction) return;

    // 2개 이상의 입력이 필요한 함수인 경우 두 번째 이미지 확인
    if (selectedFunction.inputCount && selectedFunction.inputCount >= 2 && !inputCanvas2) {
      alert('이 함수는 src1과 src2 두 개의 입력이 필요합니다.');
      return;
    }

    setIsProcessing(true);
    const startTime = performance.now();

    try {
      const result = OpenCVProcessor.processImage(
        inputCanvas, 
        selectedFunction.id, 
        parameters,
        inputCanvas2 || undefined
      );
      const endTime = performance.now();

      setOutputImage(result.canvas.toDataURL());
      setProcessingInfo(result.info);
      setProcessingTime(endTime - startTime);
    } catch (error) {
      alert(`처리 중 오류가 발생했습니다: ${error instanceof Error ? error.message : '알 수 없는 오류'}`);
    } finally {
      setIsProcessing(false);
    }
  };

  const handleSave = () => {
    if (!outputImage) return;

    const link = document.createElement('a');
    link.href = outputImage;
    link.download = `opencv-${selectedFunction?.id || 'result'}-${Date.now()}.png`;
    link.click();
  };

  if (!isOpenCVLoaded) {
    return (
      <div className="size-full flex items-center justify-center bg-gray-50">
        <div className="text-center">
          {loadingError ? (
            <>
              <AlertCircle size={48} className="mx-auto mb-4 text-red-500" />
              <p className="text-lg text-gray-700 mb-2">OpenCV 로드 실패</p>
              <p className="text-sm text-gray-500">{loadingError}</p>
            </>
          ) : (
            <>
              <Loader2 size={48} className="mx-auto mb-4 text-blue-500 animate-spin" />
              <p className="text-lg text-gray-700">OpenCV 라이브러리 로딩 중...</p>
              <p className="text-sm text-gray-500 mt-2">잠시만 기다려주세요</p>
            </>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="size-full bg-gray-50 overflow-hidden">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-700 text-white px-6 py-4 shadow-lg">
        <h1 className="text-2xl font-bold">📚 OpenCV 내장 라이브러리 함수 테스팅 보드</h1>
        <p className="text-sm text-blue-100 mt-1">
          학생들을 위한 OpenCV 함수 학습 및 실습 도구 - 카테고리별 함수 탐색 및 파라미터 실험
        </p>
      </div>

      {/* Main Content */}
      <div className="h-[calc(100vh-88px)] flex">
        {/* Left Panel - Input */}
        <div className="w-[30%] border-r border-gray-300 bg-white overflow-y-auto">
          <div className="p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <span className="text-2xl">📥</span>
              src1
            </h2>
            <ImageUploader
              onImageLoad={handleImageLoad}
              currentImage={inputImage}
              onClear={handleImageClear}
            />

            {/* 2개 이상의 입력이 필요한 함수일 경우 두 번째 입력 이미지 표시 */}
            {selectedFunction && selectedFunction.inputCount && selectedFunction.inputCount >= 2 && (
              <div className="mt-6">
                <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                  <span className="text-2xl">📥</span>
                  src2
                </h2>
                <ImageUploader
                  onImageLoad={handleImageLoad2}
                  currentImage={inputImage2}
                  onClear={handleImageClear2}
                />
              </div>
            )}
          </div>
        </div>

        {/* Center Panel - Function Selection & Parameters */}
        <div className="flex-1 overflow-y-auto bg-white">
          <div className="p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <span className="text-2xl">⚙️</span>
              함수 선택 및 파라미터 설정
            </h2>

            <FunctionSelector
              selectedFunction={selectedFunction}
              onFunctionSelect={handleFunctionSelect}
            />

            {selectedFunction && (
              <div className="mt-6">
                <h3 className="text-md font-semibold mb-3">파라미터 설정</h3>
                <div className="p-4 bg-gray-50 rounded-lg border border-gray-200">
                  <div className="mb-4 pb-4 border-b border-gray-300">
                    <div className="font-medium">{selectedFunction.name}</div>
                    <div className="text-sm text-gray-600 mt-1">{selectedFunction.description}</div>
                  </div>
                  <ParameterInput
                    selectedFunction={selectedFunction}
                    parameters={parameters}
                    onParameterChange={handleParameterChange}
                  />
                </div>

                <button
                  onClick={handleProcess}
                  disabled={!inputCanvas || isProcessing}
                  className="mt-4 w-full flex items-center justify-center gap-2 px-6 py-3 bg-blue-500 text-white rounded-lg hover:bg-blue-600 disabled:bg-gray-300 disabled:cursor-not-allowed transition-colors"
                >
                  {isProcessing ? (
                    <>
                      <Loader2 size={20} className="animate-spin" />
                      처리 중...
                    </>
                  ) : (
                    <>
                      <Play size={20} />
                      함수 실행
                    </>
                  )}
                </button>
              </div>
            )}

            {!selectedFunction && (
              <div className="mt-6 p-8 bg-blue-50 border-2 border-blue-200 rounded-lg text-center">
                <p className="text-blue-700">
                  👆 위에서 함수를 선택하여 OpenCV 기능을 테스트하세요
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Right Panel - Output */}
        <div className="w-[30%] border-l border-gray-300 bg-white overflow-y-auto">
          <div className="p-6">
            <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
              <span className="text-2xl">📤</span>
              출력 결과
            </h2>
            <OutputPanel
              outputImage={outputImage}
              processingInfo={processingInfo}
              processingTime={processingTime}
              onSave={handleSave}
            />
            
            <div className="mt-6">
              <h2 className="text-lg font-semibold mb-4 flex items-center gap-2">
                <span className="text-2xl">📖</span>
                사용법
              </h2>
              <UsagePanel selectedFunction={selectedFunction} />
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}