import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const API_URL = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkusmd/v1/leagues/84240";
const CSV_PATH = path.join(__dirname, 'data', 'csv', 'dk.csv');

async function getDraftKingsMLB() {
  console.log('Starting DraftKings MLB scrape...');

  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    const selections = data["selections"] || [];
    console.log(`Found ${selections.length} selections`);

    const rows = [];

    for (const sel of selections) {
      try {
        const row = {
          id: sel.id,
          marketId: sel.marketId,
          label: sel.label,
          americanOdds: sel.displayOdds?.american || '',
          decimalOdds: sel.displayOdds?.decimal || '',
          fractionalOdds: sel.displayOdds?.fractional || '',
          trueOdds: sel.trueOdds,
          outcomeType: sel.outcomeType,
          sortOrder: sel.sortOrder,
          tags: (sel.tags || []).join(';'),
          main: sel.main,
          collected_at: new Date().toISOString()
        };

        rows.push(row);
      } catch (e) {
        console.error("Error parsing selection:", e);
      }
    }

    return rows;

  } catch (e) {
    console.error("Error fetching DraftKings data:", e);
    return [];
  }
}

function writeCSV(rows) {
  if (rows.length === 0) {
    console.log('No rows to write to CSV');
    return;
  }
  
  const headers = ['id', 'marketId', 'label', 'americanOdds', 'decimalOdds', 'fractionalOdds', 'trueOdds', 'outcomeType', 'sortOrder', 'tags', 'main', 'collected_at'];
  const csvLines = rows.map(row => headers.map(h => row[h]).join(','));
  const allLines = [headers.join(','), ...csvLines];

  try {
    // Ensure directory exists
    fs.mkdirSync(path.dirname(CSV_PATH), { recursive: true });

    // Overwrite file with new data
    fs.writeFileSync(CSV_PATH, allLines.join('\n') + '\n');
    console.log(`Wrote ${rows.length} rows to ${CSV_PATH}`);
    
  } catch (e) {
    console.error('Error writing to CSV:', e);
  }
}

async function main() {
  const rows = await getDraftKingsMLB();
  writeCSV(rows);
}

main();