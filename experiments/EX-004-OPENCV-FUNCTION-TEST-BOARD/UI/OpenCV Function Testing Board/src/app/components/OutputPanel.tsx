import { Download, Info } from 'lucide-react';

interface OutputPanelProps {
  outputImage: string | null;
  processingInfo: string;
  processingTime: number;
  onSave: () => void;
}

export function OutputPanel({
  outputImage,
  processingInfo,
  processingTime,
  onSave,
}: OutputPanelProps) {
  return (
    <div className="space-y-4">
      <div className="border-2 border-gray-300 rounded-lg overflow-hidden bg-gray-50">
        {outputImage ? (
          <img
            src={outputImage}
            alt="처리된 결과"
            className="w-full h-auto max-h-96 object-contain"
          />
        ) : (
          <div className="h-96 flex items-center justify-center text-gray-400">
            <div className="text-center">
              <Info size={48} className="mx-auto mb-2" />
              <p>처리 결과가 여기에 표시됩니다</p>
            </div>
          </div>
        )}
      </div>

      {outputImage && (
        <>
          <div className="p-4 bg-blue-50 border border-blue-200 rounded-lg">
            <div className="flex items-start gap-2">
              <Info size={20} className="text-blue-600 flex-shrink-0 mt-0.5" />
              <div className="flex-1">
                <div className="text-sm font-medium text-blue-900 mb-1">처리 정보</div>
                <div className="text-sm text-blue-700">{processingInfo}</div>
                <div className="text-xs text-blue-600 mt-1">
                  처리 시간: {processingTime.toFixed(2)}ms
                </div>
              </div>
            </div>
          </div>

          <button
            onClick={onSave}
            className="w-full flex items-center justify-center gap-2 px-4 py-3 bg-green-500 text-white rounded-lg hover:bg-green-600 transition-colors"
          >
            <Download size={20} />
            결과 이미지 저장
          </button>
        </>
      )}
    </div>
  );
}
