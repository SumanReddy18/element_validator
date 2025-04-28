export interface TestCase {
    url: string;
    targetNode: string;
    status: 'pass' | 'fail';
}