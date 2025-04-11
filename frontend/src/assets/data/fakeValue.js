import { useMemo } from 'react';

const getRandomInRange = (min, max) => {
  return Math.floor(Math.random() * (max - min + 1)) + min;
};

const randomStatValues = useMemo(() => ({
  positiveImpact: getRandomInRange(500, 800),             // Triệu
  negativeRatio: getRandomInRange(5, 20),                 // %
  transparency: getRandomInRange(70_000, 150_000),        // số cổ đông
  rating: getRandomInRange(1, 5),                         // từ 1 đến 5
}), []);
