import { OpenCVFunction } from '../data/opencv-functions';

interface ParameterInputProps {
  selectedFunction: OpenCVFunction;
  parameters: Record<string, any>;
  onParameterChange: (name: string, value: any) => void;
}

export function ParameterInput({
  selectedFunction,
  parameters,
  onParameterChange,
}: ParameterInputProps) {
  if (selectedFunction.parameters.length === 0) {
    return (
      <div className="p-4 bg-gray-50 rounded-lg border border-gray-200 text-center text-gray-600">
        이 함수는 파라미터가 필요하지 않습니다.
      </div>
    );
  }

  return (
    <div className="space-y-4">
      {selectedFunction.parameters.map((param) => {
        const value = parameters[param.name] ?? param.defaultValue;

        return (
          <div key={param.name} className="space-y-2">
            <label className="block text-sm font-medium">
              {param.name}
              <span className="ml-2 text-xs text-gray-500 font-normal">
                ({param.description})
              </span>
            </label>

            {param.type === 'slider' && (
              <div className="space-y-1">
                <div className="flex items-center gap-3">
                  <input
                    type="range"
                    min={param.min}
                    max={param.max}
                    step={param.step || 1}
                    value={value}
                    onChange={(e) => onParameterChange(param.name, parseFloat(e.target.value))}
                    className="flex-1 h-2 bg-gray-200 rounded-lg appearance-none cursor-pointer accent-blue-500"
                  />
                  <input
                    type="number"
                    min={param.min}
                    max={param.max}
                    step={param.step || 1}
                    value={value}
                    onChange={(e) => onParameterChange(param.name, parseFloat(e.target.value))}
                    className="w-20 px-2 py-1 border border-gray-300 rounded text-sm text-center"
                  />
                </div>
                <div className="flex justify-between text-xs text-gray-500">
                  <span>최소: {param.min}</span>
                  <span>최대: {param.max}</span>
                </div>
              </div>
            )}

            {param.type === 'number' && (
              <input
                type="number"
                min={param.min}
                max={param.max}
                step={param.step || 1}
                value={value}
                onChange={(e) => onParameterChange(param.name, parseFloat(e.target.value))}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            )}

            {param.type === 'select' && param.options && (
              <select
                value={value}
                onChange={(e) => onParameterChange(param.name, e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 bg-white"
              >
                {param.options.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            )}
          </div>
        );
      })}
    </div>
  );
}
