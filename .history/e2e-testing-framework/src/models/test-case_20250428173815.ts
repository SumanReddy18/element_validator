export class TestCase {
    constructor(
        public url: string,
        public targetNode: string,
        public status: string = 'pending'
    ) {}
}