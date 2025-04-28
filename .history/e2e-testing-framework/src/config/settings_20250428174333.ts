export const settings = {
    timeout: {
        pageLoad: process.env.TIMEOUT ? parseInt(process.env.TIMEOUT) : 30000,
        elementCheck: process.env.ELEMENT_TIMEOUT ? parseInt(process.env.ELEMENT_TIMEOUT) : 5000
    },
    headlessMode: process.env.HEADLESS_MODE !== 'false',
    browserOptions: {
        args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    }
};