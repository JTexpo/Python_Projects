/* This JS Code Was Pair Programmed with Chat-GPT 3.5 */

const question = document.getElementById('question');
const answer = document.getElementById('answer');
const result = document.getElementById('result');
const submit = document.getElementById('submit');
const operatorButtons = document.querySelectorAll('.operator-button');
const maxNumberSize = 10

/**
 * A function to create a math question
 * 
 * @param {number} numberRange the largest number that x and y can be
 * @returns {string} the math question
 */
function generateQuestion(numberRange) {
    const x = Math.floor(Math.random() * numberRange) + 1;
    const y = Math.floor(Math.random() * numberRange) + 1;
    // If the operator button is selected, we want to use the active button, else we default to the addition operation
    const activeButton = document.querySelector('.operator-button.active');
    const operator = activeButton ? activeButton.dataset.operator : '+';
    return `${x} ${operator} ${y}`;
}

/**
 * An event listeners to the operator buttons
 * 
 */
operatorButtons.forEach((button) => {
    button.addEventListener('click', () => {
        // Remove the active class from all buttons
        operatorButtons.forEach((button) => {
            button.classList.remove('active');
        });

        // Add the active class to the clicked button
        button.classList.add('active');

        // Display a new random math question with the selected operator
        question.textContent = generateQuestion(maxNumberSize);
    });
});

/**
 * An event listner for when the user clicks the submit button
 * 
 */
submit.addEventListener('click', () => {
    const userAnswer = parseFloat(answer.value).toFixed(2);
    const questionArr = question.textContent.split(' ');
    const x = parseInt(questionArr[0]);
    const operator = questionArr[1];
    const y = parseInt(questionArr[2]);
    let correctAnswer;

    // Calculate the correct answer based on the selected operator
    switch (operator) {
        case '+':
            correctAnswer = x + y;
            break;
        case '-':
            correctAnswer = x - y;
            break;
        case '*':
            correctAnswer = x * y;
            break;
        case '/':
            correctAnswer = (x / y).toFixed(2);
            break;
    }

    // Display the result
    if (parseFloat(userAnswer) === parseFloat(correctAnswer)) {
        result.textContent = 'Correct!';
    } else {
        result.textContent = `Incorrect. The correct answer was ${x} ${operator} ${y} = ${correctAnswer}.`;
    }

    // Display a new random math question
    question.textContent = generateQuestion(maxNumberSize);

    // Clear the answer field
    answer.value = '';
});

// Display the random math question on creation
question.textContent = generateQuestion(maxNumberSize);