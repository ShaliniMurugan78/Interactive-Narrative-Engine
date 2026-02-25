export const capitalize = (str) =>
  str ? str.charAt(0).toUpperCase() + str.slice(1) : "";

export const truncate = (str, len = 100) =>
  str && str.length > len ? str.slice(0, len) + "..." : str;

export const getChoiceLetter = (index) => ["A", "B", "C"][index] || String(index + 1);

export const genreEmoji = (genre) => ({
  fantasy  : "⚔️",
  horror   : "👁️",
  romance  : "🌹",
  scifi    : "🚀",
  mystery  : "🕵️",
  adventure: "🗺️"
}[genre] || "📖");

export const outcomeColor = (outcome) => ({
  Hero       : "#c9a84c",
  Triumphant : "#27ae60",
  Tragic     : "#c0392b",
  Bittersweet: "#8b6914",
  Mysterious : "#6b3fa0"
}[outcome] || "#c9a84c");
