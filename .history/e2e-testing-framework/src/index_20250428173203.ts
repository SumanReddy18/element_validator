import { GoogleSheetsService } from './services/google-sheets.service';
import { TestRunnerService } from './services/test-runner.service';

async function main() {
    const googleSheetsService = new GoogleSheetsService();
    const testRunnerService = new TestRunnerService(googleSheetsService);

    try {
        await testRunnerService.runTests();
    } catch (error) {
        console.error('Error running tests:', error);
    }
}

main();