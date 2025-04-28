export const settings = {
    timeout: {
        pageLoad: process.env.TIMEOUT ? parseInt(process.env.TIMEOUT) : 30000, // 30 seconds
        elementCheck: process.env.ELEMENT_TIMEOUT ? parseInt(process.env.ELEMENT_TIMEOUT) : 5000 // 5 seconds
    },
    headlessMode: process.env.HEADLESS_MODE !== 'false',
    browserOptions: {
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    }
};