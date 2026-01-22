import type { Problem } from "./types";

function capitalizeFirstLetter(str: string): string {
  return str.charAt(0).toUpperCase() + str.slice(1);
}

export function prettyPrintParams({ problem, params, seed }: Problem): string {
  const paramsFormatted = Object.entries(params)
    .map(([key, value]) => `${capitalizeFirstLetter(key)}: ${JSON.stringify(value)}`)
    .join(", ");
  return `Problem ${problem}\n${paramsFormatted}\nSeed: ${seed}`;
}
