import React from 'react';

const NutrientVisualization = ({ nutrients }) => {
    const totalNutrients = Object.values(nutrients).reduce((acc, value) => acc + value, 0);

    return (
        <div className="p-4">
            <h2 className="text-xl font-bold mb-4">Nutrient Visualization</h2>
            <div className="flex flex-col">
                {Object.entries(nutrients).map(([nutrient, value]) => (
                    <div key={nutrient} className="mb-2">
                        <div className="flex justify-between">
                            <span>{nutrient}</span>
                            <span>{((value / totalNutrients) * 100).toFixed(2)}%</span>
                        </div>
                        <div className="bg-gray-200 rounded-full h-4">
                            <div
                                className="bg-blue-500 h-4 rounded-full"
                                style={{ width: `${(value / totalNutrients) * 100}%` }}
                            />
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
};

export default NutrientVisualization;