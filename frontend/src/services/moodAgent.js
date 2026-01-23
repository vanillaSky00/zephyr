export const analyzeMoodAgent = (content) => {
  const text = content.toLowerCase();
  let mood = 'sweet'; 
  
  if (text.includes('累') || text.includes('sad') || text.includes('辛苦')) mood = 'bitter';
  if (text.includes('爽') || text.includes('happy') || text.includes('好棒')) mood = 'energetic';
  if (text.includes('平靜') || text.includes('chill')) mood = 'calm';

  const drinkConfig = {
    energetic: { name: "活力熱可可", icon: "🥤", quote: "燃起來了！這份熱情比咖啡還燙！🔥" },
    calm: { name: "靜謐拿鐵", icon: "☕", quote: "世界很吵，但你的心很靜。☕" },
    bitter: { name: "深夜黑咖啡", icon: "☕", quote: "辛苦了，苦澀過後留下的會是甘甜。💪" },
    sweet: { name: "幸福星冰樂", icon: "🍨", quote: "今天的生活加了點糖，真好。✨" }
  };
  return drinkConfig[mood];
};