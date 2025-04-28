import { ElementChecker } from './core/element-checker';
import { CsvHandler } from './utils/csv-handler';
import path from 'path';

async function main() {
    const csvFilePath = process.argv[2] || path.join(__dirname, '../data/test-cases.csv');
    console.log(`Reading test cases from ${csvFilePath}`);
    const csvHandler = new CsvHandler(csvFilePath);
    const elementChecker = new ElementChecker();

    try {
        await elementChecker.initialize();
        const testCases = await csvHandler.readTestCases();
        console.log(`Found ${testCases.length} test cases`);

        if (testCases.length === 0) {
            console.log('No test cases found. Please check your CSV file.');
            return;
        }

        for (let i = 0; i < testCases.length; i++) {
            const testCase = testCases[i];
            console.log(`[${i + 1}/${testCases.length}] Testing ${testCase.url} for ${testCase.targetNode}`);
            try {
                testCase.status = await elementChecker.checkElementPresence(testCase.url, testCase.targetNode);
                console.log(`Result: ${testCase.status}`);
            } catch (error) {
                console.error(`Error processing test case: ${error}`);
                testCase.status = 'error';
            }
        }

        await csvHandler.writeTestResults(testCases);
    } catch (error) {
        console.error('Error running tests:', error);
    } finally {
        await elementChecker.close();
    }
}

main().catch(error => console.error('Unhandled error:', error));