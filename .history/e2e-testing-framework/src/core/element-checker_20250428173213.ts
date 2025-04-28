export class ElementChecker {
    constructor(private browser: any) {}

    async checkElementPresence(url: string, targetNode: string): Promise<string> {
        try {
            await this.browser.goto(url);
            const element = await this.browser.$(targetNode);
            const isVisible = await element.isDisplayed();

            return isVisible ? 'pass' : 'fail';
        } catch (error) {
            console.error(`Error checking element presence for URL: ${url}, Target Node: ${targetNode}`, error);
            return 'fail';
        }
    }
}