export interface Lesson {
    id : number;
    name: string;
    grammar: string;
    reading: string;
    listening: string;
    completed: Array<boolean>;
    score: Array<Number>;
}