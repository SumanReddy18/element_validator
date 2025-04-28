import * as fs from 'fs';
import * as path from 'path';
import { TestCase } from '../models/test-case';

export class CsvHandler {
    constructor(private filePath: string) {}

    async readTestCases(): Promise<TestCase[]> {
        try {
            const data = await fs.promises.readFile(this.filePath, 'utf8');
            const lines = data.split('\n').filter(line => line.trim() !== '');
            
            return lines.map(line => {
                // Handle the case where there might be a comment at the beginning of the line
                if (line.startsWith('//')) {
                    return null;
                }
                
                const [url, targetNode] = line.split(',');
                if (!url || !targetNode) {
                    return null;
                }
                
                return new TestCase(url.trim(), targetNode.trim(), 'pending');
            }).filter(Boolean) as TestCase[]; // Filter out null values
        } catch (error) {
            console.error(`Error reading CSV file: ${error}`);
            return [];
        }
    }

    async writeTestResults(testCases: TestCase[]): Promise<void> {
        try {
            const lines = testCases.map(tc => `${tc.url},${tc.targetNode},${tc.status}`);
            const content = lines.join('\n');
            
            await fs.promises.writeFile(this.filePath, content, 'utf8');
            console.log(`Results written to ${this.filePath}`);
        } catch (error) {
            console.error(`Error writing test results to CSV: ${error}`);
        }
    }
}
