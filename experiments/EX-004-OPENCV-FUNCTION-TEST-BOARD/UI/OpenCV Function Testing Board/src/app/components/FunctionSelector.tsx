import { Search } from 'lucide-react';
import { useState } from 'react';
import { categories, opencvFunctions, OpenCVFunction } from '../data/opencv-functions';

interface FunctionSelectorProps {
  selectedFunction: OpenCVFunction | null;
  onFunctionSelect: (func: OpenCVFunction) => void;
}

export function FunctionSelector({ selectedFunction, onFunctionSelect }: FunctionSelectorProps) {
  const [selectedCategory, setSelectedCategory] = useState<string>('all');
  const [searchTerm, setSearchTerm] = useState('');

  const filteredFunctions = opencvFunctions.filter((func) => {
    const categoryMatch = selectedCategory === 'all' || func.category === selectedCategory;
    const searchMatch =
      searchTerm === '' ||
      func.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
      func.description.toLowerCase().includes(searchTerm.toLowerCase());
    return categoryMatch && searchMatch;
  });

  return (
    <div className="space-y-4">
      <div>
        <label className="block text-sm font-medium mb-2">카테고리</label>
        <div className="flex flex-wrap gap-2">
          <button
            onClick={() => setSelectedCategory('all')}
            className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
              selectedCategory === 'all'
                ? 'bg-blue-500 text-white'
                : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
            }`}
          >
            전체
          </button>
          {categories.map((cat) => (
            <button
              key={cat.id}
              onClick={() => setSelectedCategory(cat.id)}
              className={`px-3 py-1.5 rounded-lg text-sm transition-colors ${
                selectedCategory === cat.id
                  ? 'bg-blue-500 text-white'
                  : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
              }`}
            >
              {cat.icon} {cat.name}
            </button>
          ))}
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">함수 검색</label>
        <div className="relative">
          <Search className="absolute left-3 top-1/2 -translate-y-1/2 text-gray-400" size={20} />
          <input
            type="text"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="함수명 또는 설명 검색..."
            className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </div>

      <div>
        <label className="block text-sm font-medium mb-2">
          함수 목록 ({filteredFunctions.length}개)
        </label>
        <div className="max-h-96 overflow-y-auto border border-gray-300 rounded-lg divide-y">
          {filteredFunctions.length === 0 ? (
            <div className="p-4 text-center text-gray-500">
              검색 결과가 없습니다.
            </div>
          ) : (
            filteredFunctions.map((func) => {
              const category = categories.find((c) => c.id === func.category);
              return (
                <button
                  key={func.id}
                  onClick={() => onFunctionSelect(func)}
                  className={`w-full text-left p-3 transition-colors ${
                    selectedFunction?.id === func.id
                      ? 'bg-blue-50 border-l-4 border-l-blue-500'
                      : 'hover:bg-gray-50'
                  }`}
                >
                  <div className="flex items-start gap-2">
                    <span className="text-lg flex-shrink-0">{category?.icon}</span>
                    <div className="flex-1 min-w-0">
                      <div className="font-medium text-sm truncate">{func.name}</div>
                      <div className="text-xs text-gray-600 mt-0.5 line-clamp-2">
                        {func.description}
                      </div>
                      {func.requiresGrayscale && (
                        <div className="text-xs text-orange-600 mt-1">
                          ⚠️ 그레이스케일 필요
                        </div>
                      )}
                    </div>
                  </div>
                </button>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
