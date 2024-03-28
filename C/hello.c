#include <stdio.h>


int askQuestion(const char *question, const char *option1, const char *option2, const char *option3, const char *correctAnswer) {
    printf("%s\n", question);
    printf("A. %s\nB. %s\nC. %s\n", option1, option2, option3);

    char userAnswer;
    printf("Your answer (A, B, or C): ");
    scanf(" %c", &userAnswer);

    if (userAnswer == correctAnswer[0]) {
        printf("Correct!\n");
        return 1; 
    } else {
        printf("Incorrect. The correct answer is %c. \n", correctAnswer[0]);
        return 0; 
    }
}

int main() {
    int score = 0;

    // Question 1
    score += askQuestion("What is the capital of France?", "Paris", "Berlin", "London", "A");

    // Question 2
    score += askQuestion("Which planet is known as the Red Planet?", "Mars", "Jupiter", "Venus", "A");

    // Question 3
    score += askQuestion("What is the largest mammal in the world?", "Elephant", "Blue Whale", "Giraffe", "B");

    // Question 4
    score += askQuestion("Who's the prime minister of India?", "Rahul Gandhi", "Arvind Kejriwal", "Narendra Modi", "C");

    // Display final score
    printf("Your final score: %d out of 4\n", score);

    return 0;
}