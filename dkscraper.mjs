import fs from 'fs';
import path from 'path';
import fetch from 'node-fetch';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const API_URL = "https://sportsbook-nash.draftkings.com/api/sportscontent/dkusmd/v1/leagues/84240";
const CSV_PATH = path.join(__dirname, 'data', 'csv', 'dk.csv');
const INTERVAL = 60 * 1000; // 60 seconds

async function getDraftKingsMLB() {
  // Function to get baseball data from DraftKings
  console.log('Starting DraftKings MLB scrape...');

  try {
    const res = await fetch(API_URL);
    const data = await res.json();

    const selections = data["selections"];
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
        console.log(`Added row: ${JSON.stringify(row)}`);
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
  // Function to write collected data to csv
  if (rows.length === 0) {
    console.log('No rows to write to CSV');
    return;
  }
  
  const headers = ['id', 'marketId', 'label', 'americanOdds', 'decimalOdds', 'fractionalOdds', 'trueOdds', 'outcomeType', 'sortOrder', 'tags', 'main', 'collected_at'];
  const csvLines = rows.map(row => headers.map(h => row[h]).join(','));
  
  try {
    // Ensure directory exists
    fs.mkdirSync(path.dirname(CSV_PATH), { recursive: true });
    
    // Check if file exists to decide whether to write headers
    const fileExists = fs.existsSync(CSV_PATH);
    
    if (!fileExists) {
      fs.writeFileSync(CSV_PATH, headers.join(',') + '\n');
      console.log('Created new CSV file with headers');
    }
    
    // Append data
    fs.appendFileSync(CSV_PATH, csvLines.join('\n') + '\n');
    console.log(`Successfully appended ${rows.length} rows to CSV`);
    
  } catch (e) {
    console.error('Error writing to CSV:', e);
  }
}

async function main() {
  console.log('MLB Scraper starting...');
  
  while (true) {
    try {
      const rows = await getDraftKingsMLB();
      
      if (rows.length > 0) {
        writeCSV(rows);
        console.log(`[${new Date().toLocaleTimeString()}] Wrote ${rows.length} rows to dk.csv`);
      } else {
        console.log(`[${new Date().toLocaleTimeString()}] No valid MLB rows found`);
      }
      
    } catch (e) {
      console.error('Scrape error:', e);
    }
    
    console.log(`Waiting ${INTERVAL/1000} seconds for next scrape...`);
    await new Promise(r => setTimeout(r, INTERVAL));
  }
}

main();