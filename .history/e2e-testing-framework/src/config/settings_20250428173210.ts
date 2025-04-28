export const settings = {
    googleSheetsApiKey: process.env.GOOGLE_SHEETS_API_KEY || '',
    googleSheetsId: process.env.GOOGLE_SHEETS_ID || '',
    timeout: {
        pageLoad: 30000, // 30 seconds
        elementCheck: 5000 // 5 seconds
    },
    headlessMode: true,
    browserOptions: {
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    }
};