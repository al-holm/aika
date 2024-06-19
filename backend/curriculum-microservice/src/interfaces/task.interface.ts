export enum TaskType {
    single_choice = "single-choice",
    gaps = "gaps",
    open = "open"
}

export interface Task {
    type: TaskType;
    question: string;
    options: Array<Array<string>>;
    userAnswers: Array<Array<string>>;
    solutions: Array<string>;
    completed: boolean;
    score: number;
}