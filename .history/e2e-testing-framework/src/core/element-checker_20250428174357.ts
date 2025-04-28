import * as puppeteer from 'puppeteer';
import { settings } from '../config/settings';

export class ElementChecker {
    private browser: puppeteer.Browser | null = null;

    async initialize(): Promise<void> {
        this.browser = await puppeteer.launch({
            headless: settings.headlessMode,
            args: settings.browserOptions.args
        });
    }

    async checkElementPresence(url: string, targetNode: string): Promise<string> {
        if (!this.browser) {
            await this.initialize();
        }

        let page: puppeteer.Page | null = null;

        try {
            page = await this.browser.newPage();
            page.setDefaultNavigationTimeout(settings.timeout.pageLoad);
            await page.goto(url, { waitUntil: 'networkidle2' });
            await page.waitForSelector(targetNode, {
                timeout: settings.timeout.elementCheck,
                visible: true
            });
            return 'pass';
        } catch (error) {
            console.error(`Error checking element presence for URL: ${url}, Target Node: ${targetNode}`, error);
            return 'fail';
        } finally {
            if (page) {
                await page.close().catch(() => {});
            }
        }
    }

    async close(): Promise<void> {
        if (this.browser) {
            await this.browser.close().catch(() => {});
            this.browser = null;
        }
    }
}