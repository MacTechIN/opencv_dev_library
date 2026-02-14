import { BookOpen, ExternalLink } from 'lucide-react';
import { OpenCVFunction } from '../data/opencv-functions';

interface UsagePanelProps {
  selectedFunction: OpenCVFunction | null;
}

export function UsagePanel({ selectedFunction }: UsagePanelProps) {
  if (!selectedFunction) {
    return (
      <div className="p-4 bg-gray-50 rounded-lg border border-gray-200 text-center text-gray-500">
        함수를 선택하면 사용법이 표시됩니다.
      </div>
    );
  }

  return (
    <div className="space-y-3">
      <div className="p-4 bg-slate-50 rounded-lg border border-slate-300">
        <div className="flex items-center gap-2 mb-3">
          <BookOpen size={18} className="text-slate-600" />
          <h4 className="font-semibold text-slate-800">함수 문법</h4>
        </div>
        
        <div className="bg-slate-800 text-green-400 p-3 rounded font-mono text-sm overflow-x-auto">
          <code>{selectedFunction.syntax}</code>
        </div>
      </div>

      <div className="p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h4 className="font-semibold text-blue-900 mb-2 text-sm">파라미터 설명</h4>
        <div className="space-y-2 text-sm">
          <div className="text-blue-800">
            <span className="font-medium">src1:</span> 입력 소스 이미지
          </div>
          <div className="text-blue-800">
            <span className="font-medium">dst:</span> 출력 이미지 (목적지)
          </div>
          {selectedFunction.parameters.map((param) => (
            <div key={param.name} className="text-blue-800">
              <span className="font-medium">{param.name}:</span> {param.description}
            </div>
          ))}
        </div>
      </div>

      <a
        href={selectedFunction.documentation}
        target="_blank"
        rel="noopener noreferrer"
        className="flex items-center justify-center gap-2 w-full px-4 py-2.5 bg-indigo-500 text-white rounded-lg hover:bg-indigo-600 transition-colors text-sm"
      >
        <ExternalLink size={16} />
        OpenCV 공식 문서 보기
      </a>
    </div>
  );
}