import { ElementChecker } from './core/element-checker';
import { CsvHandler } from './utils/csv-handler';
import path from 'path';

async function main() {
    // Get CSV file path from command line arguments or use a default path
    const csvFilePath = process.argv[2] || path.join(__dirname, '../data/test-cases.csv');
    
    console.log(`Reading test cases from ${csvFilePath}`);
    const csvHandler = new CsvHandler(csvFilePath);
    const elementChecker = new ElementChecker();
    
    try {
        // Initialize the browser
        await elementChecker.initialize();
        
        // Read test cases from CSV file
        const testCases = await csvHandler.readTestCases();
        console.log(`Found ${testCases.length} test cases`);
        
        if (testCases.length === 0) {
            console.log('No test cases found. Please check your CSV file.');
            return;
        }
        
        // Process each test case
        for (let i = 0; i < testCases.length; i++) {
            const testCase = testCases[i];
            console.log(`[${i+1}/${testCases.length}] Testing ${testCase.url} for ${testCase.targetNode}`);
            
            try {
                testCase.status = await elementChecker.checkElementPresence(
                    testCase.url,
                    testCase.targetNode
                );
                
                console.log(`Result: ${testCase.status}`);
            } catch (error) {
                console.error(`Error processing test case: ${error}`);
                testCase.status = 'error';
            }
        }
        
        // Write results back to CSV file
        await csvHandler.writeTestResults(testCases);
    } catch (error) {
        console.error('Error running tests:', error);
    } finally {
        // Close the browser
        await elementChecker.close();
    }
}

// Run the main function
main().catch(error => console.error('Unhandled error:', error));