function appendToDisplay(value) {
  document.getElementById('result').value += value;
}

function clearDisplay() {
  document.getElementById('result').value = '';
}

function backspace() {
  let currentValue = document.getElementById('result').value;
  document.getElementById('result').value = currentValue.slice(0, -1);
}

function calculate() {
  try {
      let expression = document.getElementById('result').value;
      // Replace × with * and ÷ with / for proper evaluation
      expression = expression.replace(/×/g, '*').replace(/÷/g, '/');
      const result = eval(expression);
      document.getElementById('result').value = result;
  } catch (error) {
      document.getElementById('result').value = 'Error';
  }
}