export class Lesson {
    public readonly id: number;
    public userID: number;
    public progress: Map<string, boolean>;

    constructor(id: number, userID: number) {
        this.id = id;
        this.userID = userID;
        this.progress = new Map<string, boolean>([
            ["1.1", false],
            ["1.2", false],
            ["1.3", false],
            ["2.1", false],
            ["2.2", false],
            ["2.3", false],
            ["3.1", false],
            ["3.2", false],
            ["3.3", false]
        ]);
    }
}